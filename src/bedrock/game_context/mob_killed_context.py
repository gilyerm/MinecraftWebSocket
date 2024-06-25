from .game_context import GameContext
from src.bedrock.utils import Entity, Tool, Player, Armor


class MobKilledContext(GameContext):

    @property
    def armor_feet(self) -> Armor:
        return Armor(self._data["armorFeet"])

    @property
    def armor_head(self) -> Armor:
        return Armor(self._data["armorHead"])

    @property
    def armor_legs(self) -> Armor:
        return Armor(self._data["armorLegs"])

    @property
    def armor_torso(self) -> Armor:
        return Armor(self._data["armorTorso"])

    @property
    def is_monster(self) -> bool:
        return self._data["isMonster"]

    @property
    def kill_method_type(self) -> int:
        return self._data["killMethodType"]

    @property
    def player(self) -> Player:
        return Player(self._data["player"])

    @property
    def player_is_hidden_from(self) -> bool:
        return self._data["playerIsHiddenFrom"]

    @property
    def victim(self) -> Entity:
        return Entity(self._data["victim"])

    @property
    def weapon(self) -> Tool:
        return Tool(self._data["weapon"])
