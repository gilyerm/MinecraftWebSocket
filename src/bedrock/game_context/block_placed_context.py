from src.bedrock.utils import Player, Block, Tool
from .game_context import GameContext


class BlockPlacedContext(GameContext):

    @property
    def block(self) -> Block:
        return Block(self._data["block"])

    @property
    def count(self) -> int:
        return self._data["count"]

    @property
    def placed_under_water(self) -> bool:
        return self._data["placedUnderWater"]

    @property
    def placement_method(self) -> int:
        return self._data["placementMethod"]

    @property
    def player(self) -> Player:
        return Player(self._data["player"])

    @property
    def tool(self) -> str | Tool:
        return None or Tool(self._data["tool"])
