from enum import Enum


class SpellDelivery(Enum):
    SELF = "self"
    TARGET = "target"
    AREA = "area"


class SpellSchool(Enum):
    ABJURATION = "abjuration"
    CONJURATION = "conjuration"
    DIVINATION = "divination"
    ENCHANTMENT = "enchantment"
    EVOCATION = "evocation"
    ILLUSION = "illusion"
    NECROMANCY = "necromancy"
    TRANSMUTATION = "transmutation"
    UNIVERSAL = "universal"


class SpellType(Enum):
    OFFENSIVE = "offensive"
    DEFENSIVE = "defensive"
    UTILITY = "utility"


class Spell:
    name = "Spell"
    desc = "A spell."
    level = 0  # maybe replace with difficulty?
    cost = 0

    school = SpellSchool.UNIVERSAL  # abjuration, conjuration, etc.
    ability = None  # int, wis, cha, etc.
    delivery = None  # target, area, etc.

    def cast(self, caster, **kwargs):
        pass
