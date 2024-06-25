from typing import TYPE_CHECKING

from .server_context import ServerContext

if TYPE_CHECKING:
    from src.bedrock.server import Server


class ReadyContext(ServerContext):
    _host: str
    _port: int

    def __init__(self, server: 'Server', host: str, port: int):
        super().__init__(server)
        self._host = host
        self._port = port

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port
