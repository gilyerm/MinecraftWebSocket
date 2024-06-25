from .game_context import GameContext
from src.bedrock.utils import Item, Player


class ItemCraftedContext(GameContext):

    @property
    def count(self) -> int:
        return self._data["count"]

    @property
    def crafted_automatically(self) -> bool:
        return self._data["craftedAutomatically"]

    @property
    def ending_tab_id(self) -> str:
        return self._data["endingTabId"]

    @property
    def has_craftable_filter_on(self) -> bool:
        return self._data["hasCraftableFilterOn"]

    @property
    def item(self) -> Item:
        return Item(self._data["item"])

    @property
    def number_of_tabs_changed(self) -> int:
        return self._data["numberOfTabsChanged"]

    @property
    def player(self) -> Player:
        return Player(self._data["player"])

    @property
    def recipe_book_shown(self) -> bool:
        return self._data["recipeBookShown"]

    @property
    def starting_tab_id(self) -> str:
        return self._data["startingTabId"]

    @property
    def used_crafting_table(self) -> bool:
        return self._data["usedCraftingTable"]

    @property
    def used_search_bar(self) -> bool:
        return self._data["usedSearchBar"]
