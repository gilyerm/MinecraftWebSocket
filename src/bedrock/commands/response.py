# pylint: disable=duplicate-code
from typing import Mapping

from src.bedrock.exceptions import CommandRequestError


class CommandResponse:
    """A response sent by the client."""

    _message: str
    _status: int

    def __init__(self, message: str, status: int):
        self._message = message
        self._status = status

    @property
    def message(self) -> str:
        return self._message

    @property
    def status(self) -> int:
        return self._status

    @property
    def ok(self) -> bool:
        """Returns ``True`` when the command has been executed successfully."""
        return self.status == 0

    @classmethod
    def parse(cls, data: Mapping[str, any]) -> 'CommandResponse':
        return cls(
            message=data["body"].get("statusMessage"),
            status=data["body"]["statusCode"],
        )

    def raise_for_status(self) -> None:
        """
        Raises :class:`bedrock.exceptions.CommandRequestError` if the command did
        not run successfully. Otherwise this method returns ``None``.
        """
        if not self.ok:
            raise CommandRequestError(self.message, self.status)
