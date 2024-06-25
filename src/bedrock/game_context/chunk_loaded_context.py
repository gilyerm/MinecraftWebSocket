from .game_context import GameContext
from src.bedrock.utils import Chunk


class ChunkLoadedContext(GameContext):

    @property
    def chunk(self) -> Chunk:
        return Chunk(self._data["chunk"])
