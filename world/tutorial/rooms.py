from typeclasses import rooms

from evennia.utils.create import create_object


class NautilusRoom(rooms.XYRoom):
    """
    This is a Tutorial room.
    """


class NautilusMapRoom(NautilusRoom):
    """
    This is the Map Room with the open-skull body. When you interact with the
    person in the chair, your character may notice that the exposed brain is
    not, in fact, the person's own brain, but rather an abberation that has
    taken to feeding on the person.
    """

    def at_object_creation(self):
        self.db.interaction = "world.tutorial.interactions.nautilus_brain"
        self.initialize_objects()

    def initialize_objects(self):
        create_object(
            typeclass="world.tutorial.objects.ScalplessPerson",
            key="person",
            location=self,
            home=self,
            aliases=["corpse", "body"],
        )
