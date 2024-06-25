from .game_context import GameContext
from src.bedrock.utils import Player


class PlayerTransformContext(GameContext):
    @property
    def player(self) -> Player:
        return Player(self._data["player"])
