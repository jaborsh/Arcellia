from collections import defaultdict

from typeclasses import characters

from world.nautilus.interactions.levers import LeverCmdSet
from world.nautilus.mobs import EnchantressCmdSet
from world.nautilus.quest import NautilusObjective, NautilusQuest
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

        if moved_obj.quests.get_objective_completed(
            "Nautilus", NautilusObjective.FREE_ENCHANTRESS
        ):
            return

        enchantress = moved_obj.search("enchantress", quiet=True)[0]
        enchantress.greeting()

    def get_display_mobs(self, looker, **kwargs):
        """
        Get the 'mobs' component of the object description. Called by `return_appearance`.

        Args:
            looker (Object): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.

        Returns:
            str: The character display data.
        """

        def _filter_visible(obj_list):
            return [
                obj
                for obj in obj_list
                if obj != looker
                and obj.access(looker, "view")
                and not looker.quests.get_objective_failed(
                    "Nautilus", NautilusObjective.FREE_ENCHANTRESS
                )
            ]

        mobs = _filter_visible(self.contents_get(content_type="mob"))

        # Convert the mobs array into a dictionary of mobs where mobs with the same key
        # are grouped together and given a count number.
        grouped_mobs = defaultdict(list)
        for mob in mobs:
            grouped_mobs[mob.get_display_name(looker, **kwargs)].append(mob)

        mob_names = []
        for mobname, moblist in sorted(grouped_mobs.items()):
            nmobs = len(moblist)
            mob = moblist[0]
            singular, plural = mob.get_numbered_name(nmobs, looker, key=mobname)
            mob_names.append(
                mob.get_display_name(looker, **kwargs)
                + mob.get_extra_display_name_info(looker, **kwargs)
                if nmobs == 1
                else plural[0].upper()
                + plural[1:]
                + ",".join(
                    [m.get_extra_display_name_info(looker, **kwargs) for m in moblist]
                )
            )

        mob_names = "\n".join(reversed(mob_names))

        return f"{mob_names}\n\n" if mob_names else ""
