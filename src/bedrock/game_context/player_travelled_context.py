from .game_context import GameContext
from src.bedrock.utils import Player


class PlayerTravelledContext(GameContext):
    @property
    def underwater(self) -> bool:
        return self._data["isUnderwater"]

    @property
    def meters_travelled(self) -> float:
        return self._data["metersTravelled"]

    @property
    def new_biome(self) -> bool:
        return bool(self._data["newBiome"])

    @property
    def player(self) -> Player:
        return Player(self._data["player"])

    @property
    def travel_method(self) -> int:
        return self._data["travelMethod"]
