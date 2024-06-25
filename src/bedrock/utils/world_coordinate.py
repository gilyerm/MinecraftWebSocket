from .utils import numeric


class WorldCoordinate:
    """
    A class representing a world coordinate.
    """

    coord: float
    is_relative: bool = False

    def __init__(self, coord: float, is_relative: bool = False) -> None:
        self.coord = coord
        self.is_relative = is_relative

    def __str__(self) -> str:
        return f"{'~' if self.is_relative else ''}{self.coord}"

    @classmethod
    def from_string(cls, value: str) -> 'WorldCoordinate':
        """Parses a world coordinate.

        Parameters
        ----------
        value
            The coordinate to parse.

        Examples
        --------
         code-block:: python

            x = WorldCoordinate.from_string("17")
            y = WorldCoordinate.from_string("~27")
            z = WorldCoordinate.from_string("~-27.4928")

            goto = WorldCoordinates((x, y, z))
        """
        n = value.removeprefix("~")
        return cls(numeric(n), is_relative=len(n) != len(value))


class WorldCoordinates:
    x: WorldCoordinate
    y: WorldCoordinate
    z: WorldCoordinate

    def __init__(self, coords: tuple[WorldCoordinate, WorldCoordinate, WorldCoordinate]) -> None:
        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2]

    def __str__(self) -> str:
        return f"({self.x.coord:.2f}, {self.y.coord:.2f}, {self.z.coord:.2f})"
