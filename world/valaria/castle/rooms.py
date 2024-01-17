from evennia.utils import create
from typeclasses import rooms


class CastleValariaRoom(rooms.XYRoom):
    """
    This is a room in the castle.
    """

    def at_init(self):
        super().at_init()
        if not self.db.mobs:
            self.db.mobs = []
            self.initialize_mobs()
        else:
            self.update_mob_locations()

    def initialize_mobs(self):
        self.add_guards()

    def update_mob_locations(self):
        for mob in self.db.mobs:
            if mob.location != self:
                mob.move_to(self, quiet=True)

    def create_mobs(self, typeclass, key, aliases=[], count=1):
        for _ in range(count):
            mob = create.create_object(typeclass=typeclass, key=key, aliases=aliases)
            mob.location = self
            mob.home = self
            self.db.mobs.append(mob)

    def add_guards(self, count=1):
        self.create_mobs(
            "typeclasses.valaria.castle.mobs.CastleValariaGuard",
            "Valarian Castle Guard",
            count=count,
        )


class CastleValariaThroneRoom(CastleValariaRoom):
    def initialize_mobs(self):
        self.create_mobs(
            "typeclasses.valaria.castle.mobs.QueenEveline",
            "Queen Eveline",
            ["queen", "eveline"],
        )
        # self.create_mobs(
        #    "typeclasses.valaria.castle.mobs.IsoldeNightshade",
        #    "Isolde Nightshade",
        #    ["isolde", "nightshade"],
        # )
        self.add_guards(count=2)


class CastleValariaStudy(CastleValariaRoom):
    def initialize_mobs(self):
        return
        self.create_mobs(
            "typeclasses.valaria.castle.mobs.CedricSterling",
            "Cedric Sterling",
            ["cedric", "sterling"],
        )


class CastleValariaRoundtable(CastleValariaRoom):
    def initialize_mobs(self):
        return
        self.create_mobs(
            "typeclasses.valaria.castle.mobs.SeraphinaLightbringer",
            "Seraphina Lightbringer",
            ["seraphina", "lightbringer"],
        )
        self.create_mobs(
            "typeclasses.valaria.castle.mobs.ReginaldArundel",
            "Reginald Arundel",
            ["reginald", "arundel"],
        )
        self.create_mobs(
            "typeclasses.valaria.castle.mobs.AriaWhisperwind",
            "Aria Whisperwind",
            ["aria", "whisperwind"],
        )
        self.create_mobs(
            "typeclasses.valaria.castle.mobs.EzekielGrimblade",
            "Ezekiel Grimblade",
            ["ezekiel", "grimblade"],
        )
        self.create_mobs(
            "typeclasses.valaria.castle.mobs.EldricShadowweaver",
            "Eldric Shadowweaver",
            ["eldric", "shadowweaver"],
        )


class CastleValariaArmory(CastleValariaRoom):
    def initialize_mobs(self):
        return
        self.create_mobs(
            "typeclasses.valaria.castle.mobs.ThornIronforge",
            "Thorn Ironforge",
            ["thorn", "ironforge"],
        )


class CastleValariaRoyalBedchamber(CastleValariaRoom):
    def initialize_mobs(self):
        return
        self.create_mobs(
            "typeclasses.valaria.castle.mobs.EvelynGraceworn",
            "Evelyn Graceworn",
            ["evelyn", "graceworn"],
        )


class CastleValariaUpperEasternWing(CastleValariaRoom):
    def initialize_mobs(self):
        return
        self.create_mobs(
            "typeclasses.valaria.castle.mobs.SilasShadowsteel",
            "Silas Shadowsteel",
            ["silas", "shadowsteel"],
        )
        self.create_mobs(
            "typeclasses.valaria.castle.mobs.LoreleiStormrider",
            "Lorelei Stormrider",
            ["lorelei", "stormrider"],
        )


class CastleValariaLibrary(CastleValariaRoom):
    def initialize_mobs(self):
        return
        self.create_mobs(
            "typeclasses.valaria.castle.mobs.BrynnMarketwell",
            "Brynn Marketwell",
            ["brynn", "marketwell"],
        )
        self.create_mobs(
            "typeclasses.valaria.castle.mobs.SableBlackthorn",
            "Sable Blackthorn",
            ["sable", "blackthorn"],
        )
