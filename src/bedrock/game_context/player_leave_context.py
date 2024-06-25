from .game_context import GameContext
from src.bedrock.utils import Player


class PlayerLeaveContext(GameContext):

    # NEED_TODO: Implement PlayerLeaveContext class

    def player(self) -> Player:
        return Player(self._data["player"])
