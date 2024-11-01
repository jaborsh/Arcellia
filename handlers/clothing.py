from copy import copy
from typing import Any, List, Optional

from evennia.utils.utils import inherits_from

from handlers.config.clothing_config import ClothingConfig
from handlers.handler import Handler
from typeclasses.clothing import Clothing


class ClothingHandler(Handler):
    """
    Handler for managing clothing items on a character or object.

    This handler manages the wearing, removal, and tracking of clothing items,
    including their layering and coverage relationships.

    Inherits from:
        Handler: Base handler class for attribute management
    """

    def __init__(
        self,
        obj: Any,
        db_attribute_key: str,
        db_attribute_category: Optional[str] = None,
        default_data: dict = None,
    ) -> None:
        if default_data is None:
            default_data = copy(ClothingConfig.DEFAULTS)
        super().__init__(
            obj, db_attribute_key, db_attribute_category, default_data
        )

    def all(self, exclude_covered: bool = False) -> List:
        """
        Get all clothing items currently worn.

        Args:
            exclude_covered (bool): If True, only return visible (uncovered) items.
                Defaults to False.

        Returns:
            List: List of clothing items, sorted by TYPE_ORDER.
        """
        clothes = [
            item
            for sublist in self._data.values()
            if sublist is not None
            for item in sublist
        ]

        if exclude_covered:
            clothes = [item for item in clothes if not item.covered_by]

        return sorted(
            clothes,
            key=lambda x: ClothingConfig.TYPE_ORDER.index(x.clothing_type),
        )

    def get(self, clothing_type) -> Optional[List]:
        """
        Get clothing items of a specific type.

        Args:
            clothing_type (ClothingType): The type of clothing to retrieve

        Returns:
            Optional[List]: List of items of the specified type or None if empty
        """
        return super().get(clothing_type)

    def can_wear(self, item) -> bool:
        """
        Check if an item can be worn.

        Args:
            item: The clothing item to check

        Returns:
            bool: True if the item can be worn, False otherwise
        """
        if not inherits_from(item, Clothing):
            return False
        if len(self.all()) >= ClothingConfig.OVERALL_LIMIT:
            return False
        return True

    def remove(self, item) -> bool:
        """
        Remove a clothing item from the wearer.

        Args:
            item: The clothing item to remove

        Returns:
            bool: True if item was removed, False if not found
        """
        removed = False
        for clothing_type, items in self._data.items():
            if items and item in items:
                items.remove(item)
                removed = True
                break

        if removed:
            for piece in item.covering:
                piece.covered_by.remove(item)

            for piece in item.covered_by:
                piece.covering.remove(item)

            item.covering = []
            item.covered_by = []

            self._save()

            message = f"$You() $conj(remove) {item.get_display_name(self.obj)}"
            self.obj.location.msg_contents(message + ".", from_obj=self.obj)

        return removed

    def wear(self, item) -> bool:
        """
        Add a clothing item to be worn.

        Args:
            item: The clothing item to wear

        Returns:
            bool: True if item was worn successfully, False otherwise
        """
        if not self.can_wear(item):
            self.obj.msg("You cannot wear that.")
            return False

        clothing_type = item.clothing_type

        # Update coverage relationships
        for covered_type in ClothingConfig.TYPE_COVER[clothing_type]:
            covered_items = self.get(covered_type)
            if covered_items:
                for covered_item in covered_items:
                    item.covering.append(covered_item)
                    covered_item.covered_by.append(item)

        if self._data[clothing_type] is None:
            self._data[clothing_type] = [item]
        else:
            self._data[clothing_type].append(item)

        self._save()

        message = f"$You() $conj(wear) {item.get_display_name(self.obj)}"
        self.obj.location.msg_contents(message + ".", from_obj=self.obj)
        return True

    def reset(self) -> None:
        """
        Reset all clothing slots to their default empty state.

        This removes all worn items and returns the handler to its initial state.
        """
        self._data = copy(ClothingConfig.DEFAULTS)
        self._save()
