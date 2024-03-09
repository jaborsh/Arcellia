from enum import Enum

from evennia.utils.utils import lazy_property
from typeclasses.objects import Object


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
    OUTERWEAR = "outerwear"
    FULLBODY = "fullbody"
    WRISTWEAR = "wristwear"
    HANDWEAR = "handwear"
    RING = "ring"
    BELT = "belt"
    UNDERWEAR = "underwear"
    BOTTOM = "bottom"
    HOSIERY = "hosiery"
    FOOTWEAR = "footwear"


class Clothing(Object):
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
        return self.attributes.get("covering", [])

    @covering.setter
    def covering(self, value: list):
        self.db.covering = value

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

    # def remove(self, wearer):
    #     """
    #     Removed worn clothes and optionally echoes to the room.

    #     Args:
    #         wearer (obj): object wearing this clothing object.
    #         quiet (bool): if true, don't echo to the room.
    #     """
    #     uncovered = []

    #     # Check to see if any other clothes are covered by this object.
    #     for article in wearer.clothes.all():
    #         if self in article.covered_by:
    #             article.covered_by.remove(self)
    #             uncovered.append(article)

    #     # Remove the clothes from the covered_by list.
    #     self.covered_by = []

    #     # Remove the clothes from the wearer.
    #     wearer.clothes.remove(self)

    #     message = f"$You() $conj(remove) {self.get_display_name(wearer)}"
    #     if len(uncovered) > 0:
    #         message += f", revealing {', '.join([article.get_display_name(wearer) for article in uncovered])}"

    #     wearer.location.msg_contents(message + ".", from_obj=wearer)

    # def wear(self, wearer):
    #     """
    #     Sets clothes to be worn and optionally echoes to the room.

    #     Args:
    #         wearer (obj): object wearing the clothing article.
    #         wearstyle (str): the style of wear.
    #         quiet (bool): if true, don't echo to the room.
    #     """

    #     # Auto-cover appropriately
    #     covering = []
    #     wearer_clothes = wearer.clothes.all()
    #     for article in wearer_clothes:
    #         if article.clothing_type in CLOTHING_TYPE_COVER[self.clothing_type]:
    #             article.covered_by.append(self)
    #             covering.append(article)
    #         elif self.clothing_type in CLOTHING_TYPE_COVER[article.clothing_type]:
    #             self.covered_by.append(article)

    #     wearer.clothes.wear(self)

    #     message = f"$You() $conj(wear) {self.get_display_name(wearer)}"
    #     if covering:
    #         message += f", covering {', '.join([article.get_display_name(wearer) for article in covering])}"

    #     wearer.location.msg_contents(message + ".", from_obj=wearer)
