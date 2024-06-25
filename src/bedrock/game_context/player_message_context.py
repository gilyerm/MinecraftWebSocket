from src.bedrock.commands import CommandResponse
from src.bedrock.utils import rawtext
from .game_context import GameContext


class PlayerMessageContext(GameContext):
    @property
    def message(self) -> str:
        """The message."""
        return self._data["message"]

    @property
    def receiver(self) -> str | None:
        """The receiver of the message.

         note:: This may be ``None`` if there was no specific receiver.
        """
        return None or self._data["receiver"]

    @property
    def sender(self) -> str:
        """The sender of the message."""
        return self._data["sender"]

    @property
    def type(self) -> str:
        """The type of the message."""
        return self._data["type"]

    async def reply(
            self, message: str, *, raw: bool = False,
    ) -> CommandResponse:
        if raw:
            command = f"tellraw {self.sender} {rawtext(message)}"
        else:
            command = f"tell {self.sender} {message}"
        return await self.server.run(command, auth_session=self.session)
