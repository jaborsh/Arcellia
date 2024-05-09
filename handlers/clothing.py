from copy import copy

from typeclasses.clothing import ClothingType

from handlers.handler import Handler

CLOTHING_DEFAULTS = {
    ClothingType.HEADWEAR: None,
    ClothingType.EYEWEAR: None,
    ClothingType.EARRING: None,
    ClothingType.NECKWEAR: None,
    ClothingType.UNDERSHIRT: None,
    ClothingType.TOP: None,
    ClothingType.OUTERWEAR: None,
    ClothingType.FULLBODY: None,
    ClothingType.WRISTWEAR: None,
    ClothingType.HANDWEAR: None,
    ClothingType.RING: None,
    ClothingType.BELT: None,
    ClothingType.UNDERWEAR: None,
    ClothingType.BOTTOM: None,
    ClothingType.HOSIERY: None,
    ClothingType.FOOTWEAR: None,
}

CLOTHING_OVERALL_LIMIT = 20

CLOTHING_TYPE_COVER = {
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

CLOTHING_TYPE_ORDER = [
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


class ClothingHandler(Handler):
    def __init__(
        self,
        obj,
        db_attribute_key,
        db_attribute_category=None,
        default_data=copy(CLOTHING_DEFAULTS),
    ):
        super().__init__(obj, db_attribute_key, db_attribute_category, default_data)

    def all(self, exclude_covered=False):
        """
        Returns a list of all clothing items in the ClothingHandler.

        Args:
            exclude_covered (bool, optional): If True, excludes clothing items that are covered by other items. Defaults to False.

        Returns:
            list: A sorted list of clothing items, sorted based on the order defined in CLOTHING_TYPE_ORDER.

        """
        clothes = [
            item
            for sublist in self._data.values()
            if sublist is not None
            for item in sublist
        ]

        if exclude_covered:
            clothes = [item for item in clothes if not item.covered_by]

        sorted_clothes = sorted(
            clothes,
            key=lambda x: CLOTHING_TYPE_ORDER.index(x.clothing_type),
        )

        return sorted_clothes

    def remove(self, item):
        """
        Removes a clothing item from the ClothingHandler.

        Args:
            item: The clothing item to be removed.

        Returns:
            None

        Raises:
            None

        Notes:
            - If the item is found in the ClothingHandler, it will be removed from the appropriate clothing type list.
            - After removing the item, the changes will be saved using the _save() method.
            - A message will be sent to the location of the game object to inform others about the removal of the item.

        Example:
            handler.remove(item)
        """
        for clothing_type, items in self._data.items():
            if item in items:
                items.remove(item)
                break

        for piece in item.covering:
            piece.covered_by.remove(self)

        for piece in item.covered_by:
            piece.covering.remove(self)

        item.covering = []
        item.covered_by = []

        self._save()

        message = f"$You() $conj(remove) {item.get_display_name(self.obj)}"
        self.obj.location.msg_contents(message + ".", from_obj=self.obj)

    def wear(self, item):
        """
        Wears a clothing item.

        Args:
            item: The clothing item to be worn.

        Returns:
            None

        Raises:
            None

        Notes:
            - Checks if the number of clothing items already worn exceeds the overall clothing limit. If it does, a message is sent to the game object informing them that they cannot wear more clothes.
            - Adds the item to the appropriate clothing type list in the ClothingHandler's data attribute.
            - Saves the changes using the _save() method.
            - Sends a message to the location of the game object to inform others about the wearing of the item.

        Example:
            handler.wear(item)
        """
        if len(self.all()) >= CLOTHING_OVERALL_LIMIT:
            self.obj.msg("You cannot wear more clothes.")
            return

        clothing_type = item.clothing_type

        if self._data[clothing_type] is None:
            self._data[clothing_type] = [item]
        else:
            self._data[clothing_type].append(item)
        self._save()

        message = f"$You() $conj(wear) {item.get_display_name(self.obj)}"
        self.obj.location.msg_contents(message + ".", from_obj=self.obj)

    def reset(self):
        self._data = self.default_data.copy()
        self._save()
