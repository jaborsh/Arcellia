from evennia.utils.create import create_object


class MobBuilder:
    default_settings = {
        "key": "",
        "aliases": [],
        "name": "",
        "desc": "",
        "type": "typeclasses.mobs.Mob",
        "location": None,
        "locks": (
            "control:perm(Admin);call:false();examine:perm(Admin);"
            "delete:perm(Admin);edit:perm(Admin);view:all();"
            "search:perm(Admin);get:perm(Developer);puppet:perm(Admin);"
            "attrcreate:perm(Admin);"
        ),
        "stats": {
            "ac": 10,
            "health": 10,
            "mana": 10,
            "stamina": 10,
            "wealth": 0,
            "weight": 0,
        },
        "attributes": {
            "strength": 10,
            "dexterity": 10,
            "constitution": 10,
            "intelligence": 10,
            "wisdom": 10,
            "charisma": 10,
        },
    }

    def __init__(self):
        self.settings = self.default_settings.copy()

    def set_key(self, key):
        self.settings["key"] = key

    def set_aliases(self, aliases):
        self.settings["aliases"] = aliases

    def set_name(self, name):
        self.settings["name"] = name

    def set_desc(self, desc):
        self.settings["desc"] = desc

    def set_type(self, type):
        self.settings["type"] = type

    def set_location(self, location):
        self.settings["location"] = location

    def set_stats(self, ac, health, mana, stamina):
        self.settings["stats"]["ac"] = ac
        self.settings["stats"]["health"] = health
        self.settings["stats"]["mana"] = mana
        self.settings["stats"]["stamina"] = stamina

    def set_armor(self, armor):
        self.settings["stats"]["armor"] = armor

    def set_health(self, health):
        self.settings["stats"]["health"] = health

    def set_mana(self, mana):
        self.settings["stats"]["mana"] = mana

    def set_stamina(self, stamina):
        self.settings["stats"]["stamina"] = stamina

    def set_wealth(self, wealth):
        self.settings["stats"]["wealth"] = wealth

    def set_weight(self, weight):
        self.settings["stats"]["weight"] = weight

    def set_attributes(
        self, strength, dexterity, constitution, intelligence, wisdom, charisma
    ):
        self.settings["attributes"]["strength"] = strength
        self.settings["attributes"]["dexterity"] = dexterity
        self.settings["attributes"]["constitution"] = constitution
        self.settings["attributes"]["intelligence"] = intelligence
        self.settings["attributes"]["wisdom"] = wisdom
        self.settings["attributes"]["charisma"] = charisma

    def set_strength(self, strength):
        self.settings["attributes"]["strength"] = strength

    def set_dexterity(self, dexterity):
        self.settings["attributes"]["dexterity"] = dexterity

    def set_constitution(self, constitution):
        self.settings["attributes"]["constitution"] = constitution

    def set_intelligence(self, intelligence):
        self.settings["attributes"]["intelligence"] = intelligence

    def set_wisdom(self, wisdom):
        self.settings["attributes"]["wisdom"] = wisdom

    def set_charisma(self, charisma):
        self.settings["attributes"]["charisma"] = charisma

    def build(self):
        mob = create_object(
            typeclass=self.settings["type"],
            key="Test",  # self.settings["key"],
            location=self.settings["location"],
            home=self.settings["location"],
            locks=self.settings["locks"],
        )

        mob.stats.add(
            "ac", "Armor Class", trait_type="static", base=self.settings["stats"]["ac"]
        )
        mob.stats.add(
            "health",
            "Health",
            trait_type="static",
            base=self.settings["stats"]["health"],
        )
        mob.stats.add(
            "mana", "Mana", trait_type="static", base=self.settings["stats"]["mana"]
        )
        mob.stats.add(
            "stamina",
            "Stamina",
            trait_type="static",
            base=self.settings["stats"]["stamina"],
        )
        mob.stats.add(
            "wealth",
            "Wealth",
            trait_type="static",
            base=self.settings["stats"]["wealth"],
        )
        mob.stats.add(
            "weight",
            "Weight",
            trait_type="static",
            base=self.settings["stats"]["weight"],
        )

        mob.stats.add(
            "strength",
            "Strength",
            trait_type="static",
            base=self.settings["attributes"]["strength"],
        )
        mob.stats.add(
            "dexterity",
            "Dexterity",
            trait_type="static",
            base=self.settings["attributes"]["dexterity"],
        )
        mob.stats.add(
            "constitution",
            "Constitution",
            trait_type="static",
            base=self.settings["attributes"]["constitution"],
        )
        mob.stats.add(
            "intelligence",
            "Intelligence",
            trait_type="static",
            base=self.settings["attributes"]["intelligence"],
        )
        mob.stats.add(
            "wisdom",
            "Wisdom",
            trait_type="static",
            base=self.settings["attributes"]["wisdom"],
        )
        mob.stats.add(
            "charisma",
            "Charisma",
            trait_type="static",
            base=self.settings["attributes"]["charisma"],
        )

        return mob
