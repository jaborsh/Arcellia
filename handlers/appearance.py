import datetime
import random
import re
from collections import defaultdict, deque

from django.db.models import Q
from evennia import FuncParser, gametime
from evennia.utils import dbserialize
from evennia.utils.utils import compress_whitespace, dedent, iter_to_str, repeat

from handlers.handler import Handler
from utils.text import _INFLECT, strip_ansi
from world.features import racial as racial_feats

APPEARANCE_TEMPLATE = dedent(
    """
    {desc}
    
    {characters}
    {things}
    """
)

ROOM_APPEARANCE_TEMPLATE = dedent(
    """
    {name}
    
        {desc}
        
        {exits}
        
    {characters}{mobs}{things}
    """
)

ROOM_DARK_APPEARANCE_TEMPLATE = dedent(
    """
    {name}
    
        {desc}
    """
)


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


class AppearanceHandler(Handler):
    def __init__(self, obj):
        super().__init__(obj, "appearance")
        self.appearance_template = APPEARANCE_TEMPLATE

    def _filter_visible(self, looker, obj_list):
        return [
            obj
            for obj in obj_list
            if obj != looker and obj.access(looker, "view")
        ]

    def get_display_name(self, looker=None, **kwargs):
        """
        Displays the name of the object in a viewer-aware manner.

        Args:
            looker (DefaultObject): The object or account that is looking at or getting information
                for this object.

        Returns:
            str: A name to display for this object. By default this returns the `.name` of the object.

        Notes:
            This function can be extended to change how object names appear to users in character,
            but it does not change an object's keys or aliases when searching.
        """
        if looker and self.obj.locks.check_lockstring(looker, "perm(Builder)"):
            return f"{self.obj.display_name}(#{self.obj.id})"
        return self.obj.display_name

    def get_display_desc(self, looker, **kwargs):
        """
        Get the 'desc' component of the object description. Called by `return_appearance`.

        Args:
            looker (DefaultObject): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The desc display string.

        """
        return self.obj.db.desc.strip() or "You see nothing special."

    def get_display_characters(self, looker, **kwargs):
        """
        Get the 'characters' component of the object description. Called by `return_appearance`.

        Args:
            looker (DefaultObject): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The character display data.

        """
        characters = self._filter_visible(
            looker, self.obj.contents_get(content_type="character")
        )
        character_names = iter_to_str(
            char.get_display_name(looker, **kwargs) for char in characters
        )

        return f"|wCharacters:|n {character_names}" if character_names else ""

    def get_display_things(self, looker=None, **kwargs):
        """
        Get the 'things' component of the object description. Called by `return_appearance`.

        Args:
            looker (DefaultObject): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The things display data.
        """
        things = self._filter_visible(
            looker, self.obj.contents_get(content_type="object")
        )

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
        thing_names = "\n ".join(thing_names)
        return f"|wYou see:|n\n {thing_names}" if thing_names else ""

    def get_numbered_name(self, count, looker, **kwargs):
        """
        Return the numbered (singular, plural) forms of this object's key. This
        is by default called by return_appearance and is used for grouping
        multiple same-named of this object. Note that this will be called on
        *every* member of a group even though the plural name will be only shown
        once. Also the singular display version, such as 'an apple', 'a tree'
        is determined from this method.

        Args:
            count (int): Number of objects of this type
            looker (Object): Onlooker. Not used by default.

        Keyword Args:
            key (str): Optional key to pluralize. If not given, the object's `.name` property is used.
            no_article (bool): If 'True', do not return an article if 'count' is 1.

        Returns:
            tuple: This is a tuple `(str, str)` with the singular and plural forms of the key
                including the count.

        Examples:
            obj.get_numbered_name(3, looker, key="foo") -> ("a foo", "three foos")
        """
        if kwargs.get("no_article", False):
            return self.obj.get_display_name(looker), self.obj.get_display_name(
                looker
            )

        key = kwargs.get("key", self.obj.get_display_name(looker))

        color_code_pattern = r"(\|(r|g|y|b|m|c|w|x|R|G|Y|B|M|C|W|X|\d{3}|#[0-9A-Fa-f]{6})|\[.*\])"
        color_code_positions = [
            (m.start(0), m.end(0)) for m in re.finditer(color_code_pattern, key)
        ]

        segments = []
        last_pos = 0
        for start, end in color_code_positions:
            segments.append(key[last_pos:start])
            segments.append(key[start:end])
            last_pos = end
        segments.append(key[last_pos:])

        plural_segments = []
        singular_segments = []

        for segment in segments:
            if re.match(color_code_pattern, segment):
                plural_segments.append(segment)
                singular_segments.append(segment)
            else:
                plural_segment = (
                    _INFLECT.plural(segment, count)
                    if segment.strip()
                    else segment
                )
                plural_segments.append(plural_segment)

                if len(singular_segments) == 2:
                    segment = (
                        _INFLECT.an(segment) if segment.strip() else segment
                    )
                    split_segment = segment.split(" ")
                    singular_segment = (
                        strip_ansi(split_segment[0])
                        + singular_segments[1]
                        + " "
                        + " ".join(split_segment[1:])
                    )
                    singular_segments[1] = ""
                else:
                    singular_segment = segment
                singular_segments.append(singular_segment)

        plural = re.split(color_code_pattern, "".join(plural_segments), 1)
        plural = (
            _INFLECT.number_to_words(count)
            + " "
            + plural[1]
            + _INFLECT.plural(plural[3], count)
            + "|n"
            if len(plural) > 1
            else _INFLECT.plural(plural[0])
        )
        singular = "".join(singular_segments)

        if not self.obj.aliases.get(strip_ansi(singular)):
            self.obj.aliases.add(strip_ansi(singular))
        if not self.obj.aliases.get(strip_ansi(plural)):
            self.obj.aliases.add(strip_ansi(plural))

        return singular, plural

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
            looker (DefaultObject): Object doing the looking. Passed into all helper methods.
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

        return compress_whitespace(
            self.appearance_template.format(
                desc=self.get_display_desc(looker, **kwargs),
                characters=self.get_display_characters(looker, **kwargs),
                things=self.get_display_things(looker, **kwargs),
            ).strip(),
            max_linebreaks=2,
        )


