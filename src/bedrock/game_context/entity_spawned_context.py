from .game_context import GameContext
from src.bedrock.utils import Player, Mob


class EntitySpawnedContext(GameContext):

    @property
    def mob(self) -> Mob:
        return Mob(self._data["mob"])

    @property
    def player(self) -> Player:
        return Player(self._data["player"])

    @property
    def spawn_type(self) -> int:
        return self._data["spawnType"]
