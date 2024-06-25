from typing import List


class Item:

    def __init__(self, data: dict):
        self._data = data

    @property
    def aux(self) -> int:
        return self._data["aux"]

    @property
    def enchantments(self) -> List[str]:
        return self._data["enchantments"]

    @property
    def free_stack_size(self) -> int:
        return self._data["freeStackSize"]

    @property
    def id(self) -> str:
        return self._data["id"]

    @property
    def max_stack_size(self) -> int:
        return self._data["maxStackSize"]

    @property
    def namespace(self) -> str:
        return self._data["namespace"]

    @property
    def stack_size(self) -> int:
        return self._data["stackSize"]
