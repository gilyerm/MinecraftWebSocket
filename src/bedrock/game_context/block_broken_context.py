from .game_context import GameContext
from src.bedrock.utils import Player, Block, Tool


class BlockBrokenContext(GameContext):

    @property
    def block(self) -> Block:
        return Block(self._data["block"])

    @property
    def count(self) -> int:
        return self._data["count"]

    @property
    def destruction_method(self) -> int:
        return self._data["destructionMethod"]

    @property
    def player(self) -> Player:
        return Player(self._data["player"])

    @property
    def tool(self) -> Tool:
        return Tool(self._data["tool"])

    @property
    def variant(self) -> int:
        return self._data["variant"]
