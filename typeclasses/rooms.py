"""
Room

Rooms are simple containers that has no location of their own.

"""

from collections import defaultdict
from textwrap import dedent

from evennia.objects.objects import DefaultRoom
from evennia.utils.utils import iter_to_str, lazy_property

from handlers import combat
from world.features import racial as racial_feats

from .objects import ObjectParent
from .rooms_extended import ExtendedRoom


class Room(ExtendedRoom, ObjectParent, DefaultRoom):
    """
    Modified Extended Room (Griatch)

    Room states:
      A room state is set as a Tag with category "roomstate" and tagkey "on_fire" or "flooded"
      etc).

    Alternative descriptions:
    - Add an Attribute `desc_<roomstate>` to the room, where <roomstate> is the name of the
      roomstate to use this for, like `desc_on_fire` or `desc_flooded`. If not given, seasonal
      descriptions given in desc_spring/summer/autumn/winter will be used, and last the
      regular `desc` Attribute.

    Alternative text sections
    - Used to add alternative text sections to the room description. These are embedded in the
      description by adding `$state(roomstate, txt)`. They will show only if the room is in the
      given roomstate. These are managed via the add/remove/get_alt_text methods.

    Details:
    - This is set as an Attribute `details` (a dict) on the room, with the detail name as key.
      When looking at this room, the detail name can be used as a target to look at without having
      to add an actual database object for it. The `detail` command is used to add/remove details.

    Room messages
    - Set `room_message_rate > 0` and add a list of `room_messages`. These will be randomly
      echoed to the room at the given rate.
    """

    def at_object_creation(self):
        """
        Called when the room is created.
        """
        super().at_object_creation()
        self.add_desc("This room is dark.", "dark")

    def basetype_setup(self):
        super().basetype_setup()
        self.locks.add(
            ";".join(
                [
                    "get:false()",
                    "puppet:false()",
                    "teleport:false()",
                    "teleport_here:true()",
                ]
            )
        )  # would be weird to puppet a room ...
        self.location = None

    # populated by `return_appearance`
    appearance_template = dedent(
        """
        {name}
        
            {desc}
            
            {exits}
            
        {characters}{mobs}{things}
        """
    )

    dark_appearance_template = dedent(
        """
        {name}

            {desc}
        """
    )

    @lazy_property
    def combat(self):
        return combat.CombatHandler(self, db_attribute_key="combat")

    def get_display_desc(self, looker, **kwargs):
        """
        Evennia standard hook. Dynamically get the 'desc' component of the object description. This
        is called by the return_appearance method and in turn by the 'look' command.

        Args:
            looker (Object): Object doing the looking (unused by default).
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The desc display string.

        """
        desc = self.get_stateful_desc()
        desc = self.replace_legacy_time_of_day_markup(desc)
        desc = self._get_funcparser(looker).parse(desc, **kwargs)
        desc = (
            desc.replace("\n\n", "\n\n    ")
            .replace("|/|/", "|/|/    ")
            .lstrip()
            .rstrip()
        )
        return desc

    def get_display_exits(self, looker, **kwargs):
        """
        Get the 'exits' component of the object description, ordered as per the 'ordered_exits' list.
        Other exits not in the list are appended after the predefined ones.

        Args:
            looker (Object): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.

        Returns:
            str: The exits display data, ordered by 'ordered_exits'.
        """

        ordered_exits = [
            "north",
            "west",
            "south",
            "east",
            "northwest",
            "northeast",
            "southwest",
            "southeast",
            "up",
            "down",
        ]

        def exit_sort_key(exit):
            try:
                return ordered_exits.index(exit.display_name)
            except ValueError:
                return len(ordered_exits)

        def _filter_visible(obj_list):
            return (
                obj
                for obj in obj_list
                if obj != looker and obj.access(looker, "view")
            )

        exits = sorted(
            _filter_visible(self.contents_get(content_type="exit")),
            key=exit_sort_key,
        )
        exit_names = iter_to_str(exit.display_name for exit in exits)

        return (
            f"|wObvious Exits: {exit_names}|n"
            if exit_names
            else "|wObvious Exits: None|n"
        )

    def get_display_characters(self, looker, **kwargs):
        """
        Get the 'characters' component of the object description. Called by `return_appearance`.

        Args:
            looker (Object): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.

        Returns:
            str: The character display data.
        """

        def _filter_visible(obj_list):
            return (
                obj
                for obj in obj_list
                if obj != looker and obj.access(looker, "view")
            )

        characters = _filter_visible(
            self.contents_get(content_type="character")
        )
        character_names = iter_to_str(
            char.get_display_name(looker, **kwargs) for char in characters
        )

        return f"{character_names}\n" if character_names else ""

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
                if obj != looker and obj.access(looker, "view")
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
                if nmobs == 1
                else plural[0].upper()
                + plural[1:]
                + ",".join(
                    [
                        m.get_extra_display_name_info(looker, **kwargs)
                        for m in moblist
                    ]
                )
            )

        mob_names = "\n".join(reversed(mob_names))

        return f"{mob_names}\n\n" if mob_names else ""

    def get_display_things(self, looker, **kwargs):
        """
        Get the 'things' component of the object description. Called by `return_appearance`.

        Args:
            looker (Object): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The things display data.

        """

        def _filter_visible(obj_list):
            return (
                obj
                for obj in obj_list
                if obj != looker and obj.access(looker, "view")
            )

        # sort and handle same-named things
        things = _filter_visible(self.contents_get(content_type="object"))

        grouped_things = defaultdict(list)
        for thing in things:
            grouped_things[thing.get_display_name(looker, **kwargs)].append(
                thing
            )

        thing_names = []
        for thingname, thinglist in sorted(grouped_things.items()):
            nthings = len(thinglist)
            thing = thinglist[0]
            singular, plural = thing.get_numbered_name(
                nthings, looker, key=thingname
            )
            thing_names.append(singular if nthings == 1 else plural)
        thing_names = "\n".join(thing_names)
        return f"{thing_names}\n" if thing_names else ""

    def return_appearance(self, looker, **kwargs):
        """
        Main callback used by 'look' for the object to describe itself.
        This formats a description. By default, this looks for the `appearance_template`
        string set on this class and populates it with formatting keys
            'name', 'desc', 'exits', 'characters', 'things' as well as
            (currently empty) 'header'/'footer'. Each of these values are
            retrieved by a matching method `.get_display_*`, such as `get_display_name`,
            `get_display_footer` etc.

        Args:
            looker (Object): Object doing the looking. Passed into all helper methods.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call. This is passed into all helper methods.

        Returns:
            str: The description of this entity. By default this includes
                the entity's name, description and any contents inside it.

        Notes:
            To simply change the layout of how the object displays itself (like
            adding some line decorations or change colors of different sections),
            you can simply edit `.appearance_template`. You only need to override
            this method (and/or its helpers) if you want to change what is passed
            into the template or want the most control over output.
        """

        if not looker:
            return ""

        if not looker.permissions.check("Admin"):
            if self.tags.get(
                "dark", category="room_state"
            ) and not looker.feats.has(racial_feats.Darkvision):
                return self.return_dark_appearance(looker, **kwargs)
            elif self.tags.get(
                "magical_dark", category="room_state"
            ) and not looker.feats.has(racial_feats.SuperiorDarkvision):
                return self.return_magical_dark_appearance(looker, **kwargs)

        # populate the appearance_template string.
        return self.appearance_template.format(
            name=self.get_display_name(looker, **kwargs),
            desc=self.get_display_desc(looker, **kwargs),
            exits=self.get_display_exits(looker, **kwargs),
            characters=self.get_display_characters(looker, **kwargs),
            mobs=self.get_display_mobs(looker, **kwargs),
            things=self.get_display_things(looker, **kwargs),
        ).strip()

    def return_dark_appearance(self, looker, **kwargs):
        """
        Returns the dark appearance of the room for a given looker.

        Args:
            looker (object): The object looking at the room.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The dark appearance of the room.

        """
        if not looker:
            return ""

        # populate the dark_appearance_template string.
        return self.dark_appearance_template.format(
            name=self.get_display_name(looker, **kwargs),
            desc=self.get_display_desc(looker, **kwargs),
        ).strip()

    def return_magical_dark_appearance(self, looker, **kwargs):
        """
        Returns the appearance of the room when it is super dark.

        Args:
            looker (object): The object trying to look at the room.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The appearance of the room when it is super dark.
        """
        if not looker:
            return ""

        if looker.feats.has(racial_feats.Darkvision):
            return self.return_dark_appearance(looker, **kwargs)

        return "It is too dark to see."

    # Methods
    def brighten(self, text=None, magical=False):
        if magical and self.tags.has("magical_dark", category="room_state"):
            self.tags.remove("magical_dark", category="room_state")
        elif self.tags.has("dark", category="room_state"):
            self.tags.remove("dark", category="room_state")
        else:
            return False

        if text:
            self.msg_contents(text)

        return True

    def darken(self, text=None, magical=False):
        if magical:
            if self.tags.has("magical_dark", category="room_state"):
                return False

            if self.tags.has("dark", category="room_state"):
                self.tags.remove("dark", category="room_state")

            self.tags.add("magical_dark", category="room_state")
        elif not self.tags.has("dark", category="room_state"):
            self.tags.add("dark", category="room_state")
        else:
            return False

        if text:
            self.msg_contents(text)

        return True