class RoomAppearanceHandler(AppearanceHandler):
    def __init__(self, obj):
        super().__init__(obj)
        self.appearance_template = ROOM_APPEARANCE_TEMPLATE
        self.dark_template = ROOM_DARK_APPEARANCE_TEMPLATE
        self.fallback_desc = "You see nothing special."
        self.room_state_tag_category = "room_state"
        self.months_per_year = 12
        self.hours_per_day = 24

        # Time periods
        self.seasons_per_year = {
            "spring": (3 / self.months_per_year, 6 / self.months_per_year),
            "summer": (6 / self.months_per_year, 9 / self.months_per_year),
            "autumn": (9 / self.months_per_year, 12 / self.months_per_year),
            "winter": (12 / self.months_per_year, 3 / self.months_per_year),
        }

        self.times_of_day = {
            "night": (0, 6 / self.hours_per_day),
            "morning": (6 / self.hours_per_day, 12 / self.hours_per_day),
            "afternoon": (12 / self.hours_per_day, 18 / self.hours_per_day),
            "evening": (18 / self.hours_per_day, 0),
        }

        # Initialize room details and messages
        self._room_message_rate = 0
        self._broadcast_repeat_task = None
        self._load()

    @property
    def details(self):
        """Get room details"""
        return self._data["details"]

    @details.setter
    def details(self, value):
        """Set room details"""
        self._data["details"] = value
        self.obj.attributes.add("details", value)

    @property
    def room_messages(self):
        """Get room messages"""
        return self._data["room_messages"]

    @room_messages.setter
    def room_messages(self, value):
        """Set room messages"""
        self._room_messages = value
        self.obj.attributes.add("room_messages", value)

    @property
    def room_states(self):
        return [
            tag.db_key
            for tag in self.obj.tags.get(
                category=self.room_state_tag_category, return_list=True
            )
        ]

    def _load(self):
        """Override to load both details and messages"""
        details = self.obj.attributes.get("details", {})
        room_messages = self.obj.attributes.get("room_messages", [])
        self._data = {
            "details": dbserialize.deserialize(details),
            "room_messages": dbserialize.deserialize(room_messages),
        }

    def _save(self):
        """Override to save both details and messages"""
        self.obj.attributes.add("details", self.details)
        self.obj.attributes.add("room_messages", self.room_messages)

    def _get_funcparser(self, looker):
        return FuncParser(
            {"state": func_state},
            looker=looker,
            room=self.obj,
        )

    def get_time_of_day(self):
        """Get current time of day"""
        timestamp = gametime.gametime(absolute=True)
        datestamp = datetime.datetime.fromtimestamp(timestamp)
        timeslot = float(datestamp.hour) / self.hours_per_day

        for time_of_day, (start, end) in self.times_of_day.items():
            if start < end and start <= timeslot < end:
                return time_of_day
        return time_of_day

    def get_season(self):
        """Get current season"""
        timestamp = gametime.gametime(absolute=True)
        datestamp = datetime.datetime.fromtimestamp(timestamp)
        timeslot = float(datestamp.month) / self.months_per_year

        for season, (start, end) in self.seasons_per_year.items():
            if start < end and start <= timeslot < end:
                return season
        return season

    def add_room_state(self, *room_states):
        """Add room states"""
        self.obj.tags.batch_add(
            *((state, self.room_state_tag_category) for state in room_states)
        )

    def remove_room_state(self, *room_states):
        """Remove room states"""
        for room_state in room_states:
            self.obj.tags.remove(
                room_state, category=self.room_state_tag_category
            )

    def clear_room_state(self):
        """Clear all room states"""
        self.obj.tags.clear(category=self.room_state_tag_category)

    def add_detail(self, key, description):
        """Add a room detail"""
        if not self.details:
            self.details = {}
        self.details[key.lower()] = description
        self._save()

    def remove_detail(self, key):
        """Remove a room detail"""
        self.details.pop(key.lower(), None)
        self._save()

    def get_detail(self, key, looker=None):
        key = key.lower()
        detail_keys = tuple(self.details.keys())

        if key in detail_keys:
            detail = self.details[key]
        else:
            # Find closest match starting with key
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
                detail = self.details[startswith_matches[0][0]]
            else:
                return None

        return self._get_funcparser(looker).parse(detail) if detail else None

    def start_broadcast_messages(self, rate=None):
        """Start broadcasting room messages"""
        if rate:
            self._room_message_rate = rate

        if (
            self._room_message_rate
            and self.room_messages
            and not self._broadcast_repeat_task
        ):
            self._broadcast_repeat_task = repeat(
                self._room_message_rate,
                self.broadcast_message,
                persistent=False,
            )
        self._save()

    def broadcast_message(self):
        """Broadcast a random room message"""
        if self.room_messages:
            self.obj.msg_contents(random.choice(self.room_messages))

    def get_stateful_desc(self):
        """Get description based on current room state"""
        room_states = self.room_states
        seasons = self.seasons_per_year.keys()
        seasonal_states = []

        descriptions = dict(
            self.obj.db_attributes.filter(
                Q(db_key__startswith="desc_") | Q(db_key__endswith="_desc")
            ).values_list("db_key", "db_value")
        )

        for state in sorted(room_states):
            if state not in seasons:
                if desc := (
                    descriptions.get(f"desc_{state}")
                    or descriptions.get(f"{state}_desc")
                ):
                    return desc
            else:
                seasonal_states.append(state)

        if not seasons:
            return self.obj.attributes.get("desc", self.fallback_desc)

        for seasonal_state in seasonal_states:
            if desc := descriptions.get(f"desc_{seasonal_state}"):
                return desc

        season = self.get_season()
        if desc := (
            descriptions.get(f"desc_{season}")
            or descriptions.get(f"{season}_desc")
        ):
            return desc

        return self.obj.attributes.get("desc", self.fallback_desc)

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

        current_time_of_day = self.get_time_of_day()

        # regexes for in-desc replacements (gets cached)
        if not hasattr(self, "legacy_timeofday_regex_map"):
            timeslots = deque()
            for tod in self.times_of_day:
                timeslots.append(
                    (
                        tod,
                        re.compile(rf"<{tod}>(.*?)</{tod}>", re.IGNORECASE),
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
        regextuple = self.legacy_timeofday_regex_map[current_time_of_day]
        for regex in regextuple:
            desc = regex.sub(r"\1" if regex == regextuple[0] else "", desc)
        return desc

    def get_display_name(self, looker, **kwargs):
        """
        Displays the name of the object in a viewer-aware manner.

        Args:
            looker (DefaultObject): The object or account that is looking at or getting information
                for this object.

        Returns:
            str: A name to display for this object. By default this returns the `.name` of the object.

        Notes:
            This function can be extended to change how object names appear to users in character,
            but it does not change an object's keys or aliases when searching.
        """
        x = self.obj.tags.get(category="room_x_coordinate")
        y = self.obj.tags.get(category="room_y_coordinate")
        z = self.obj.tags.get(category="room_z_coordinate")
        xyz = f"[{x},{y},{z}]" if x and y and z else ""
        if looker and self.obj.locks.check_lockstring(looker, "perm(Builder)"):
            return f"{self.obj.display_name}{xyz}(#{self.obj.id})"
        return self.obj.display_name

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

        exits = sorted(
            self._filter_visible(
                looker, self.obj.contents_get(content_type="exit")
            ),
            key=exit_sort_key,
        )
        exit_names = iter_to_str(exit.display_name for exit in exits)

        return (
            f"|wObvious Exits: {exit_names}|n"
            if exit_names
            else "|wObvious Exits: None|n"
        )

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

        mobs = _filter_visible(self.obj.contents_get(content_type="mob"))

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
        things = _filter_visible(self.obj.contents_get(content_type="object"))

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
