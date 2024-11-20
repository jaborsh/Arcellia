from handlers.stats.health_progression import HEALTH_PROGRESSION
from handlers.stats.mana_progression import MANA_PROGRESSION
from handlers.stats.stamina_progression import STAMINA_PROGRESSION
from handlers.stats.weight_progression import WEIGHT_PROGRESSION
from handlers.traits import TraitHandler


class StatHandler(TraitHandler):
    def __init__(
        self, obj, db_attribute_key="stats", db_attribute_category=None
    ):
        super().__init__(obj, db_attribute_key, db_attribute_category)

    def _init_stats(self):
        self.add("level", "Level", trait_type="counter", base=1, min=1, max=99)

        self.add("body", "Body", trait_type="counter", base=10, min=1, max=99)
        self.add("mind", "Mind", trait_type="counter", base=10, min=1, max=99)
        self.add(
            "endurance",
            "Endurance",
            trait_type="counter",
            base=1,
            min=1,
            max=99,
        )
        self.add(
            "strength", "Strength", trait_type="counter", base=1, min=0, max=99
        )
        self.add(
            "dexterity",
            "Dexterity",
            trait_type="counter",
            base=1,
            min=0,
            max=99,
        )
        self.add(
            "intelligence",
            "Intelligence",
            trait_type="counter",
            base=1,
            min=0,
            max=99,
        )
        self.add("faith", "Faith", trait_type="counter", base=1, min=0, max=99)
        self.add(
            "arcane", "Arcane", trait_type="counter", base=1, min=0, max=99
        )

        self.add(
            "health",
            "Health",
            trait_type="counter",
            base=HEALTH_PROGRESSION[self.body.current],
            min=0,
            max=HEALTH_PROGRESSION[self.body.current],
        )
        self.add(
            "mana",
            "Mana",
            trait_type="counter",
            base=MANA_PROGRESSION[self.mind.current],
            min=0,
            max=MANA_PROGRESSION[self.mind.current],
        )
        self.add(
            "stamina",
            "Stamina",
            trait_type="counter",
            base=STAMINA_PROGRESSION[self.endurance.current],
            min=0,
            max=STAMINA_PROGRESSION[self.endurance.current],
        )

        self.add(
            "experience", "Experience", trait_type="counter", base=0, min=0
        )
        self.add(
            "weight",
            "Weight",
            trait_type="counter",
            base=0,
            min=0,
            max=WEIGHT_PROGRESSION[self.endurance.current],
        )

    @property
    def level(self):
        return self.get("level")

    @property
    def body(self):
        return self.get("body")

    @property
    def mind(self):
        return self.get("mind")

    @property
    def endurance(self):
        return self.get("endurance")

    @property
    def strength(self):
        return self.get("strength")

    @property
    def dexterity(self):
        return self.get("dexterity")

    @property
    def intelligence(self):
        return self.get("intelligence")

    @property
    def faith(self):
        return self.get("faith")

    @property
    def arcane(self):
        return self.get("arcane")

    @property
    def health(self):
        return self.get("health")

    @property
    def mana(self):
        return self.get("mana")

    @property
    def stamina(self):
        return self.get("stamina")

    @property
    def experience(self):
        return self.get("experience")

    @property
    def weight(self):
        return self.get("weight")

    def at_level_body(self):
        self.body.current += 1
        self.stats.add(
            "health",
            "Health",
            trait_counter="counter",
            base=HEALTH_PROGRESSION[self.body.current],
            min=0,
            max=HEALTH_PROGRESSION[self.body.current],
        )
        self.msg("|#32CD32A warm surge of vitality fills you.|n")

    def at_level_mind(self):
        self.mind.current += 1
        self.stats.add(
            "mana",
            "Mana",
            trait_type="counter",
            base=MANA_PROGRESSION[self.mind.current],
            min=0,
            max=MANA_PROGRESSION[self.mind.current],
        )
        self.msg(
            "|#4169E1An electric energy courses through you, filling the mind.|n"
        )

    def at_level_endurance(self):
        self.endurance.current += 1
        self.stats.add(
            "stamina",
            "Stamina",
            trait_type="counter",
            base=STAMINA_PROGRESSION["stamina"][self.endurance.current],
            min=0,
            max=STAMINA_PROGRESSION["stamina"][self.endurance.current],
        )
        self.stats.add(
            "weight",
            "Weight",
            trait_type="counter",
            base=0,
            min=0,
            max=WEIGHT_PROGRESSION["weight"][self.endurance.current],
        )
        self.msg("|#FFD700A steady, invigorating force floods your muscles.|n")
        self.msg(
            "|#8B4513A grounding endurance settles within you, fortifying your frame.|n"
        )
