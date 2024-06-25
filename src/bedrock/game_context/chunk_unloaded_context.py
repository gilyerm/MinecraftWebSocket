from .game_context import GameContext
from src.bedrock.utils import Chunk


class ChunkUnloadedContext(GameContext):

    @property
    def chunk(self) -> Chunk:
        return Chunk(self._data["chunk"])
