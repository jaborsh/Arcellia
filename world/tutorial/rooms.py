from typeclasses import rooms

from evennia.utils.create import create_object


class NautilusRoom(rooms.XYRoom):
    """
    This is a Tutorial room.
    """

    def at_object_creation(self):
        self.initialize_objects()

    def initialize_objects(self):
        pass

    def initialize_mobs(self):
        pass


class NautilusBerthingSouth(NautilusRoom):
    def initialize_objects(self):
        chest = create_object(
            typeclass="world.tutorial.objects.WoodenChest",
            key="chest",
            location=self,
            home=self,
        )

        create_object(
            typeclass="world.items.miscellaneous.gems.Onyx",
            key="onyx",
            location=chest,
            home=chest,
        )


class NautilusMapRoom(NautilusRoom):
    """
    This is the Map Room with the open-skull body. When you interact with the
    person in the chair, your character may notice that the exposed brain is
    not, in fact, the person's own brain, but rather an abberation that has
    taken to feeding on the person.
    """

    def initialize_objects(self):
        create_object(
            typeclass="world.tutorial.objects.BrokenBody",
            key="body",
            location=self,
            home=self,
        )
