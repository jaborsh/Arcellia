from enum import Enum


class CharacterBodyType(Enum):
    PETITE = "petite"
    SLENDER = "slender"
    AVERAGE = "average"
    ATHLETIC = "athletic"
    ROBUST = "robust"


class CharacterHeight(Enum):
    SHORT = "short"
    AVERAGE = "average"
    TALL = "tall"


class CharacterEyeColor(Enum):
    AMBER = "amber"
    BLUE = "blue"
    BROWN = "brown"
    GREEN = "green"
    GREY = "grey"
    HAZEL = "hazel"

    BLACK = "black"
    COPPER = "copper"
    CRIMSON = "crimson"
    EMERALD = "emerald"
    GOLD = "gold"
    OPAL = "opal"
    ONYX = "onyx"
    RED = "red"
    SAPPHIRE = "sapphire"
    SILVER = "silver"
    VIOLET = "violet"
    WHITE = "white"


class CharacterHairColor(Enum):
    AUBURN = "auburn"
    BLACK = "black"
    BLONDE = "blonde"
    BROWN = "brown"
    GREY = "grey"
    RED = "red"
    WHITE = "white"

    BLUE = "blue"
    GREEN = "green"
    PINK = "pink"
    PURPLE = "purple"
    SILVER = "silver"
    TEAL = "teal"
    YELLOW = "yellow"


class CharacterSkinType(Enum):
    FRECKLED = "freckled"
    SCARRED = "scarred"
    WRINKLED = "wrinkled"
    UNBLEMISHED = "unblemished"


class CharacterEyeType(Enum):
    ALMOND = "almond"
    HOODED = "hooded"
    ROUND = "round"


class CharacterNoseType(Enum):
    AQUILINE = "aquiline"
    BUTTON = "button"
    FLAT = "flat"
    WIDE = "wide"


class CharacterMouthType(Enum):
    FULL = "full"
    SMALL = "small"
    THIN = "thin"
    WIDE = "wide"


class CharacterJawType(Enum):
    POINTED = "pointed"
    ROUND = "round"
    SQUARE = "square"


class CharacterEyebrowType(Enum):
    ARCHED = "arched"
    STRAIGHT = "straight"
    THICK = "thick"
    THIN = "thin"
