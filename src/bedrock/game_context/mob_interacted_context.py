from .game_context import GameContext
from src.bedrock.utils import Player, Mob


class MobInteractedContext(GameContext):

    @property
    def interation_type(self) -> int:
        return self._data["interactionType"]

    @property
    def mob(self) -> Mob:
        return Mob(self._data["mob"])

    @property
    def player(self) -> Player:
        return Player(self._data["player"])
