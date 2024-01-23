from collections import defaultdict
from textwrap import dedent

from django.conf import settings
from evennia.contrib.grid.xyzgrid import xyzroom
from evennia.objects.objects import DefaultRoom
from evennia.utils.utils import iter_to_str

from typeclasses.mixins.rooms import ExtendedRoomMixin

from .objects import Object

CLIENT_DEFAULT_WIDTH = settings.CLIENT_DEFAULT_WIDTH
MAP_X_TAG_CATEGORY = "room_x_coordinate"
MAP_Y_TAG_CATEGORY = "room_y_coordinate"
MAP_Z_TAG_CATEGORY = "room_z_coordinate"

MAP_XDEST_TAG_CATEGORY = "exit_dest_x_coordinate"
MAP_YDEST_TAG_CATEGORY = "exit_dest_y_coordinate"
MAP_ZDEST_TAG_CATEGORY = "exit_dest_z_coordinate"


class Room(ExtendedRoomMixin, DefaultRoom, Object):
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

    # populated by `return_appearance`
    appearance_template = dedent(
        """
        {name}

            {desc}

            {exits}{characters}{mobs}{things}
        """
    )

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
                obj for obj in obj_list if obj != looker and obj.access(looker, "view")
            )

        exits = sorted(
            _filter_visible(self.contents_get(content_type="exit")), key=exit_sort_key
        )
        exit_names = iter_to_str(exit.display_name for exit in exits)

        return (
            f"|wObvious Exits: {exit_names}|n\n"
            if exit_names
            else "|wObvious Exits: None|n\n"
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
                obj for obj in obj_list if obj != looker and obj.access(looker, "view")
            )

        characters = _filter_visible(self.contents_get(content_type="character"))
        character_names = iter_to_str(
            char.get_display_name(looker, **kwargs) for char in characters
        )

        return f"\n{character_names}\n" if character_names else ""

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
                obj for obj in obj_list if obj != looker and obj.access(looker, "view")
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
                else plural[0].upper() + plural[1:]
            )

        mob_names = "\n".join(reversed(mob_names))

        return mob_names

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
                obj for obj in obj_list if obj != looker and obj.access(looker, "view")
            )

        # sort and handle same-named things
        things = _filter_visible(self.contents_get(content_type="object"))

        grouped_things = defaultdict(list)
        for thing in things:
            grouped_things[thing.get_display_name(looker, **kwargs)].append(thing)

        thing_names = []
        for thingname, thinglist in sorted(grouped_things.items()):
            nthings = len(thinglist)
            thing = thinglist[0]
            singular, plural = thing.get_numbered_name(nthings, looker, key=thingname)
            thing_names.append(singular if nthings == 1 else plural)
        thing_names = "\n".join(thing_names)
        return "\n" + thing_names

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

        # populate the appearance_template string.
        return self.format_appearance(
            self.appearance_template.format(
                name=self.get_display_name(looker, **kwargs),
                desc=self.get_display_desc(looker, **kwargs),
                exits=self.get_display_exits(looker, **kwargs),
                characters=self.get_display_characters(looker, **kwargs),
                mobs=self.get_display_mobs(looker, **kwargs),
                things=self.get_display_things(looker, **kwargs),
            ),
            looker,
            **kwargs,
        )


class XYRoom(Room, xyzroom.XYZRoom):
    """
    A game location aware of its XYZ-position.

    Special properties:
        map_display (bool): If the return_appearance of the room should
            show the map or not.
        map_mode (str): One of 'nodes' or 'scan'. See `return_apperance`
            for examples of how they differ.
        map_visual_range (int): How far on the map one can see. This is a
            fixed value here, but could also be dynamic based on skills,
            light etc.
        map_character_symbol (str): The character symbol to use to show
            the character position. Can contain color info. Default is
            the @-character.
        map_area_client (bool): If True, map area will always fill the entire
            client width. If False, the map area's width will vary with the
            width of the currently displayed location description.
        map_fill_all (bool): I the map area should fill the client width or not.
        map_separator_char (str): The char to use to separate the map area from
            the room description.
    """
