from class_registry import ClassRegistry

class_registry = ClassRegistry("name")


class CharacterClass:
    pass


@class_registry.register
class Adventurer(CharacterClass):
    name = "adventurer"


@class_registry.register
class Cleric(CharacterClass):
    name = "cleric"


@class_registry.register
class Druid(CharacterClass):
    name = "druid"


@class_registry.register
class Hunter(CharacterClass):
    name = "hunter"


@class_registry.register
class Mage(CharacterClass):
    name = "mage"


@class_registry.register
class Merchant(CharacterClass):
    name = "merchant"


@class_registry.register
class Paladin(CharacterClass):
    name = "paladin"


@class_registry.register
class Rogue(CharacterClass):
    name = "rogue"


@class_registry.register
class Shaman(CharacterClass):
    name = "shaman"


@class_registry.register
class Warlock(CharacterClass):
    name = "warlock"


@class_registry.register
class Warrior(CharacterClass):
    name = "warrior"
