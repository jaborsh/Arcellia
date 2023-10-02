"""
Clothing - Provides a typeclass and commands for wearable clothing,
which is appended to a character's description when worn.

Evennia contribution - Tim Ashley Jenkins 2017
Modifications - Jake 2023
"""

from evennia.utils import iter_to_str

from typeclasses.objects import Object

CLOTHING_OVERALL_LIMIT = 10

CLOTHING_TYPE_AUTOCOVER = (
    {
        "top": ["undershirt"],
        "bottom": ["underwear"],
        "fullbody": ["undershirt", "underwear"],
        "gloves": ["ring"],
        "shoes": ["socks"],
    },
)

# The order in which clothing types appear on the description. Untyped clothing or clothing
# with a type not given in this list goes last.
CLOTHING_TYPE_ORDER = [
    "hat",
    "necklace",
    "earrings",
    "top",
    "undershirt",
    "bracelet",
    "fullbody",
    "gloves",
    "ring",
    "bottom",
    "underwear",
    "socks",
    "shoes",
]

CLOTHING_TYPE_SUBCATEGORIES = {
    "top": [
        "blouse",
        "jacket",
        "shirt",
        "sweater",
        "tanktop",
        "buttonup",
        "sweatshirt",
        "vest",
    ],
    "fullbody": ["suit", "outerwear", "jumpsuit", "dress", "robe"],
    "bottom": ["pants", "skirt", "shorts"],
    "shoes": [
        "sandals",
        "flats",
        "loafers",
        "slippers",
        "heels",
        "wedges",
        "sneakers",
        "boots",
    ],
}

WEARSTYLE_MAXLENGTH = 50


# HELPER FUNCTIONS START HERE
def get_worn_clothes(character, exclude_covered=False):
    """
    Get a list of clothes worn by a given character.

    Args:
        character (obj): The character to get a list of worn clothes from.

    Keyword Args:
        exclude_covered (bool): If True, excludes clothes covered by other
                                clothing from the returned list.

    Returns:
        ordered_clothes_list (list): A list of clothing items worn by the
                                     given character, ordered according to
                                     the CLOTHING_TYPE_ORDER option specified
                                     in this module.
    """
    clothes_list = []
    for thing in character.contents:
        # If uncovered or not excluding covered items
        if not thing.db.covered_by or exclude_covered is False:
            # If 'worn' is True, add to the list
            if thing.db.worn:
                clothes_list.append(thing)
    # Might as well put them in order here too.
    ordered_clothes_list = order_clothes_list(clothes_list)
    return ordered_clothes_list


def order_clothes_list(clothes_list):
    """
    Orders a given clothes list by the order specified in CLOTHING_TYPE_ORDER.

    Args:
        clothes_list (list): List of clothing items to put in order

    Returns:
        ordered_clothes_list (list): The same list as passed, but re-ordered
                                     according to the hierarchy of clothing types
                                     specified in CLOTHING_TYPE_ORDER.
    """
    ordered_clothes_list = clothes_list
    # For each type of clothing that exists...
    for current_type in reversed(CLOTHING_TYPE_ORDER):
        # Check each item in the given clothes list.
        for clothes in clothes_list:
            # If the item has a clothing type...
            if clothes.db.clothing_type:
                item_type = clothes.db.clothing_type
                # And the clothing type matches the current type...
                if item_type == current_type:
                    # Move it to the front of the list!
                    ordered_clothes_list.remove(clothes)
                    ordered_clothes_list.insert(0, clothes)
    return ordered_clothes_list


class Clothing(Object):
    @property
    def worn(self):
        return self.db.worn

    @worn.setter
    def worn(self, value: bool):
        self.db.worn = value

    @property
    def covered_by(self):
        return self.db.covered_by

    @covered_by.setter
    def covered_by(self, value):
        self.db.covered_by = value

    def at_get(self, getter):
        """
        Called when this object has just been picked up by
        someone.
        """
        self.worn = False

    def at_pre_move(self, destination, **kwargs):
        """
        Called just before starting to move this object to destination.
        Returns False to abort move.
        """
        # Covered clothing cannot be removed, dropped, or relocated.
        if self.covered_by:
            return False
        return True

    def remove(self, wearer, quiet=False):
        """
        Removes worn clothes and optionally echoes to the room.

        Args:
            wearer (obj): character object wearing this clothing object

        Keyword Args:
            quiet (bool): If false, does not message the room
        """
        self.worn = False
        uncovered_list = []

        # Check to see if any other clothes are covered by this object.
        for thing in wearer.contents:
            if thing.covered_by == self:
                thing.covered_by = False
                uncovered_list.append(thing.name)
        # Echo a message to the room
        if not quiet:
            remove_message = f"$You() $conj(remove) {self.name}"
            if len(uncovered_list) > 0:
                remove_message += f", revealing {iter_to_str(uncovered_list)}"
            wearer.location.msg_contents(remove_message + ".", from_obj=wearer)

    def wear(self, wearer, wearstyle, quiet=False):
        """
        Sets clothes to 'worn' and optionally echoes to the room.

        Args:
            wearer (obj): character object wearing this clothing object
            wearstyle (True or str): string describing the style of wear or True for none

        Keyword Args:
            quiet (bool): If false, does not message the room

        Notes:
            Optionally sets db.worn with a 'wearstyle' that appends a short passage to
            the end of the name  of the clothing to describe how it's worn that shows
            up in the wearer's desc - I.E. 'around his neck' or 'tied loosely around
            her waist'. If db.worn is set to 'True' then just the name will be shown.
        """
        # Set clothing as worn
        self.db.worn = wearstyle
        # Auto-cover appropriate clothing types
        to_cover = []
        if clothing_type := self.db.clothing_type:
            if autocover_types := CLOTHING_TYPE_AUTOCOVER.get(clothing_type):
                to_cover.extend(
                    [
                        garment
                        for garment in get_worn_clothes(wearer)
                        if garment.db.clothing_type in autocover_types
                    ]
                )
        for garment in to_cover:
            garment.db.covered_by = self

        # Echo a message to the room
        if not quiet:
            if isinstance(wearstyle, str):
                message = f"$You() $conj(wear) {self.name} {wearstyle}"
            else:
                message = f"$You() $conj(put) on {self.name}"
            if to_cover:
                message += f", covering {iter_to_str(to_cover)}"
            wearer.location.msg_contents(message + ".", from_obj=wearer)
