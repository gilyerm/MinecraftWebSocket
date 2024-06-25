from .game_context import GameContext
from src.bedrock.utils import Block, Player


class PlayerBouncedContext(GameContext):

    @property
    def block(self) -> Block:
        return Block(self._data["block"])

    @property
    def bounce_height(self) -> float:
        return self._data["bounceHeight"]

    @property
    def player(self) -> Player:
        return Player(self._data["player"])
