import asyncio
from typing import Mapping, Any
from uuid import UUID

from src.bedrock.commands.response import CommandResponse


class CommandRequest:
    """A command request sent to the server."""

    _identifier: UUID
    _data: Mapping[str, Any]
    _response: asyncio.Future[CommandResponse]

    def __init__(self, identifier: UUID, data: Mapping[str, Any], response: asyncio.Future[CommandResponse]) -> None:
        self._identifier = identifier
        self._data = data
        self._response = response

    @property
    def identifier(self) -> UUID:
        return self._identifier

    @property
    def data(self) -> Mapping[str, Any]:
        return self._data

    @property
    def response(self) -> asyncio.Future[CommandResponse]:
        return self._response
