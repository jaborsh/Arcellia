"""
Room

Rooms are simple containers that has no location of their own.

"""
import datetime
import random
import re
from collections import defaultdict, deque
from textwrap import dedent

from django.conf import settings
from django.db.models import Q
from evennia import FuncParser, gametime
from evennia.contrib.grid.xyzgrid import xyzroom
from evennia.objects.objects import DefaultRoom
from evennia.typeclasses.attributes import AttributeProperty
from evennia.utils.utils import iter_to_str, repeat

from .objects import Object

CLIENT_DEFAULT_WIDTH = settings.CLIENT_DEFAULT_WIDTH
MAP_X_TAG_CATEGORY = "room_x_coordinate"
MAP_Y_TAG_CATEGORY = "room_y_coordinate"
MAP_Z_TAG_CATEGORY = "room_z_coordinate"

MAP_XDEST_TAG_CATEGORY = "exit_dest_x_coordinate"
MAP_YDEST_TAG_CATEGORY = "exit_dest_y_coordinate"
MAP_ZDEST_TAG_CATEGORY = "exit_dest_z_coordinate"


def func_state(roomstate, *args, looker=None, room=None, **kwargs):
    """
    Usage: $state(roomstate, text)

    Funcparser callable for ExtendedRoom. This is called by the FuncParser when it
    returns the description of the room. Use 'default' for a default text when no
    other states are set.

    Args:
        roomstate (str): A roomstate, like "morning", "raining". This is case insensitive.
        *args: All these will be combined into one string separated by commas.

    Keyword Args:
        looker (Object): The object looking at the room. Unused by default.
        room (ExtendedRoom): The room being looked at.

    Example:

        $state(morning, It is a beautiful morning!)

    Notes:
        We try to merge all args into one text, since this function doesn't require more than one
        argument. That way, one may be able to get away without using quotes.

    """
    roomstate = str(roomstate).lower()
    text = ", ".join(args)
    # make sure we have a room and a caller and not something parsed from the string
    if (
        not (roomstate and looker and room)
        or isinstance(looker, str)
        or isinstance(room, str)
    ):
        return ""

    try:
        if roomstate in room.room_states or roomstate == room.get_time_of_day():
            return text
        if roomstate == "default" and not room.room_states:
            # return this if no roomstate is set
            return text
    except AttributeError:
        # maybe used on a non-ExtendedRoom?
        pass
    return ""


