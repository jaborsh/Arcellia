from typeclasses.clothing import CLOTHING_OVERALL_LIMIT, CLOTHING_TYPE_ORDER


class ClothingHandler:
    """
    A class that handles the management of clothing items for a given object.
    """

    def __init__(self, caller):
        self.caller = caller
        self.clothes = self.caller.attributes.get("clothes", category="clothing")
        if not self.clothes:
            self.caller.attributes.add("clothes", [], category="clothing")
            self.clothes = self.caller.attributes.get("clothes", category="clothing")

        # Remove potentially invalid clothing items
        for item in self.clothes:
            if not item:
                self.clothes.remove(item)

    def all(self, exclude_covered=False):
        # Optionally exclude covered clothes
        clothes = self.clothes
        if exclude_covered:
            clothes = [item for item in self.clothes if not item.covered_by]

        # Sort the clothes according to the defined order, accounting for potential None values
        sorted_clothes = sorted(
            [item for item in clothes if item is not None],
            key=lambda x: CLOTHING_TYPE_ORDER.index(x.clothing_type),
        )

        return sorted_clothes

    def remove(self, item):
        self.clothes.remove(item)

    def wear(self, item):
        if len(self.clothes) > CLOTHING_OVERALL_LIMIT:
            self.caller.msg("You cannot wear more clothes.")
            return

        self.clothes.append(item)