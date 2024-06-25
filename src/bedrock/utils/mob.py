class Mob:

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def color(self) -> str:
        return self._data["color"]

    @property
    def type(self) -> str:
        return self._data["type"]

    @property
    def variant(self) -> int:
        return self._data["variant"]
