import asyncio
import base64
import json
import logging
import pprint
import ssl
import uuid
import warnings
from typing import Mapping, Any, Optional, Type

import convert_case
from websockets import server as wss
from websockets.exceptions import ConnectionClosedError

from src.bedrock import consts
from src.bedrock.commands import CommandResponse
from src.bedrock.encryption import EncryptionSession, AuthenticatedSession
from src.bedrock.exceptions import TimeoutAuthenticationError, RefusedAuthenticationError
from src.bedrock.game_context import GameContext
from src.bedrock.game_context_factory import get_game_context
from src.bedrock.server_components import EventHandling
from src.bedrock.server_context import DisconnectContext, ConnectContext, ReadyContext, ServerContext

logger = logging.getLogger(__name__)


class Server(EventHandling):
    _loop: asyncio.AbstractEventLoop | None
    _ws: wss.WebSocketServerProtocol | None
    _command_processing_semaphore: asyncio.BoundedSemaphore

    def __init__(self) -> None:
        super().__init__()
        self.unauthenticated_session = EncryptionSession()
        self._loop = None
        self._ws = None
        self._command_processing_semaphore = asyncio.BoundedSemaphore(
            consts.MAX_COMMAND_PROCESSING
        )

    def start(self, host: str, port: int) -> None:
        """
        Starts the server.

        Parameters
        ----------
        host
            The host to run the server on.

        port
            The port to run the server on.
        """

        self._setup_server(host, port)
        self._run_server()

    def _setup_server(self, host: str, port: int) -> None:
        """
        Sets up the server.

        Parameters
        ----------
        host : str
            The host to run the server on.

        port : int
            The port to run the server on.
        """
        server = wss.serve(self._websocket_handler,
                           host=host, port=port,
                           subprotocols=["com.microsoft.minecraft.wsencrypt"],
                           ping_interval=None,
                           logger=logger,
                           )
        self._loop = asyncio.get_event_loop()
        self._loop.run_until_complete(server)
        print(f"Server started @ {host}:{port}")
        self._dispatch_server_event(
            "ready", ReadyContext(self, host=host, port=port)
        )

    def _run_server(self) -> None:
        """
        Runs the server.

        This method starts the server and keeps it running until it is stopped.
        """
        try:
            self._loop.run_forever()
        except KeyboardInterrupt as e:
            raise KeyboardInterrupt from e
        finally:
            self._cleanup_server()

    def _cleanup_server(self) -> None:
        """
        Cleans up the server.

        This method is called when the server is stopped.
        It is responsible for cleaning up any resources that the server was using.
        """
        self._dispatch_server_event("disconnect", DisconnectContext(self))
        for t in asyncio.tasks.all_tasks(self._loop):
            t.cancel()
        self._loop.close()

    def close(self) -> None:
        """
        Closes the server.
        """
        if self._ws is None:
            raise RuntimeError("server is not running")
        assert self._loop is not None
        self._loop.create_task(self._ws.close())

    async def _websocket_handler(self, server: wss.WebSocketServerProtocol) -> None:
        """
        Handles the WebSocket connection.

        This method is responsible for setting up the WebSocket connection, dispatching server events,
        enabling encryption, and processing incoming data.

        Parameters
        ----------
        server : WebSocketServerProtocol
            The WebSocket server protocol instance.
        """
        logger.debug("handling ws")

        self._ws = server
        self._dispatch_server_event("connect", ConnectContext(self))

        # Send the enable encryption command
        session = await self.enable_encryption(self._ws, self.unauthenticated_session)

        logger.info(
            "Encrypted connection established, now listening for updates..."
        )

        for event_name in self._game_event_handlers:
            identifier = uuid.uuid4()
            await self._ws.send(
                session.encrypt(
                    json.dumps(
                        {
                            "header": {
                                "messageType": "commandRequest",
                                "messagePurpose": "subscribe",
                                "version": 1,
                                "requestId": str(identifier),
                            },
                            "body": {"eventName": convert_case.pascal_case(event_name)},
                        }
                    ).encode()
                )
            )

        try:
            first_message_encrypted = await self._ws.recv()
            first_message = session.decrypt(first_message_encrypted)
            first_data = json.loads(first_message)
            await self._process_first_data(first_data)
        except json.JSONDecodeError as json_err:
            logger.error(f"JSON decoding error: {json_err}")
            raise json_err

        try:
            async for message_encrypted in self._ws:
                logger.debug("processing data ...")
                try:
                    json.loads(message_encrypted)
                    logger.error("message is not encrypted")
                    continue
                except UnicodeDecodeError as _:  # noqa: F841
                    pass
                except json.JSONDecodeError as _:  # noqa: F841
                    pass
                message = session.decrypt(message_encrypted)
                data = json.loads(message)
                await self._process_data(data, session)
                logger.debug("processed data")
        except ConnectionClosedError:
            self._dispatch_server_event("disconnect", DisconnectContext(self))

        except ssl.SSLError as ssl_error:
            logger.error(f"SSL/TLS error occurred: {ssl_error}")

    def _dispatch_server_event(self, event_name: str, ctx: ServerContext) -> None:
        """
        Dispatches a server event.

        Parameters
        ----------
        event_name : str
            The name of the event to dispatch.

        ctx : ServerContext
            The context to pass to the event handler.
        """
        assert self._loop is not None
        server_event = self.get_server_event(event_name)
        logger.debug(f"triggering server event {event_name}... ")
        self._loop.create_task(server_event(ctx))
        logger.debug(f"triggered server event {event_name}")

    async def _process_first_data(self, data: Mapping[str, Any]) -> None:
        """
        Processes the first incoming data.

        This method processes the first incoming data and checks if the connection was successful.

        Parameters
        ----------
        data : Mapping[str, Any]
            The first incoming data to be processed.
        """

        if "body" not in data or "statusCode" not in data["body"] or type(data["body"]["statusCode"]) is not int:
            raise ValueError("Failed to connect to the Minecraft")

        if data["body"]["statusCode"] != 0:
            raise ConnectionError("Failed to connect to the Minecraft")

        logger.info("Connected to Minecraft!")

    async def _process_data(self, data: Mapping[str, Any], session: AuthenticatedSession) -> None:
        """
        Process the incoming data.

        This method takes the incoming data and the session, processes the data,
        and updates the session accordingly.

        Parameters
        ----------
        data : Mapping[str, Any]
            The incoming data to be processed.
        session : AuthenticatedSession
            The session associated with the data.
        """
        assert self._loop is not None

        header = data["header"]
        body = data["body"]
        event_name = None or convert_case.pascal_case(header.get("eventName", ""))

        event = self._game_event_handlers.get(event_name, None)
        if event is None:
            logger.error(f"unknown event {event_name!r}")
            return

        logger.debug(f"triggering event {event.name}...")
        try:
            game_context: Type[GameContext] = get_game_context(event.name)
            ctx = game_context(self, body, session)
        except KeyError:
            warnings.warn(f"unknown event name {event_name!r}", RuntimeWarning)
            ctx = GameContext(self, body, session)
        await self._loop.create_task(event(ctx, ))

    async def run(
            self, command: str, *,
            auth_session: Optional[AuthenticatedSession] = None
    ) -> CommandResponse:
        """
        Executes a Minecraft command.

        Note: The leading slash (`/`) may be omitted.

        Parameters
        ----------
        command : str
            The command to execute. For example, "setblock 10 10 10 stone".

        auth_session : AuthSession
            The authenticated session to use for encryption.
        """

        logger.debug(f"running command {command!r}")
        command = command.removeprefix("/")
        return await self.send(
            header={
                "messageType": "commandRequest",
                "messagePurpose": "commandRequest",
            },
            body={
                "commandLine": command,
                "origin": {"type": "player"},
            },
            auth_session=auth_session,
        )

    async def send(
            self,
            header: dict[str, Any],
            body: dict[str, Any],
            auth_session: Optional[AuthenticatedSession] = None
    ) -> Optional[CommandResponse]:
        """
        Sends data to the client.

        Parameters
        ----------
        header : dict
            The header data for the request.

        body : dict
            The body data for the request.

        auth_session : AuthenticatedSession
            The authenticated session to use for encryption.

        Returns
        -------
        asyncio.Future
            A future object representing the response of the request, wrapped in a :class:`~CommandResponse`.
        """
        assert self._ws is not None
        assert self._loop is not None

        identifier = uuid.uuid4()
        data = {
            "header": header | {"version": 1, "requestId": str(identifier)},
            "body": body,
        }

        async with self._command_processing_semaphore:
            logger.debug("sending data ...")
            d = json.dumps(data)
            if auth_session:
                logger.debug("encrypting the data...")
                d = auth_session.encrypt(d.encode())
            await self._ws.send(d)
            logger.debug("sent data")
        return None

    @staticmethod
    async def enable_encryption(websocket: wss.WebSocketServerProtocol, session: EncryptionSession) -> AuthenticatedSession:
        """
        Negotiates the authentication handshake.

        Parameters
        ----------
        websocket : WebSocket
            The WebSocket connection to enable encryption on.

        session : EncryptionSession
            The session to use for the encryption.

        Returns
        -------
        AuthenticatedSession
            The authenticated session after the encryption has been enabled.
        """

        # generate a unique request ID for the payload
        request_id = str(uuid.uuid1())
        public_key = session.b64_public_key
        salt = session.b64_salt

        authentication_payload = {
            "body": {
                "commandLine": f'enableencryption "{public_key}" "{salt}"',
                "version": 1,
            },
            "header": {
                "requestId": request_id,
                "messagePurpose": "commandRequest",
                "version": 1,
            },
        }

        await websocket.send(json.dumps(authentication_payload))

        # check that the response has a matching requestId
        for _ in range(3):
            response = json.loads(await websocket.recv())

            if response["header"]["requestId"] == request_id:
                break
        else:
            raise TimeoutAuthenticationError(
                "Not responding to unique request ID. "
                + "Check it's not busy with requests from multiple instances?"
            )

        try:
            public_key = base64.b64decode(response["body"]["publicKey"])
        except KeyError as e:
            raise RefusedAuthenticationError(
                f"Connection was refused. Response:\n{pprint.pformat(response)}"
            ) from e

        logger.debug(f"Received client public key= {public_key}")
        logger.debug(response)
        logger.debug(json.loads(await websocket.recv()))  # ignore the next message

        return AuthenticatedSession(session, public_key)
