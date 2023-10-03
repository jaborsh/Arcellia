from enum import Enum

from evennia.utils import dbserialize, iter_to_str
from evennia.utils.utils import lazy_property

from typeclasses.objects import Object

CLOTHING_OVERALL_LIMIT = 15


class ClothingHandler:
    """
    A class that handles the management of clothing items for a given object.
    """

    def __init__(self, caller):
        self.caller = caller
        self.slots = {}
        self._load()

    def _load(self):
        self.slots = self.caller.attributes.get("clothes", {}, category="clothing")

    def _save(self):
        # Remove potential None values from the list.
        self.slots = {k: v for k, v in self.slots.items() if v}
        self.caller.attributes.add("clothes", self.slots, category="clothing")
        self._load()

    def all(self, exclude_covered=False):
        # Flatten the list of clothing articles
        flat_clothes = [item for sublist in self.slots.values() for item in sublist]

        # Optionally exclude covered clothes
        if exclude_covered:
            flat_clothes = [item for item in flat_clothes if not item.covered_by]

        # Sort the clothes according to the defined order
        sorted_clothes = sorted(
            flat_clothes, key=lambda x: CLOTHING_TYPE_ORDER.index(x.clothing_type)
        )

        return sorted_clothes

    def remove(self, item):
        self.slots[item.clothing_type].remove(item)
        self._save()

    def wear(self, item):
        slot = item.clothing_type

        if len(self.slots.values()) > CLOTHING_OVERALL_LIMIT:
            self.caller.msg("You cannot wear more clothes.")
            return

        if slot in self.slots:
            self.slots[slot].append(item)
        else:
            self.slots[slot] = [item]

        self._save()


class ClothingType(Enum):
    """
    Defines the type of clothing.
    """

    HEADWEAR = "headwear"
    EYEWEAR = "eyewear"
    EARRING = "earring"
    NECKWEAR = "neckwear"
    UNDERSHIRT = "undershirt"
    TOP = "top"
    FULLBODY = "fullbody"
    WRISTWEAR = "wristwear"
    HANDWEAR = "handwear"
    RING = "ring"
    BELT = "belt"
    UNDERWEAR = "underwear"
    BOTTOM = "bottom"
    FOOTWEAR = "footwear"


# Articles that are automatically concealed by their key clothing type.
CLOTHING_TYPE_COVER = {
    ClothingType.FULLBODY: [
        ClothingType.TOP,
        ClothingType.UNDERSHIRT,
        ClothingType.BELT,
        ClothingType.BOTTOM,
    ],
    ClothingType.TOP: [ClothingType.UNDERSHIRT],
    ClothingType.HANDWEAR: [ClothingType.RING],
    ClothingType.BOTTOM: [ClothingType.UNDERWEAR],
}

# The order in which clothing types appear on the description.
CLOTHING_TYPE_ORDER = [
    ClothingType.HEADWEAR,
    ClothingType.EYEWEAR,
    ClothingType.EARRING,
    ClothingType.NECKWEAR,
    ClothingType.FULLBODY,
    ClothingType.UNDERSHIRT,
    ClothingType.TOP,
    ClothingType.WRISTWEAR,
    ClothingType.HANDWEAR,
    ClothingType.RING,
    ClothingType.BELT,
    ClothingType.UNDERWEAR,
    ClothingType.BOTTOM,
    ClothingType.FOOTWEAR,
]


class Clothing(Object):
    def at_object_creation(self):
        self.owner = None
        self.db.covered_by = []

    @property
    def clothing_type(self):
        """
        Returns the clothing type of this object.
        """
        return self.attributes.get("clothing_type", None)

    @clothing_type.setter
    def clothing_type(self, value: ClothingType):
        self.db.clothing_type = value

    @property
    def covered_by(self):
        """
        Returns a list of clothing objects that are covering this object.
        """
        return self.attributes.get("covered_by", [])

    @property
    def display_name(self):
        """
        Return a potentially fanciful name
        """
        return self.attributes.get("display_name", self.key)

    @display_name.setter
    def display_name(self, value: str):
        self.db.display_name = value

    @lazy_property
    def position(self):
        """
        Returns the position of this object.
        """
        position_map = {
            ClothingType.HEADWEAR: "on head",
            ClothingType.EYEWEAR: "on eyes",
            ClothingType.EARRING: "on ears",
            ClothingType.NECKWEAR: "around neck",
            ClothingType.UNDERSHIRT: "on torso",
            ClothingType.TOP: "about torso",
            ClothingType.FULLBODY: "on body",
            ClothingType.WRISTWEAR: "around wrists",
            ClothingType.HANDWEAR: "on hands",
            ClothingType.RING: "on finger",
            ClothingType.BELT: "around waist",
            ClothingType.UNDERWEAR: "on hips",
            ClothingType.BOTTOM: "on legs",
            ClothingType.FOOTWEAR: "on feet",
        }
        return position_map.get(self.clothing_type, "on body")

    def remove(self, wearer, quiet=False):
        """
        Removed worn clothes and optionally echoes to the room.

        Args:
            wearer (obj): object wearing this clothing object.
            quiet (bool): if true, don't echo to the room.
        """
        uncovered = []

        # Check to see if any other clothes are covered by this object.
        for article in wearer.clothes.all():
            if article.covered_by == self:
                article.covered_by.remove(self)
                uncovered.append(article)

        # Remove the clothes from the wearer.
        wearer.clothes.remove(self)
        self.owner = None  # dbserialize.dbunserialize(wearer)

        # Echo a message to the room
        if not quiet:
            remove_message = f"$You() $conj(remove) {self.get_display_name(wearer)}"
            if len(uncovered) > 0:
                remove_message += f", revealing {iter_to_str(uncovered)}"
            wearer.location.msg_contents(remove_message + ".", from_obj=wearer)

    def wear(self, wearer, quiet=False):
        """
        Sets clothes to be worn and optionally echoes to the room.

        Args:
            wearer (obj): object wearing the clothing article.
            wearstyle (str): the style of wear.
            quiet (bool): if true, don't echo to the room.
        """

        wearer.clothes.wear(self)
        self.owner = dbserialize.dbserialize(wearer)

        # Auto-cover appropriately
        covering = []
        if self.clothing_type in CLOTHING_TYPE_COVER:
            wearer_clothes = wearer.clothes.all()
            for article in wearer_clothes:
                if article.clothing_type in CLOTHING_TYPE_COVER[self.clothing_type]:
                    article.covered_by.append(self)
                    covering.append(article)

        # Echo to the room.
        if not quiet:
            message = f"$You() $conj(wear) {self.get_display_name(wearer)}"
            if covering:
                message += f", covering {iter_to_str(covering)}"

            wearer.location.msg_contents(message + ".", from_obj=wearer)
