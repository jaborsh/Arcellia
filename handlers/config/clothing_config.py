from typing import Dict, List

from typeclasses.clothing import ClothingType


class ClothingConfig:
    """
    Configuration class for the clothing system.

    This class contains all the constant values and rules that define how
    clothing items can be worn and interact with each other.

    Attributes:
        DEFAULTS (Dict[ClothingType, None]): Default empty state for each clothing slot
        OVERALL_LIMIT (int): Maximum number of clothing items that can be worn
        TYPE_COVER (Dict[ClothingType, List[ClothingType]]): Defines which clothing types cover others
        TYPE_ORDER (List[ClothingType]): Defines the display order of clothing types
    """

    DEFAULTS: Dict[ClothingType, None] = {
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

    OVERALL_LIMIT: int = 20

    TYPE_COVER: Dict[ClothingType, List[ClothingType]] = {
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

    TYPE_ORDER: List[ClothingType] = [
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
