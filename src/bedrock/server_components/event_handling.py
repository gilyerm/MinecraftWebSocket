import logging

import convert_case

from src.bedrock.events import GameEvent, ServerEvent
from src.bedrock.events.event import EventHandler

logger = logging.getLogger(__name__)


class EventHandling:
    _game_event_handlers: dict[str, GameEvent]
    _server_event_handlers: dict[str, ServerEvent]

    def __init__(self):
        self._game_event_handlers = {}
        self._server_event_handlers = {}

    def server_event(self, fn: EventHandler, /) -> ServerEvent:
        """
        Convenient decorator for adding a server event handler.

        The decorated function name must match the name of the event to listen to.
        It takes one positional argument which is an instance of :class:`context.ServerContext` of the event.

        Examples
        --------
        Example usage of the decorator:

        .. code-block:: python

            @app.server_event
            async def ready(ctx):
                print(f"Ready @ {ctx.host}:{ctx.port}")

        Parameters
        ----------
        fn : callable
            The decorated function.

        Returns
        -------
        events.ServerEvent
            The function turned into a :class:`events.ServerEvent`.
        """

        event = ServerEvent(fn.__name__, fn)
        logger.info(f"adding server event {event.name}")
        self.add_server_event(event)
        return event

    def add_server_event(self, event: ServerEvent) -> None:
        """
        Adds a server event to the server event handlers.
        """
        self._server_event_handlers[event.name] = event

    def remove_server_event(self, event: ServerEvent) -> None:
        """
        Removes a server event from the event handlers.

        Raises
        ------
        ValueError
            If the event is not registered.
        """
        del self._server_event_handlers[event.name]

    def get_server_event(self, event_name: str) -> ServerEvent:
        """
        Retrieves a server event by its name.

        Parameters
        ----------
        event_name : str
            The name of the event.

        Returns
        -------
        ServerEvent
            The corresponding server event.
        """
        return self._server_event_handlers[event_name]

    def game_event(self, fn: EventHandler, /) -> GameEvent:
        """
        Convenient decorator for adding a game event listener.

        The decorated function name must match the name of the event to listen to.
        It takes one positional argument which is an instance of :class:`context.GameContext` of the event.

        Examples
        --------
        Example usage of the decorator:

        .. code-block:: python

            @app.server_event
            async def player_message(ctx):
                ctx.reply("Hello World!")

        Parameters
        ----------
        fn : callable
            The decorated function.

        Returns
        -------
        events.GameEvent
            The function turned into a :class:`events.GameEvent`.
        """

        try:
            function_name = convert_case.pascal_case(fn.__name__)
        except AttributeError:
            function_name = fn.__name__
            logger.error(f"function name {function_name} is not a valid function name")

        event = GameEvent(function_name, fn)
        logger.info(f"adding game event {event.name}")
        self.add_game_event(event)
        return event

    def add_game_event(self, event: GameEvent) -> None:
        """
        Adds a game event to the game event handlers.
        """
        self._game_event_handlers[event.name] = event

    def remove_game_event(self, event: GameEvent) -> None:
        """
        Removes a game event from the event handlers.

        Raises
        ------
        ValueError
            If the event is not registered.
        """
        del self._game_event_handlers[event.name]

    def get_game_event(self, event_name: str) -> GameEvent:
        """
        Retrieves a game event by its name.

        Parameters
        ----------
        event_name : str
            The name of the event.

        Returns
        -------
        GameEvent
            The corresponding game event.
        """
        return self._game_event_handlers[event_name]
