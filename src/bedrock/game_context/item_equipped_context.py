from .game_context import GameContext
from src.bedrock.utils import Item, Player


class ItemEquippedContext(GameContext):

    @property
    def item(self) -> Item:
        return Item(self._data["item"])

    @property
    def player(self) -> Player:
        return Player(self._data["player"])

    @property
    def slot(self) -> int:
        return self._data["slot"]
