from .game_context import GameContext
from src.bedrock.utils import Item, Player


class EntityInteractedContext(GameContext):

    @property
    def count(self) -> int:
        return self._data["count"]

    @property
    def item(self) -> Item:
        return Item(self._data["item"])

    @property
    def method(self) -> int:
        return self._data["method"]

    @property
    def player(self) -> Player:
        return Player(self._data["player"])
