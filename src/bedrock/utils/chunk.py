class Chunk:

    def __init__(self, data: dict):
        self._data = data

    @property
    def dimension(self) -> int:
        return self._data["dimension"]

    @property
    def x(self) -> int:
        return self._data["x"]

    @property
    def z(self) -> int:
        return self._data["z"]
    
    def __str__(self) -> str:
        return f"Chunk(x={self.x}, z={self.z}, dimension={self.dimension})"
