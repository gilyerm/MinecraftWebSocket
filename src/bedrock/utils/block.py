class Block:

    def __init__(self, data: dict):
        self._data = data

    @property
    def aux(self) -> int:
        return self._data["aux"]

    @property
    def id(self) -> str:
        return self._data["id"]

    @property
    def namespace(self) -> str:
        return self._data["namespace"]
