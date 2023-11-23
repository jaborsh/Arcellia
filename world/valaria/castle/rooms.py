from typeclasses import rooms


class CastleRoom(rooms.XYRoom):
    """
    This is a room in the castle.
    """

    def at_init(self):
        if not self.db.mobs:
            self.initialize_mobs()

    def initialize_mobs(self):
        if not self.db.mobs:
            self.db.mobs = []
            self.add_guards()
        else:
            self.update_mob_locations()

    def add_guards(self, count=1):
        self.db.mobs += self.create_mobs(
            typeclass="world.valaria.castle.mobs.ValarianCastleGuard",
            key="Valarian Castle Guard",
            count=count,
        )

    def update_mob_locations(self):
        for mob in self.db.mobs:
            if mob.location != self:
                mob.move_to(self)

    def at_object_delete(self):
        for mob in self.db.mobs:
            mob.delete()

        return True


class ThroneRoom(CastleRoom):
    def at_init(self):
        self.initialize_mobs()

    def initialize_mobs(self):
        if not self.db.mobs:
            self.db.mobs = []
            self.add_queen()
            self.add_guards(2)
        else:
            self.update_mob_locations()

    def add_queen(self):
        self.db.mobs += self.create_mobs(
            typeclass="world.valaria.castle.mobs.QueenEveline",
            key="Queen Eveline",
            aliases=["queen", "eveline"],
        )

    def update_mob_locations(self):
        for mob in self.db.mobs:
            if mob.location != self:
                mob.move_to(self)
