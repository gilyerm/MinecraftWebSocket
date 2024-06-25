from .game_context import GameContext
from src.bedrock.utils import Chunk


class ChunkChangedContext(GameContext):

    @property
    def chunk(self) -> Chunk:
        return Chunk(self._data["chunk"])
