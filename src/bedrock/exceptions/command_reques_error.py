# pylint: disable=duplicate-code
from __future__ import annotations


class CommandRequestError(Exception):
    _message: str
    _status: int

    def __init__(self, message: str, status: int) -> None:
        self._message = message
        self._status = status

    def __str__(self) -> str:
        return self._message
