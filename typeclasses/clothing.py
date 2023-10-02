from enum import Enum

from evennia.utils import iter_to_str

from typeclasses.objects import Object

CLOTHING_OVERALL_LIMIT = 10


class ClothingHandler:
    """
    A class that handles the management of clothing items for a given object.

    Attributes:
        obj (Object): The object that this ClothingHandler instance is managing clothing for.
        default (dict): A dictionary containing default empty lists for each ClothingType.
    """

    def __init__(self, obj):
        self.obj = obj
        self.default = {
            ClothingType.HEADWEAR: [],
            ClothingType.EYEWEAR: [],
            ClothingType.EARRING: [],
            ClothingType.NECKWEAR: [],
            ClothingType.FULLBODY: [],
            ClothingType.UNDERSHIRT: [],
            ClothingType.TOP: [],
            ClothingType.WRISTWEAR: [],
            ClothingType.HANDWEAR: [],
            ClothingType.RING: [],
            ClothingType.BELT: [],
            ClothingType.UNDERWEAR: [],
            ClothingType.BOTTOM: [],
            ClothingType.FOOTWEAR: [],
        }

        self._load()

    # Overloading the __call__ function so that .get() is the default call.
    def __call__(self, exclude_covered=False):
        return self.get(exclude_covered=exclude_covered)

    def _load(self):
        self.clothes = self.obj.attributes.get(
            "clothes", default=self.default, category="clothes"
        )

    def _save(self):
        self.obj.attributes.add("clothes", self.clothes, category="clothes")
        self._load()

    def add(self, clothing):
        self.clothes[clothing.clothing_type].append(clothing)
        self._save()

    def get(self, exclude_covered=False):
        # Flatten the list of clothing articles
        flat_clothes = [item for sublist in self.clothes.values() for item in sublist]

        # Optionally exclude covered clothes
        if exclude_covered:
            flat_clothes = [item for item in flat_clothes if not item.covered_by]

        # Sort the clothes according to the defined order
        sorted_clothes = sorted(
            flat_clothes, key=lambda x: CLOTHING_TYPE_ORDER.index(x.clothing_type)
        )

        return sorted_clothes

    def remove(self, clothing):
        self.clothes[clothing.clothing_type].remove(clothing)
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
        super().at_object_creation()
        # self.db.clothing_type = None
        # self.db.covered_by = []

    @property
    def clothing_type(self):
        """
        Returns the clothing type of this object.
        """
        return self.attributes.get("clothing_type", None)

    @property
    def covered_by(self):
        """
        Returns a list of clothing objects that are covering this object.
        """
        return self.attributes.get("covered_by", [])

    @covered_by.setter
    def covered_by(self, value):
        value.is_typeclass(Clothing)

    def remove(self, wearer, quiet=False):
        """
        Removed worn clothes and optionally echoes to the room.

        Args:
            wearer (obj): object wearing this clothing object.
            quiet (bool): if true, don't echo to the room.
        """
        uncovered = []

        # Check to see if any other clothes are covered by this object.
        for article in wearer.clothes.get():
            if article.covered_by == self:
                article.covered_by.remove(self)
                uncovered.append(article)

        # Remove the clothes from the wearer.
        wearer.clothes.get().remove(self)

        # Echo a message to the room
        if not quiet:
            remove_message = f"$You() $conj(remove) {self.name}"
            if len(uncovered) > 0:
                remove_message += f", revealing {iter_to_str(uncovered)}"
            wearer.location.msg_contents(remove_message + ".", from_obj=wearer)

    def wear(self, wearer, wearstyle, quiet=False):
        """
        Sets clothes to be worn and optionally echoes to the room.

        Args:
            wearer (obj): object wearing the clothing article.
            wearstyle (str): the style of wear.

        Keyword Args:
            quiet (bool): if true, don't echo to the room.
        """

        wearer.clothes.add(self)

        # Auto-cover appropriately
        covering = []
        if self.clothing_type in CLOTHING_TYPE_COVER:
            wearer_clothes = wearer.clothes.get()
            for article in wearer_clothes:
                if article.clothing_type in CLOTHING_TYPE_COVER[self.clothing_type]:
                    article.covered_by.append(self)
                    covering.append(article)

        # Echo to the room.
        if not quiet:
            message = f"$You() $conj(wear) {self.name}"
            if covering:
                message += f", covering {iter_to_str(covering)}"

            wearer.location.msg_contents(message + ".", from_obj=wearer)
