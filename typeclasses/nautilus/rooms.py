from world.nautilus.interactions.levers import LeverCmdSet
from world.xyzgrid.xyzroom import XYZRoom

from typeclasses import characters


class NautilusInnerHold(XYZRoom):
    """
    The Inner Hold of the Nautilus where the Enchantress is kept.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.cmdset.add_default(LeverCmdSet)

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

        if moved_obj.quests.get_detail("Tutorial", "enchantress"):
            return

        enchantress = moved_obj.search("enchantress", quiet=True)[0]
        enchantress.greeting()