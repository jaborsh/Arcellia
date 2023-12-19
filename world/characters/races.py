from class_registry import ClassRegistry

race_registry = ClassRegistry("name")


class CharacterRace:
    pass


@race_registry.register
class Human(CharacterRace):
    name = "human"


@race_registry.register
class Elf(CharacterRace):
    name = "elf"


@race_registry.register
class HighElf(Elf):
    name = "high elf"


@race_registry.register
class NightElf(Elf):
    name = "night elf"


@race_registry.register
class WoodElf(Elf):
    name = "wood elf"


@race_registry.register
class Dwarf(CharacterRace):
    name = "dwarf"


@race_registry.register
class EmberheartDwarf(Dwarf):
    name = "emberheart dwarf"


@race_registry.register
class StoneguardDwarf(Dwarf):
    name = "stoneguard dwarf"


@race_registry.register
class IronveinDwarf(Dwarf):
    name = "ironvein dwarf"


@race_registry.register
class Gnome(CharacterRace):
    name = "gnome"


@race_registry.register
class DuskGnome(Gnome):
    name = "dusk gnome"


@race_registry.register
class HearthGnome(Gnome):
    name = "hearth gnome"


@race_registry.register
class SylvanGnome(Gnome):
    name = "sylvan gnome"


@race_registry.register
class Nymph(CharacterRace):
    name = "nymph"


@race_registry.register
class Orc(CharacterRace):
    name = "orc"


@race_registry.register
class Pyreling(CharacterRace):
    name = "pyreling"


@race_registry.register
class ArcanistPyreling(Pyreling):
    name = "arcanist pyreling"


@race_registry.register
class EmberkinPyreling(Pyreling):
    name = "emberkin pyreling"


@race_registry.register
class WarbrandPyreling(Pyreling):
    name = "warbrand pyreling"
