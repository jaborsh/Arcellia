from evennia.utils.utils import lazy_property

from handlers import traits
from world.characters.stats import (
    BODY_PROGRESSION,
    ENDURANCE_PROGRESSION,
    MIND_PROGRESSION,
)


class StatMixin:
    def init_stats(self):
        # Attributes
        self.stats.add(
            "body", "Body", trait_type="counter", base=10, min=1, max=99
        )
        self.stats.add(
            "mind", "Mind", trait_type="counter", base=10, min=1, max=99
        )
        self.stats.add(
            "endurance",
            "Endurance",
            trait_type="counter",
            base=1,
            min=1,
            max=99,
        )
        self.stats.add(
            "strength",
            "Strength",
            trait_type="counter",
            base=1,
            min=0,
            max=99,
        )
        self.stats.add(
            "dexterity",
            "Dexterity",
            trait_type="counter",
            base=1,
            min=0,
            max=99,
        )
        self.stats.add(
            "intelligence",
            "Intelligence",
            trait_type="counter",
            base=1,
            min=0,
            max=99,
        )
        self.stats.add(
            "faith",
            "Faith",
            trait_type="counter",
            base=1,
            min=0,
            max=99,
        )
        self.stats.add(
            "arcane",
            "Arcane",
            trait_type="counter",
            base=1,
            min=0,
            max=99,
        )
        self.stats.add(
            "charisma",
            "Charisma",
            trait_type="counter",
            base=1,
            min=0,
            max=99,
        )

        # Stats
        self.stats.add(
            "health",
            "Health",
            trait_type="gauge",
            base=BODY_PROGRESSION[self.stats.get("body").current],
            min=0,
            max=BODY_PROGRESSION[self.stats.get("body").current],
        )
        self.stats.add(
            "mana",
            "Mana",
            trait_type="gauge",
            base=MIND_PROGRESSION[self.stats.get("mind").current],
            min=0,
            max=MIND_PROGRESSION[self.stats.get("mind").current],
        )
        self.stats.add(
            "stamina",
            "Stamina",
            trait_type="gauge",
            base=ENDURANCE_PROGRESSION["stamina"][
                self.stats.get("endurance").current
            ],
            min=0,
            max=ENDURANCE_PROGRESSION["stamina"][
                self.stats.get("endurance").current
            ],
        )

        # Misc.
        self.stats.add("level", "Level", trait_type="counter", base=1, min=1)
        self.stats.add(
            "experience", "Experience", trait_type="counter", base=0, min=0
        )
        self.stats.add("wealth", "Wealth", trait_type="counter", base=0, min=0)
        self.stats.add(
            "weight",
            "Weight",
            trait_type="counter",
            base=0,
            min=0,
            max=ENDURANCE_PROGRESSION["weight"][
                self.stats.get("endurance").current
            ],
        )

    @lazy_property
    def stats(self):
        return traits.TraitHandler(self, db_attribute_key="stats")

    @property
    def body(self):
        return self.stats.get("body")

    @property
    def mind(self):
        return self.stats.get("mind")

    @property
    def endurance(self):
        return self.stats.get("endurance")

    @property
    def strength(self):
        return self.stats.get("strength")

    @property
    def dexterity(self):
        return self.stats.get("dexterity")

    @property
    def intelligence(self):
        return self.stats.get("intelligence")

    @property
    def faith(self):
        return self.stats.get("faith")

    @property
    def arcane(self):
        return self.stats.get("arcane")

    @property
    def charisma(self):
        return self.stats.get("charisma")

    @property
    def health(self):
        return self.stats.get("health")

    @property
    def mana(self):
        return self.stats.get("mana")

    @property
    def stamina(self):
        return self.stats.get("stamina")

    @property
    def level(self):
        return self.stats.get("level")

    @property
    def experience(self):
        return self.stats.get("experience")

    @property
    def wealth(self):
        return self.stats.get("wealth")

    @property
    def weight(self):
        self.stats.get("weight").current = sum(
            [o.db.weight or 0 for o in self.contents]
        )
        return self.stats.get("weight")

    def at_level_body(self):
        self.body.current += 1
        self.stats.add(
            "health",
            "Health",
            trait_type="counter",
            base=BODY_PROGRESSION[self.body.current],
            min=0,
            max=BODY_PROGRESSION[self.body.current],
        )
        self.msg("|#32CD32A warm surge of vitality fills you.|n")

    def at_level_mind(self):
        self.mind.current += 1
        self.stats.add(
            "mana",
            "Mana",
            trait_type="counter",
            base=MIND_PROGRESSION[self.mind.current],
            min=0,
            max=MIND_PROGRESSION[self.mind.current],
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
            base=ENDURANCE_PROGRESSION["stamina"][self.endurance.current],
            min=0,
            max=ENDURANCE_PROGRESSION["stamina"][self.endurance.current],
        )
        self.stats.add(
            "weight",
            "Weight",
            trait_type="counter",
            base=0,
            min=0,
            max=ENDURANCE_PROGRESSION["weight"][self.endurance.current],
        )
        self.msg("|#FFD700A steady, invigorating force floods your muscles.|n")
        self.msg(
            "|#8B4513A grounding endurance settles within you, fortifying your frame.|n"
        )
