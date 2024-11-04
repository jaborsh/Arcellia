from evennia.utils.utils import lazy_property

from handlers import buffs, traits
from typeclasses.equipment.equipment import Equipment, EquipmentType

# Constants for trait configuration
POWER_TRAITS = {
    "physical": "Physical",
    "magic": "Magic",
    "fire": "Fire",
    "lightning": "Lightning",
    "holy": "Holy",
}

STAT_TRAITS = {
    "strength": "Strength",
    "dexterity": "Dexterity",
    "intelligence": "Intelligence",
    "faith": "Faith",
    "arcane": "Arcane",
}


class Weapon(Equipment):
    """
    Represents a weapon in the game.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.attributes.add("equipment_type", EquipmentType.WEAPON)

        self.setup_power()
        self.setup_scaling()
        self.setup_requirements()

    def at_object_post_spawn(self):
        super().at_object_post_spawn()
        attributes = {
            "powers": ("power", " Power"),
            "scale": ("scaling", " Scaling"),
            "reqs": ("requirements", " Requirement"),
        }

        for attr_key, (handler_name, suffix) in attributes.items():
            items = self.attributes.get(attr_key, {})
            handler = getattr(self, handler_name)
            for key, value in items.items():
                handler.add(
                    key,
                    f"{key.capitalize()}{suffix}",
                    trait_type="static",
                    base=value,
                )
            self.attributes.remove(attr_key)

    def _setup_traits(self, handler, traits_dict, suffix=""):
        """Helper method to set up traits in bulk."""
        for key, name in traits_dict.items():
            full_name = f"{name}{suffix}" if suffix else name
            handler.add(key, full_name, trait_type="static", base=0)

    def setup_power(self):
        self._setup_traits(self.power, POWER_TRAITS, " Power")

    def setup_scaling(self):
        self._setup_traits(self.scaling, STAT_TRAITS, " Scaling")

    def setup_requirements(self):
        self._setup_traits(self.requirements, STAT_TRAITS, " Requirement")

    @lazy_property
    def power(self):
        return traits.TraitHandler(self, db_attribute_key="power")

    @lazy_property
    def requirements(self):
        return traits.TraitHandler(self, db_attribute_key="requirements")

    @lazy_property
    def scaling(self):
        return traits.TraitHandler(self, db_attribute_key="scaling")

    @lazy_property
    def upgrades(self):
        return buffs.BuffHandler(self, db_attribute_key="upgrades")

    @property
    def damage(self):
        return self.power.get("physical").value

    # damage = base_ap + (stat * scale [all attrs])
