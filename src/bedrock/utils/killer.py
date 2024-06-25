class Killer:

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def color(self) -> int:
        return self._data["color"]

    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def type(self) -> int:
        return self._data["type"]

    @property
    def variant(self) -> int:
        return self._data["variant"]
