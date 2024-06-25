from .game_context import GameContext
from src.bedrock.utils import Player


class PlayerTeleportedContext(GameContext):

    @property
    def cause(self) -> int:
        return self._data["cause"]

    @property
    def item_type(self) -> int:
        return self._data["itemType"]

    @property
    def meters_travelled(self) -> float:
        return self._data["metersTravelled"]

    @property
    def player(self) -> Player:
        return Player(self._data["player"])