class Room(Object, DefaultRoom):
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

    # fallback description if nothing else is set
    fallback_desc = "You see nothing special."

    # tag room_state category
    room_state_tag_category = "room_state"

    # time setup
    months_per_year = 12
    hours_per_day = 24

    # seasons per year, given as (start, end) boundaries, each a fraction of a year. These
    # will change the description. The last entry should wrap around to the first.
    seasons_per_year = {
        "spring": (3 / months_per_year, 6 / months_per_year),  # March - May
        "summer": (6 / months_per_year, 9 / months_per_year),  # June - August
        "autumn": (9 / months_per_year, 12 / months_per_year),  # September - November
        "winter": (12 / months_per_year, 3 / months_per_year),  # December - February
    }

    # time-dependent room descriptions (these must match the `seasons_per_year` above).
    desc_spring = AttributeProperty("", autocreate=False)
    desc_summer = AttributeProperty("", autocreate=False)
    desc_autumn = AttributeProperty("", autocreate=False)
    desc_winter = AttributeProperty("", autocreate=False)

    # time-dependent embedded descriptions, usable as $timeofday(morning, text)
    # (start, end) boundaries, each a fraction of a day. The last one should
    # end at 0 (not 24) to wrap around to midnight.
    times_of_day = {
        "night": (0, 6 / hours_per_day),  # midnight - 6AM
        "morning": (6 / hours_per_day, 12 / hours_per_day),  # 6AM - noon
        "afternoon": (12 / hours_per_day, 18 / hours_per_day),  # noon - 6PM
        "evening": (18 / hours_per_day, 0),  # 6PM - midnight
    }

    # normal vanilla description if no other `*_desc` matches or are set.
    desc = AttributeProperty("", autocreate=False)

    # look-targets without database objects
    details = AttributeProperty(dict, autocreate=False)

    # messages to send to the room
    room_message_rate = 0  # set >0s to enable
    room_messages = AttributeProperty(list, autocreate=False)

    def _get_funcparser(self, looker):
        return FuncParser(
            {"state": func_state},
            looker=looker,
            room=self,
        )

    def _start_broadcast_repeat_task(self):
        if (
            self.room_message_rate
            and self.room_messages
            and not self.ndb.broadcast_repeat_task
        ):
            self.ndb.broadcast_repeat_task = repeat(
                self.room_message_rate,
                self.repeat_broadcast_msg_to_room,
                persistent=False,
            )

    def at_init(self):
        """Evennia hook. Start up repeating function whenever object loads into memory."""
        self._start_broadcast_repeat_task()

    def at_object_delete(self):
        for mob in self.db.mobs:
            mob.delete()
        return True

    def start_repeat_broadcast_messages(self):
        """
        Start repeating the broadcast messages. Only needs to be called if adding messages
        and not having reloaded the server.

        """
        self._start_broadcast_repeat_task()

    def repeat_broadcast_message_to_room(self):
        """
        Send a message to the room at room_message_rate. By default
        we will randomize which one to send.

        """
        self.msg_contents(random.choice(self.room_messages))

    def get_time_of_day(self):
        """
        Get the current time of day.

        Override to customize.

        Returns:
            str: The time of day, such as 'morning', 'afternoon', 'evening' or 'night'.

        """
        timestamp = gametime.gametime(absolute=True)
        datestamp = datetime.datetime.fromtimestamp(timestamp)
        timeslot = float(datestamp.hour) / self.hours_per_day

        for time_of_day, (start, end) in self.times_of_day.items():
            if start < end and start <= timeslot < end:
                return time_of_day
        return time_of_day  # final back to the beginning

    def get_season(self):
        """
        Get the current season.

        Override to customize.

        Returns:
            str: The season, such as 'spring', 'summer', 'autumn' or 'winter'.

        """
        timestamp = gametime.gametime(absolute=True)
        datestamp = datetime.datetime.fromtimestamp(timestamp)
        timeslot = float(datestamp.month) / self.months_per_year

        for season_of_year, (start, end) in self.seasons_per_year.items():
            if start < end and start <= timeslot < end:
                return season_of_year
        return season_of_year  # final step is back to beginning

    ##############
    # Properties #
    ##############
    @property
    def display_name(self):
        """
        Return a potentially fanciful name
        """
        return self.attributes.get("display_name", self.name)

    @display_name.setter
    def display_name(self, value: str):
        self.db.display_name = value

    # manipulate room states
    @property
    def room_states(self):
        """
        Get all room_states set on this room.

        """
        return list(
            sorted(
                self.tags.get(category=self.room_state_tag_category, return_list=True)
            )
        )

    ###########
    # Methods #
    ###########
    def add_room_state(self, *room_states):
        """
        Set a room-state or room-states to the room.

        Args:
            *room_state (str): A room state like 'on_fire' or 'flooded'. This will affect
                what `desc_*` and `roomstate_*` descriptions/inlines are used. You can add
                more than one at a time.

        Notes:
            You can also set time-based room_states this way, like 'morning' or 'spring'. This
            can be useful to force a particular description, but while this state is
            set this way, that state will be unaffected by the passage of time. Remove
            the state to let the current game time determine this type of states.

        """
        self.tags.batch_add(
            *((state, self.room_state_tag_category) for state in room_states)
        )

    def remove_room_state(self, *room_states):
        """
        Remove a roomstate from the room.

        Args:
            *room_state (str): A roomstate like 'on_fire' or 'flooded'. If the
            room did not have this state, nothing happens.You can remove more than one at a time.

        """
        for room_state in room_states:
            self.tags.remove(room_state, category=self.room_state_tag_category)

    def clear_room_state(self):
        """
        Clear all room states.

        Note that fallback time-of-day and seasonal states are not affected by this, only
        custom states added with `.add_room_state()`.

        """
        self.tags.clear(category="room_state")

    # control the available room descriptions

    def add_desc(self, desc, room_state=None):
        """
        Add a custom description, matching a particular room state.

        Args:
            desc (str): The description to use when this roomstate is active.
            roomstate (str, None): The roomstate to match, like 'on_fire', 'flooded', or "spring".
                If `None`, set the default `desc` fallback.

        """
        if room_state is None:
            self.attributes.add("desc", desc)
        else:
            self.attributes.add(f"desc_{room_state}", desc)

    def remove_desc(self, room_state):
        """
        Remove a custom description.

        Args:
            room_state (str): The room-state description to remove.

        """
        self.attributes.remove(f"desc_{room_state}")

    def all_desc(self):
        """
        Get all available descriptions.

        Returns:
            dict: A mapping of roomstate to description. The `None` key indicates the
                base subscription (stored in the `desc` Attribute).

        """
        return {
            **{None: self.db.desc or ""},
            **{
                attr.key[5:]: attr.value
                for attr in self.db_attributes.filter(
                    db_key__startswith="desc_"
                ).order_by("db_key")
            },
        }

    def get_stateful_desc(self):
        """
        Get the currently active room description based on the current roomstate.

        Returns:
            str: The current description.

        Note:
            Only one description can be active at a time. Priority order is as follows:

            Priority order is as follows:

                1. Room-states set by `add_roomstate()` that are not seasons.
                   If multiple room_states are set, the first one is used, sorted alphabetically.
                2. Seasons set by `add_room_state()`. This allows to 'pin' a season.
                3. Time-based seasons based on the current in-game time.
                4. None, if no seasons are defined in `.seasons_per_year`.

            If either of the above is found, but doesn't have a matching `desc_<roomstate>`
            description, we move on to the next priority. If no matches are found, the `desc`
            Attribute is used.

        """

        room_states = self.room_states
        seasons = self.seasons_per_year.keys()
        seasonal_room_states = []

        # get all available descriptions on this room
        # note: *_desc is the old form, we support it for legacy
        descriptions = dict(
            self.db_attributes.filter(
                Q(db_key__startswith="desc_") | Q(db_key__endswith="_desc")
            ).values_list("db_key", "db_value")
        )

        for roomstate in sorted(room_states):
            if roomstate not in seasons:
                # if we have a roomstate that is not a season, use it
                if desc := descriptions.get(f"desc_{roomstate}") or descriptions.get(
                    "{roomstate}_desc"
                ):
                    return desc
            else:
                seasonal_room_states.append(roomstate)

        if not seasons:
            # no seasons defined, so just return the default desc
            return self.attributes.get("desc")

        for seasonal_roomstate in seasonal_room_states:
            # explicit setting of season outside of automatic time keeping
            if desc := descriptions.get(f"desc_{seasonal_roomstate}"):
                return desc

        # no matching room_states, use time-based seasons. Also support legacy *_desc form
        season = self.get_season()
        if desc := descriptions.get(f"desc_{season}") or descriptions.get(
            f"{season}_desc"
        ):
            return desc

        # fallback to normal desc Attribute
        return self.attributes.get("desc", self.fallback_desc)

    def replace_legacy_time_of_day_markup(self, desc):
        """
        Filter description by legacy markup like `<morning>...</morning>`. Filter
        out all such markings that does not match the current time. Supports
        'morning', 'afternoon', 'evening' and 'night'.

        Args:
            desc (str): The unmodified description.

        Returns:
            str: A possibly modified description.

        Notes:
            This is legacy. Use the $state markup for new rooms instead.

        """
        desc = desc or ""
        time_of_day = self.get_time_of_day()

        # regexes for in-desc replacements (gets cached)
        if not hasattr(self, "legacy_timeofday_regex_map"):
            timeslots = deque()
            for time_of_day in self.times_of_day:
                timeslots.append(
                    (
                        time_of_day,
                        re.compile(
                            rf"<{time_of_day}>(.*?)</{time_of_day}>", re.IGNORECASE
                        ),
                    )
                )

            # map the regexes cyclically, so each one is first once
            self.legacy_timeofday_regex_map = {}
            for i in range(len(timeslots)):
                # mapping {"morning": [morning_regex, ...], ...}
                self.legacy_timeofday_regex_map[timeslots[0][0]] = [
                    tup[1] for tup in timeslots
                ]
                timeslots.rotate(-1)

        # do the replacement
        regextuple = self.legacy_timeofday_regex_map[time_of_day]
        desc = regextuple[0].sub(r"\1", desc)
        desc = regextuple[1].sub("", desc)
        desc = regextuple[2].sub("", desc)
        return regextuple[3].sub("", desc)

    # manipulate details

    def add_detail(self, key, description):
        """
        This sets a new detail, using an Attribute "details".

        Args:
            detailkey (str): The detail identifier to add (for
                aliases you need to add multiple keys to the
                same description). Case-insensitive.
            description (str): The text to return when looking
                at the given detailkey. This can contain funcparser directives.

        """
        if not self.details:
            self.details = {}  # causes it to be created as real attribute
        self.details[key.lower()] = description

    set_detail = add_detail  # legacy name

    def remove_detail(self, key, *args):
        """
        Delete a detail.

        Args:
            key (str): the detail to remove (case-insensitive).
            *args: Unused (backwards compatibility)

        The description is only included for compliance but is completely
        ignored.  Note that this method doesn't raise any exception if
        the detail doesn't exist in this room.

        """
        self.details.pop(key.lower(), None)

    del_detail = remove_detail  # legacy alias

    def get_detail(self, key, looker=None):
        """
        This will attempt to match a "detail" to look for in the room.
        This will do a lower-case match followed by a startsby match. This
        is called by the new `look` Command.

        Args:
            key (str): A detail identifier.
            looker (Object, optional): The one looking.

        Returns:
            detail (str or None): A detail matching the given key, or `None` if
            it was not found.

        Notes:
            A detail is a way to offer more things to look at in a room
            without having to add new objects. For this to work, we
            require a custom `look` command that allows for `look <detail>`
            - the look command should defer to this method on
            the current location (if it exists) before giving up on
            finding the target.

        """
        key = key.lower()
        detail_keys = tuple(self.details.keys())

        detail = None
        if key in detail_keys:
            # exact match
            detail = self.details[key]
        else:
            # find closest match starting with key (shortest difference in length)
            lkey = len(key)
            startswith_matches = sorted(
                (
                    (detail_key, abs(lkey - len(detail_key)))
                    for detail_key in detail_keys
                    if detail_key.startswith(key)
                ),
                key=lambda tup: tup[1],
            )
            if startswith_matches:
                # use the matching startswith-detail with the shortest difference in length
                detail = self.details[startswith_matches[0][0]]

        if detail:
            detail = self._get_funcparser(looker).parse(detail)

        return detail

    return_detail = get_detail  # legacy name

    # populated by `return_appearance`
    appearance_template = dedent(
        """
        {name}

            {desc}

            {exits}{characters}{mobs}{things}
        """
    )

    def get_display_name(self, looker=None, **kwargs):
        """
        Displays the name of the object in a viewer-aware manner.

        Args:
            looker (TypedObject): The object or account that is looking
                at/getting inforamtion for this object. If not given, `.name` will be
                returned, which can in turn be used to display colored data.

        Returns:
            str: A name to display for this object. This can contain color codes and may
                be customized based on `looker`. By default this contains the `.key` of the object,
                followed by the DBREF if this user is privileged to control said object.

        Notes:
            This function could be extended to change how object names appear to users in character,
            but be wary. This function does not change an object's keys or aliases when searching,
            and is expected to produce something useful for builders.

        """
        if looker and self.locks.check_lockstring(looker, "perm(Builder)"):
            return "{}(#{})".format(self.display_name, self.id)
        return self.display_name

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

        return f"\n{character_names}\n" if character_names else "\n"

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
        thing_names = iter_to_str(thing_names)
        return f"\n{thing_names}" if thing_names else ""

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


class XYRoom(xyzroom.XYZRoom, Room):
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

    map_display = False
