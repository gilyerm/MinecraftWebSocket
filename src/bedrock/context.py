from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from server import Server


class Context:
    """Context passed to event handlers."""

    _server: 'Server'

    def __init__(self, server: 'Server') -> None:
        self._server = server

    @property
    def server(self) -> 'Server':
        """A reference to the server object this context belongs to."""
        return self._server
