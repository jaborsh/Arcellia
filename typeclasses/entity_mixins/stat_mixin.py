from evennia.utils.utils import lazy_property

from handlers import traits


class StatMixin:
    def init_stats(self):
        # Attributes
        self.stats.add(
            "strength",
            "Strength",
            trait_type="counter",
            base=10,
            min=0,
            max=20,
        )
        self.stats.add(
            "dexterity",
            "Dexterity",
            trait_type="counter",
            base=10,
            min=0,
            max=20,
        )
        self.stats.add(
            "intelligence",
            "Intelligence",
            trait_type="counter",
            base=10,
            min=0,
            max=20,
        )
        self.stats.add(
            "faith",
            "Faith",
            trait_type="counter",
            base=10,
            min=0,
            max=20,
        )
        self.stats.add(
            "arcane",
            "Arcane",
            trait_type="counter",
            base=10,
            min=0,
            max=20,
        )
        self.stats.add(
            "charisma",
            "Charisma",
            trait_type="counter",
            base=10,
            min=0,
            max=20,
        )

        # Stats
        self.stats.add(
            "health",
            "Health",
            trait_type="gauge",
            base=100,
            min=0,
            max=100,
        )
        self.stats.add(
            "mana",
            "Mana",
            trait_type="gauge",
            base=100,
            min=0,
            max=100,
        )
        self.stats.add(
            "stamina",
            "Stamina",
            trait_type="gauge",
            base=100,
            min=0,
            max=100,
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
            max=300,
        )

    @lazy_property
    def stats(self):
        return traits.TraitHandler(self, db_attribute_key="stats")

    @property
    def strength(self):
        return self.stats.get("strength")

    @property
    def dexterity(self):
        return self.stats.get("dexterity")

    @property
    def constitution(self):
        return self.stats.get("constitution")

    @property
    def intelligence(self):
        return self.stats.get("intelligence")

    @property
    def wisdom(self):
        return self.stats.get("wisdom")

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
