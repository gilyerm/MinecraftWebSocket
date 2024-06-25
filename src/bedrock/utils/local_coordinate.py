from .utils import numeric


class LocalCoordinate:
    """
    A class representing a local coordinate.
    """

    coord: float

    def __init__(self, coord: float) -> None:
        self.coord = coord

    def __str__(self) -> str:
        return f"^{self.coord}"

    @classmethod
    def from_string(cls, value: str) -> 'LocalCoordinate':
        """Parses a local coordinate.

        Parameters
        ----------
        value
            The coordinate to parse.

        Examples
        --------
        .. code-block:: python

            from bedrock.utils import LocalCoordinate, LocalCoordinates

            x = LocalCoordinate.from_string("^1")
            y = LocalCoordinate.from_string("^-19.5752")
            z = LocalCoordinate.from_string("^0")

            goto = LocalCoordinates((x, y, z))
        """
        n = value.removeprefix("^")
        if len(n) != len(value):
            raise ValueError("local coordinate must start with a caret (^)")
        return cls(numeric(n))


class LocalCoordinates:
    x: LocalCoordinate
    y: LocalCoordinate
    z: LocalCoordinate

    def __init__(self, coords: tuple[LocalCoordinate, LocalCoordinate, LocalCoordinate]) -> None:
        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2]

    def __str__(self) -> str:
        return f"({self.x.coord:.2f}, {self.y.coord:.2f}, {self.z.coord:.2f})"
