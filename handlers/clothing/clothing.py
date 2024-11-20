from copy import copy

from evennia.utils import dbserialize
from evennia.utils.utils import inherits_from

from handlers.clothing.clothing_types import ClothingType
from typeclasses.clothing import Clothing

CLOTHING_DEFAULTS = {
    ClothingType.HEADWEAR: [],
    ClothingType.EYEWEAR: [],
    ClothingType.EARRING: [],
    ClothingType.NECKWEAR: [],
    ClothingType.UNDERSHIRT: [],
    ClothingType.TOP: [],
    ClothingType.OUTERWEAR: [],
    ClothingType.FULLBODY: [],
    ClothingType.WRISTWEAR: [],
    ClothingType.HANDWEAR: [],
    ClothingType.RING: [],
    ClothingType.BELT: [],
    ClothingType.UNDERWEAR: [],
    ClothingType.BOTTOM: [],
    ClothingType.HOSIERY: [],
    ClothingType.FOOTWEAR: [],
}

CLOTHING_COVER = {
    ClothingType.HEADWEAR: [],
    ClothingType.EYEWEAR: [],
    ClothingType.EARRING: [],
    ClothingType.NECKWEAR: [],
    ClothingType.UNDERSHIRT: [],
    ClothingType.TOP: [ClothingType.UNDERSHIRT],
    ClothingType.OUTERWEAR: [ClothingType.TOP],
    ClothingType.FULLBODY: [
        ClothingType.TOP,
        ClothingType.UNDERSHIRT,
        ClothingType.BELT,
        ClothingType.BOTTOM,
    ],
    ClothingType.WRISTWEAR: [],
    ClothingType.HANDWEAR: [ClothingType.RING],
    ClothingType.RING: [],
    ClothingType.BELT: [],
    ClothingType.UNDERWEAR: [],
    ClothingType.BOTTOM: [ClothingType.UNDERWEAR],
    ClothingType.HOSIERY: [],
    ClothingType.FOOTWEAR: [ClothingType.HOSIERY],
}

CLOTHING_ORDER = [
    ClothingType.HEADWEAR,
    ClothingType.EYEWEAR,
    ClothingType.EARRING,
    ClothingType.NECKWEAR,
    ClothingType.OUTERWEAR,
    ClothingType.UNDERSHIRT,
    ClothingType.TOP,
    ClothingType.FULLBODY,
    ClothingType.WRISTWEAR,
    ClothingType.HANDWEAR,
    ClothingType.RING,
    ClothingType.BELT,
    ClothingType.UNDERWEAR,
    ClothingType.BOTTOM,
    ClothingType.HOSIERY,
    ClothingType.FOOTWEAR,
]

CLOTHING_LIMIT = 20


class ClothingHandler:
    """Handler for managing clothing items on a character or object."""

    def __init__(self, obj, db_attribute="clothing", db_category=None):
        self.obj = obj
        self._db_attribute = db_attribute
        self._db_category = db_category
        self._clothing = copy(CLOTHING_DEFAULTS)
        self._load()

    # Core Data Management Methods
    def _load(self):
        """Load clothing data from object attributes."""
        loaded_data = self.obj.attributes.get(
            self._db_attribute, copy(CLOTHING_DEFAULTS)
        )
        self._clothing = dbserialize.deserialize(loaded_data)

    def _save(self):
        """Save clothing data to object attributes."""
        self.obj.attributes.add(
            self._db_attribute,
            self._clothing,
            category=self._db_category,
        )

    # Query/Getter Methods
    def all(self, exclude_covered=False):
        """Get all clothing items currently worn.

        Args:
            exclude_covered: If True, only return visible (uncovered) items.

        Returns:
            List of clothing items, sorted by CLOTHING_ORDER.
        """
        clothes = [
            item
            for items in self._clothing.values()
            if items is not None
            for item in items
        ]

        if exclude_covered:
            clothes = [item for item in clothes if not item.covered_by]

        return sorted(
            clothes, key=lambda x: CLOTHING_ORDER.index(x.clothing_type)
        )

    def get(self, clothing_type):
        """Get clothing items of a specific type.

        Args:
            clothing_type: The type of clothing to retrieve

        Returns:
            List of items of the specified type or None if empty
        """
        return self._clothing.get(clothing_type)

    # Validation Methods
    def can_wear(self, item):
        """Check if an item can be worn.

        Args:
            item: The clothing item to check

        Returns:
            True if the item can be worn, False otherwise
        """
        return (
            inherits_from(item, Clothing) and len(self.all()) < CLOTHING_LIMIT
        )

    # Action Methods
    def wear(self, item):
        """Add a clothing item to be worn.

        Args:
            item: The clothing item to wear

        Returns:
            True if item was worn successfully, False otherwise
        """
        if not self.can_wear(item):
            self.obj.msg("You cannot wear that.")
            return False

        clothing_type = item.clothing_type

        # Update coverage relationships
        for covered_type in CLOTHING_COVER.get(clothing_type, []):
            covered_items = self.get(covered_type)
            if covered_items:
                for covered_item in covered_items:
                    item.covering.append(covered_item)
                    covered_item.covered_by.append(item)

        self._clothing[clothing_type].append(item)
        self._save()

        message = f"$You() $conj(wear) {item.get_display_name(self.obj)}"
        self.obj.location.msg_contents(message + ".", from_obj=self.obj)
        return True

    def remove(self, item):
        """Remove a clothing item from the wearer.

        Args:
            item: The clothing item to remove

        Returns:
            True if item was removed, False if not found
        """
        removed = False
        for clothing_type, items in self._clothing.items():
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

    def reset(self):
        """Reset all clothing slots to their default empty state."""
        self._clothing = copy(CLOTHING_DEFAULTS)
        self._save()
