import datetime
import random
import re
from collections import deque

from django.db.models import Q
from evennia import FuncParser, gametime
from evennia.typeclasses.attributes import AttributeProperty
from evennia.utils.utils import repeat


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


class ExtendedRoom:
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
        "autumn": (
            9 / months_per_year,
            12 / months_per_year,
        ),  # September - November
        "winter": (
            12 / months_per_year,
            3 / months_per_year,
        ),  # December - February
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

    @property
    def room_states(self):
        """
        Get all room_states set on this room.

        """
        return list(
            sorted(
                self.tags.get(
                    category=self.room_state_tag_category, return_list=True
                )
            )
        )

    # Methods

    def at_init(self):
        """Evennia hook. Start up repeating function whenever object loads into memory."""
        self._start_broadcast_repeat_task()

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
                if desc := descriptions.get(
                    f"desc_{roomstate}"
                ) or descriptions.get("{roomstate}_desc"):
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
