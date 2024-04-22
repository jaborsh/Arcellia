from typeclasses import characters

from world.nautilus.interactions.levers import LeverCmdSet
from world.nautilus.mobs import EnchantressCmdSet
from world.nautilus.quest import NautilusQuest
from world.xyzgrid.xyzroom import XYZRoom


class NautilusStartRoom(XYZRoom):
    def at_object_creation(self):
        super().at_object_creation()

    def at_object_receive(self, moved_obj, source_location, move_type="move", **kwargs):
        if not isinstance(moved_obj, characters.Character):
            return

        if source_location.tags.get(
            category="room_z_coordinate"
        ) == "chargen" and not moved_obj.quests.get("Nautilus"):
            moved_obj.quests.add(NautilusQuest)


class NautilusInnerHold(XYZRoom):
    """
    The Inner Hold of the Nautilus where the Enchantress is kept.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.cmdset.add(EnchantressCmdSet, persistent=True)
        self.cmdset.add(LeverCmdSet, persistent=True)

    def at_object_receive(self, moved_obj, source_location, move_type="move", **kwargs):
        """
        Called after an object has been moved into this object.

        Args:
            moved_obj (Object): The object moved into this one
            source_location (Object): Where `moved_object` came from.
                Note that this could be `None`.
            move_type (str): The type of move. "give", "traverse", etc.
                This is an arbitrary string provided to obj.move_to().
                Useful for altering messages or altering logic depending
                on the kind of movement.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).

        """

        if not isinstance(moved_obj, characters.Character):
            return

        if moved_obj.quests.get_detail("Tutorial", "enchantress_freed"):
            return

        enchantress = moved_obj.search("enchantress", quiet=True)[0]
        enchantress.greeting()
