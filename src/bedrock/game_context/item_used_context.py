from .game_context import GameContext
from src.bedrock.utils import Player, Item


class ItemUsedContext(GameContext):

    @property
    def count(self) -> int:
        return self._data["count"]

    @property
    def item(self) -> Item:
        return Item(self._data["item"])

    @property
    def player(self) -> Player:
        return Player(self._data["player"])

    @property
    def use_method(self) -> int:
        return self._data["useMethod"]
