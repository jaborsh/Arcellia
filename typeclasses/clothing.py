from evennia.utils.utils import lazy_property

from handlers.clothing.clothing_types import ClothingType
from typeclasses.objects import Object


class Clothing(Object):
    """
    Represents a piece of clothing in the game.
    """

    _content_types = (
        "clothing",
        "object",
    )

    def at_object_creation(self):
        self.db.covered_by = []
        self.db.covering = []

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

    @covered_by.setter
    def covered_by(self, value: list):
        self.db.covered_by = value

    @property
    def covering(self):
        """
        Returns a list of clothing objects that this object is covering.
        """
        return self.attributes.get("covering", [])

    @covering.setter
    def covering(self, value: list):
        self.db.covering = value

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
            ClothingType.OUTERWEAR: "over torso",
            ClothingType.FULLBODY: "on body",
            ClothingType.WRISTWEAR: "around wrists",
            ClothingType.HANDWEAR: "on hands",
            ClothingType.RING: "on finger",
            ClothingType.BELT: "around waist",
            ClothingType.UNDERWEAR: "on hips",
            ClothingType.BOTTOM: "on legs",
            ClothingType.HOSIERY: "on legs",
            ClothingType.FOOTWEAR: "on feet",
        }
        return position_map.get(self.clothing_type, "on body")

    def at_drop(self, caller):
        caller.clothing.remove(self)

    def at_give(self, caller, target):
        caller.clothing.remove(self)
