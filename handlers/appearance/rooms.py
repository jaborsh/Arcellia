import datetime
import random
import re
from collections import defaultdict, deque

from evennia import FuncParser, gametime
from evennia.utils import dbserialize
from evennia.utils.utils import dedent, iter_to_str, repeat

from handlers.appearance.appearance import AppearanceHandler
from world.features import racial as racial_feats

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


class RoomAppearanceHandler(AppearanceHandler):
    """
    A comprehensive handler for managing room appearances in Evennia.

    This handler provides functionality for dynamic room descriptions that can change based on:
    - Time of day (morning, afternoon, evening, night)
    - Seasons (spring, summer, autumn, winter)
    - Room states (custom states like "raining", "foggy", etc.)
    - Lighting conditions (normal, dark, magical darkness)

    It also manages:
    - Room details (examinable objects within the room)
    - Automated room messages (periodic broadcasts)
    - Object grouping (for displaying multiple similar items)
    - Coordinate display for builders

    The handler supports:
    - State-based descriptions using $state() markup
    - Legacy time-of-day markup (<morning>text</morning>)
    - Dark vision and magical darkness effects
    - Ordered exit display
    - Smart object grouping for mobs and items

    Example Usage:
        room.appearance.add_desc("A sunny meadow.", "default")
        room.appearance.add_desc("A rain-soaked meadow.", "raining")
        room.appearance.add_detail("tree", "A tall oak tree stands here.")
        room.appearance.add_room_state("raining")

    Properties:
        desc (str): The current description based on room state
        time_of_day (str): Current time of day (morning, afternoon, evening, night)
        season (str): Current season (spring, summer, autumn, winter)
        is_dark (bool): Whether the room is in darkness
        is_magical_dark (bool): Whether the room is in magical darkness
        details (dict): Room's detail descriptions
        states (list): Current room states
        messages (list): Room's broadcast messages
    """

    # === Initialization and Persistence ===
    def __init__(self, obj):
        super().__init__(obj)

        # Time constants
        self._months_per_year = 12
        self._hours_per_day = 24

        # Time period mappings using integer ranges for efficiency
        self._seasons_per_year = {
            "spring": (3, 6),
            "summer": (6, 9),
            "autumn": (9, 12),
            "winter": (12, 3),
        }

        self._times_of_day = {
            "night": (0, 6),
            "morning": (6, 12),
            "afternoon": (12, 18),
            "evening": (18, 24),
        }

        # Initialize room state
        self.details = {}
        self.room_messages = []
        self.room_message_rate = 0
        self.broadcast_repeat_task = None
        self.room_states = []

        self._load()

    def _load(self):
        if data := self.obj.attributes.get(
            self._db_attribute, category=self._db_category
        ):
            self.descriptions = dbserialize.deserialize(
                data.get("descriptions", {})
            )
            self.details = dbserialize.deserialize(data.get("details", {}))
            self.room_messages = dbserialize.deserialize(
                data.get("room_messages", [])
            )
            self.room_message_rate = dbserialize.deserialize(
                data.get("room_message_rate", 0)
            )
            self.broadcast_repeat_task = dbserialize.deserialize(
                data.get("broadcast_repeat_task", None)
            )
            self.room_states = dbserialize.deserialize(
                data.get("room_states", [])
            )
            self.senses = dbserialize.deserialize(data.get("senses", {}))

    def _save(self):
        self.obj.attributes.add(
            self._db_attribute,
            {
                "descriptions": self.descriptions,
                "details": self.details,
                "room_messages": self.room_messages,
                "room_message_rate": self.room_message_rate,
                "broadcast_repeat_task": self.broadcast_repeat_task,
                "senses": self.senses,
            },
            category=self._db_category,
        )

    @property
    def desc(self):
        return self.get_desc()

    @property
    def time_of_day(self):
        """Current time of day."""
        return self.get_time_of_day()

    @property
    def season(self):
        """Current season."""
        return self.get_season()

    @property
    def is_dark(self):
        """Whether the room is in darkness."""
        return bool(self.obj.tags.get("dark", category="room_state"))

    @property
    def is_magical_dark(self):
        """Whether the room is in magical darkness."""
        return bool(self.obj.tags.get("magical_dark", category="room_state"))

    @property
    def states(self):
        """List of current room states."""
        return self.room_states.copy()

    @property
    def messages(self):
        """List of room broadcast messages."""
        return self.room_messages.copy()

    # === Room State Management ===
    def add_desc(self, desc, room_state=None):
        """
        Add or update a room description for a given state.

        Args:
            desc (str): The description text to add
            room_state (str, optional): The state this description applies to.
                If None, sets the default description.

        Notes:
            States are case-insensitive. Setting a description for an existing
            state will override the previous description.
        """
        if room_state is None:
            self.descriptions["default"] = desc
        else:
            self.descriptions[room_state.lower()] = desc
            self.add_room_state(room_state.lower())
        self._save()

    def remove_desc(self, room_state="default"):
        """
        Remove a description associated with a specific room state.

        Args:
            room_state (str, optional): The state key for which to remove the description.
                Defaults to 'default'.

        Note:
            - The room state is converted to lowercase before removal
            - If the state doesn't exist, no error is raised (silently fails)
            - Changes are automatically saved to persistent storage
        """
        self.descriptions.pop(room_state.lower(), None)
        self.remove_room_state(room_state.lower())
        self._save()

    def get_desc(self):
        """
        Get the current room description based on active states.

        Returns:
            str: The room's current description text.

        Notes:
            Description priority order:
            1. Active non-seasonal room states
            2. Active seasonal states
            3. Current season
            4. Default description
            5. Fallback description ("You see nothing special.")
        """
        room_states = self.room_states
        seasons = self._seasons_per_year.keys()
        seasonal_states = []

        for state in sorted(room_states):
            if state not in seasons:
                if desc := (self.descriptions.get(state)):
                    return desc
            else:
                seasonal_states.append(state)

        if not seasons:
            return self.descriptions.get("default", self._fallback_desc)

        for seasonal_state in seasonal_states:
            if desc := self.descriptions.get(seasonal_state):
                return desc

        season = self.get_season()
        if desc := (self.descriptions.get(season)):
            return desc

        return self.descriptions.get("default", self._fallback_desc)

    def add_room_state(self, *room_states):
        """
        Add one or more states to the room.

        Args:
            *room_states: Variable number of state strings to add.

        Examples:
            add_room_state("raining")
            add_room_state("dark", "foggy", "winter")
        """
        for room_state in room_states:
            self.room_states.append(room_state.lower())
        self._save()

    def remove_room_state(self, *room_states):
        """
        Remove one or more states from the room.

        Args:
            *room_states: Variable number of state strings to remove.

        Notes:
            Silently ignores states that aren't currently active.
        """
        for room_state in room_states:
            self.room_states.remove(room_state)
        self._save()

    def clear_room_state(self):
        """Clear all room states"""
        self.room_states.clear()
        self._save()

    # === Time and Season Management ===
    def get_time_of_day(self):
        """
        Get the current time period based on game time.

        Returns:
            str: One of "night" (00-06), "morning" (06-12),
                "afternoon" (12-18), or "evening" (18-24)

        Notes:
            Uses server's game time configuration for calculations.
        """
        timestamp = gametime.gametime(absolute=True)
        hour = datetime.datetime.fromtimestamp(timestamp).hour

        for time_of_day, (start, end) in self._times_of_day.items():
            if start < end and start <= hour < end:
                return time_of_day
        return time_of_day

    def get_season(self):
        """
        Get the current season based on game time.

        Returns:
            str: One of "spring" (3-6), "summer" (6-9),
                "autumn" (9-12), or "winter" (12-3)

        Notes:
            Uses server's game time configuration for calculations.
        """
        timestamp = gametime.gametime(absolute=True)
        month = datetime.datetime.fromtimestamp(timestamp).month

        for season, (start, end) in self._seasons_per_year.items():
            if start < end and start <= month < end:
                return season
        return season

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
            for tod in self._times_of_day:
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

    # === Room Detail Management ===
    def add_detail(self, key, description):
        """
        Add an examinable detail to the room.

        Args:
            key (str): The name/identifier of the detail
            description (str): The description shown when examining the detail

        Notes:
            - Keys are case-insensitive
            - Supports $state() markup in descriptions
            - Adding a detail with an existing key overwrites the old detail
        """
        self.details[key.lower()] = description
        self._save()

    def remove_detail(self, key):
        """Remove a room detail"""
        self.details.pop(key.lower(), None)
        self._save()

    def get_detail(self, key, looker=None):
        """
        Get a detail's description, supporting partial key matches.

        Args:
            key (str): The detail key to look up
            looker (Object, optional): The object examining the detail

        Returns:
            str or None: The detail's description if found, None if no match

        Notes:
            - Searches for exact matches first
            - Falls back to prefix matching if no exact match
            - Processes any state markup in the description
            - Returns None if no match found
        """
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

    # === Message Broadcasting ===
    def start_broadcast_messages(self, rate=None):
        """
        Start periodic broadcasting of random room messages.

        Args:
            rate (int, optional): Seconds between broadcasts.
                Uses existing rate if None.

        Notes:
            - Only starts if messages exist and no broadcast is running
            - Saves the new rate if provided
            - Messages are chosen randomly from the message list
        """
        if rate:
            self.room_message_rate = rate

        if (
            self.room_message_rate
            and self.room_messages
            and not self.broadcast_repeat_task
        ):
            self.broadcast_repeat_task = repeat(
                self.room_message_rate,
                self.broadcast_message,
                persistent=False,
            )
        self._save()

    def broadcast_message(self):
        """Broadcast a random room message"""
        if self.room_messages:
            self.obj.msg_contents(random.choice(self.room_messages))

    # === Display Formatting Helpers ===
    def _func_state(self, roomstate, *args, looker=None, room=None, **kwargs):
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
            if (
                roomstate in room.room_states
                or roomstate == room.get_time_of_day()
            ):
                return text
            if roomstate == "default" and not room.room_states:
                # return this if no roomstate is set
                return text
        except AttributeError:
            # maybe used on a non-ExtendedRoom?
            pass
        return ""

    def _get_funcparser(self, looker):
        return FuncParser(
            {"state": self._func_state},
            looker=looker,
            room=self.obj,
        )

    def _filter_visible(self, looker, obj_list):
        """Filter objects that are visible to the looker."""
        return [
            obj
            for obj in obj_list
            if obj != looker and obj.access(looker, "view")
        ]

    def _group_objects(self, objects, looker, **kwargs):
        """Group objects by their display name and count occurrences."""
        grouped = defaultdict(list)
        for obj in objects:
            grouped[obj.get_display_name(looker, **kwargs)].append(obj)
        return grouped

    def _format_grouped_objects(self, grouped_objects, looker, **kwargs):
        """Format grouped objects into display strings."""
        names = []
        for objname, objlist in sorted(grouped_objects.items()):
            obj = objlist[0]
            count = len(objlist)
            singular, plural = obj.get_numbered_name(
                count, looker, key=objname, **kwargs
            )
            names.append(singular if count == 1 else plural)
        return "\n".join(names)

    # === Component Display Methods ===
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
        desc = self.get_desc()
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
        Get formatted list of visible exits.

        Args:
            looker (Object): The object viewing the exits
            **kwargs: Additional parameters passed through

        Returns:
            str: Formatted exit list in compass order

        Notes:
            - Orders exits: N,W,S,E,NW,NE,SW,SE,Up,Down
            - Only shows exits the looker can access
            - Appends non-compass exits at the end
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

        return f"{character_names}\n" if character_names else ""

    def get_display_mobs(self, looker, **kwargs):
        """Get formatted mob display string."""
        mobs = self._filter_visible(
            looker, self.obj.contents_get(content_type="mob")
        )
        grouped_mobs = self._group_objects(mobs, looker, **kwargs)
        mob_names = self._format_grouped_objects(grouped_mobs, looker, **kwargs)
        return f"{mob_names}\n" if mob_names else ""

    def get_display_things(self, looker, **kwargs):
        """Get formatted object display string."""
        things = self._filter_visible(
            looker, self.obj.contents_get(content_type="object")
        )
        grouped_things = self._group_objects(things, looker, **kwargs)
        thing_names = self._format_grouped_objects(
            grouped_things, looker, **kwargs
        )

        # Add spacing if there are characters or mobs
        has_characters = bool(
            self.obj.contents_get(exclude=looker, content_type="character")
        )
        has_mobs = bool(
            self.obj.contents_get(exclude=looker, content_type="mob")
        )
        prefix = "\n" if has_characters or has_mobs and thing_names else ""
        return f"{prefix}{thing_names}" if thing_names else ""

    # === Main Appearance Methods ===
    def return_appearance(self, looker, **kwargs):
        """
        Get the room's full appearance for a looker.

        Args:
            looker (Object): The object viewing the room
            **kwargs: Additional parameters passed through

        Returns:
            str: Complete formatted room description

        Notes:
            - Handles darkness based on looker's capabilities
            - Includes name, description, exits, and contents
            - Contents are grouped by type (chars, mobs, objects)
            - Respects room states and time-based descriptions
        """
        if not looker or not self.obj.access(looker, "appearance"):
            return ""

        # Check dark room conditions for non-admin players
        if not looker.permissions.check("Admin"):
            if self.obj.tags.get("dark", category="room_state"):
                if not looker.feats.has(racial_feats.Darkvision):
                    return self.return_dark_appearance(looker, **kwargs)
            elif self.obj.tags.get("magical_dark", category="room_state"):
                if not looker.feats.has(racial_feats.SuperiorDarkvision):
                    dark_msg = (
                        self.return_dark_appearance(looker, **kwargs)
                        if looker.feats.has(racial_feats.Darkvision)
                        else "It is too dark to see."
                    )
                    return dark_msg

        # Return normal appearance
        return ROOM_APPEARANCE_TEMPLATE.format(
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
        return ROOM_DARK_APPEARANCE_TEMPLATE.format(
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
