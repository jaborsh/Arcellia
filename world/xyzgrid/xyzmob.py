# from typeclasses.mobs import Mob as DefaultMob


# class XYZMob(DefaultMob):
#     pass

from evennia.utils.create import create_object

from world.xyzgrid.xyzroom import (
    MAP_X_TAG_CATEGORY,
    MAP_Y_TAG_CATEGORY,
    MAP_Z_TAG_CATEGORY,
)


class XYZMobBuilder:
    default_settings = {
        "key": "",
        "name": "",
        "aliases": [],
        "desc": "",
        "typeclass": "typeclasses.mobs.Mob",
        "prototype": None,
        "location": None,
        "tags": None,
        "xyz": None,
        "locks": (
            "control:perm(Admin);call:false();examine:perm(Admin);"
            "delete:perm(Admin);edit:perm(Admin);view:all();"
            "search:perm(Admin);get:perm(Developer);puppet:perm(Admin);"
            "attrcreate:perm(Admin);"
        ),
        "senses": {
            "feel": "",
            "smell": "",
            "sound": "",
            "taste": "",
        },
        "stats": {
            # Attributes
            "strength": 10,
            "dexterity": 10,
            "constitution": 10,
            "intelligence": 10,
            "wisdom": 10,
            "charisma": 10,
            # Stats (add ac eventually?)
            "health": 10,
            "mana": 10,
            "stamina": 10,
            "wealth": 0,
            "weight": 0,
        },
        "quantity": 1,
    }

    def __init__(self):
        self.settings = self.default_settings.copy()

    def set(self, key, value):
        if (
            key not in self.settings
            and key not in self.settings["senses"]
            and key not in self.settings["stats"]
        ):
            raise ValueError(f"Invalid key: {key}")

        if key in self.settings["senses"]:
            self.settings["senses"][key] = value
        elif key in self.settings["stats"]:
            self.settings["stats"][key] = value
        else:
            self.settings[key] = value

    def set_xyz(self, xyz):
        x, y, z = xyz
        tags = (
            (str(x), MAP_X_TAG_CATEGORY),
            (str(y), MAP_Y_TAG_CATEGORY),
            (str(z), MAP_Z_TAG_CATEGORY),
        )

        self.settings["xyz"] = tags

    def build(self):
        mobs = []
        for _ in range(self.settings["quantity"]):
            mob = create_object(
                typeclass=self.settings["typeclass"],
                key=self.settings["key"],
                location=self.settings["location"],
                tags=self.settings["xyz"],
                locks=self.settings["locks"],
            )

            mob.db.desc = self.settings["desc"]
            mob.display_name = self.settings["name"]
            for key, value in self.settings["stats"].items():
                if key in ["health", "mana", "stamina"]:
                    mob.stats.add(
                        key,
                        key.capitalize(),
                        trait_type="counter",
                        base=value,
                        max=value,
                    )
                else:
                    mob.stats.add(
                        key, key.capitalize(), trait_type="static", base=value
                    )
            mob.tags.add(self.settings["prototype"])
            mob.tags.add(self.settings["tags"])

            mobs.append(mob)
        return mobs

    def reset(self):
        self.settings = self.default_settings.copy()
