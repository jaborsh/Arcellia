from class_registry import ClassRegistry

background_registry = ClassRegistry("name")


class CharacterBackground:
    pass


@background_registry.register
class Adventurer(CharacterBackground):
    name = "adventurer"


@background_registry.register
class Acolyte(CharacterBackground):
    name = "acolyte"


@background_registry.register
class Charlatan(CharacterBackground):
    name = "charlatan"


@background_registry.register
class Criminal(CharacterBackground):
    name = "criminal"


@background_registry.register
class Entertainer(CharacterBackground):
    name = "entertainer"


@background_registry.register
class FolkHero(CharacterBackground):
    name = "folk hero"


@background_registry.register
class GuildArtisan(CharacterBackground):
    name = "guild artisan"


@background_registry.register
class Hermit(CharacterBackground):
    name = "hermit"


@background_registry.register
class Merchant(CharacterBackground):
    name = "merchant"


@background_registry.register
class Noble(CharacterBackground):
    name = "noble"


@background_registry.register
class Outlander(CharacterBackground):
    name = "outlander"


@background_registry.register
class Sage(CharacterBackground):
    name = "sage"


@background_registry.register
class Sailor(CharacterBackground):
    name = "sailor"


@background_registry.register
class Soldier(CharacterBackground):
    name = "soldier"


@background_registry.register
class Urchin(CharacterBackground):
    name = "urchin"
