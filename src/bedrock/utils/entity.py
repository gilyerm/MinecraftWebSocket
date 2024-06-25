from .world_coordinate import WorldCoordinates, WorldCoordinate


class Entity:

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def color(self) -> str:
        return self._data["color"]

    @property
    def dimension(self) -> int:
        return self._data["dimension"]

    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def position(self) -> WorldCoordinates:
        position: dict = self._data["position"]
        return WorldCoordinates(
            (
                WorldCoordinate(position["x"]),
                WorldCoordinate(position["y"]),
                WorldCoordinate(position["z"]),
            )
        )

    @property
    def type(self) -> str:
        return self._data["type"]

    @property
    def variant(self) -> int:
        return self._data["variant"]

    @property
    def y_rot(self) -> float:
        return self._data["yRot"]
