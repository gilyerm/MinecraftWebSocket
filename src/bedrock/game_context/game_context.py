import json
import logging
from typing import Mapping, Any, TYPE_CHECKING

from src.bedrock.context import Context
from src.bedrock.encryption import AuthenticatedSession

if TYPE_CHECKING:
    from src.bedrock.server import Server

logger = logging.getLogger(__name__)


class GameContext(Context):
    """Context passed to game event handlers."""

    _data: Mapping[str, Any]
    __session: AuthenticatedSession

    def __init__(self, server: 'Server', data: Mapping[str, Any], session: AuthenticatedSession) -> None:
        super().__init__(server)
        self._data = data
        self.__session = session
        logger.debug(json.dumps(data, indent=4))

    @property
    def session(self) -> AuthenticatedSession:
        return self.__session
