from .game_context import GameContext
from src.bedrock.utils import Player, Killer


class PlayerDiedContext(GameContext):

    @property
    def cause(self) -> int:
        return self._data["cause"]

    @property
    def in_raid(self) -> bool:
        return self._data["inRaid"]

    @property
    def killer(self) -> Killer:
        return Killer(self._data["killer"])

    @property
    def player(self) -> Player:
        return Player(self._data["player"])
