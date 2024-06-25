from .game_context import GameContext
from src.bedrock.utils import Item, Player


class ItemAcquiredContext(GameContext):

    @property
    def acquisition_method_id(self) -> int:
        return self._data["acquisitionMethodId"]

    @property
    def count(self) -> int:
        return self._data["count"]

    @property
    def item(self) -> Item:
        return Item(self._data["item"])

    @property
    def player(self) -> Player:
        return Player(self._data["player"])
