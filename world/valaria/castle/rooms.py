from evennia.utils import create
from typeclasses import rooms


class CastleRoom(rooms.XYRoom):
    """
    This is a room in the castle.
    """

    def at_init(self):
        super().at_init()
        if not self.db.mobs:
            self.db.mobs = []

        if len(self.db.mobs) < 1:
            guard = create.create_object(
                typeclass="world.valaria.castle.mobs.ValarianCastleGuard",
                key="Valarian Castle Guard",
                location=self,
            )
            self.db.mobs.append(guard)
        else:
            for mob in self.db.mobs:
                if not mob.location == self:
                    mob.move_to(self)

    def at_object_delete(self):
        for mob in self.db.mobs:
            mob.delete()

        return True
