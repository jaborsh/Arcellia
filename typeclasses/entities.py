from django.conf import settings
from evennia.utils.utils import (
    dbref,
    dedent,
    make_iter,
    variable_from_module,
)

from typeclasses.entity_mixins import (
    clothing_mixin,
    cooldown_mixin,
    equipment_mixin,
    feat_mixin,
    stat_mixin,
    trait_mixin,
)
from utils.text import grammarize
from world.characters import genders

from .objects import ObjectParent

_AT_SEARCH_RESULT = variable_from_module(
    *settings.SEARCH_AT_RESULT.rsplit(".", 1)
)


class Entity(
    ObjectParent,
    clothing_mixin.ClothingMixin,
    cooldown_mixin.CooldownMixin,
    equipment_mixin.EquipmentMixin,
    feat_mixin.FeatMixin,
    stat_mixin.StatMixin,
    trait_mixin.TraitMixin,
):
    appearance_template = dedent(
        """
        {desc}
        {health}
        {equipment}
        
        {clothing}
        """
    )

    def at_object_creation(self):
        self.init_stats()  # StatMixin

    # Hooks
    def is_alive(self):
        return self.health.current > 0

    def at_damage(self, value):
        self.health.current -= value
        if not self.is_alive():
            self.at_die()

    def at_die(self):
        self.location.msg_contents("$You() $conj(die)!", from_obj=self)

    def at_restore(self):
        self.health.current = self.health.max
        self.mana.current = self.mana.max
        self.stamina.current = self.stamina.max

    def at_pre_emote(self, message, **kwargs):
        """
        Before the object emotes something.

        This hook is by default used by the 'emote' command.

        Args:
            message (str): The suggested emote text.

        Keyword Args:
            emote_type (str): The type of emote being performed. The options
                              are 'emote', 'omote', or 'pmote'. Defaults to
                              'emote'.
        """
        emote_type = kwargs.get("emote_type", "emote")
        if emote_type == "omote":
            message = message.split(" ;", 1)
            message = f" {self}".join(message)

        return grammarize(message)

    def at_pre_say(self, message, **kwargs):
        """
        Before the object says something.

        This hook is by default used by the 'say' and 'whisper'
        commands as used by this command it is called before the text
        is said/whispered and can be used to customize the outgoing
        text from the object. Returning `None` aborts the command.

        Args:
            message (str): The suggested say/whisper text spoken by self.
        Keyword Args:
            whisper (bool): If True, this is a whisper rather than
                a say. This is sent by the whisper command by default.
                Other verbal commands could use this hook in similar
                ways.
            receivers (Object or iterable): If set, this is the target or targets for the
                say/whisper.

        Returns:
            message (str): The (possibly modified) text to be spoken.

        """  # noqa: E501
        return grammarize(message)

    def at_say(
        self,
        message,
        msg_self=None,
        msg_location=None,
        receivers=None,
        msg_receivers=None,
        **kwargs,
    ):
        """
        Display the actual say (or whisper) of self.

        This hook should display the actual say/whisper of the object in its
        location.  It should both alert the object (self) and its
        location that some text is spoken.  The overriding of messages or
        `mapping` allows for simple customization of the hook without
        re-writing it completely.

        Args:
            message (str): The message to convey.
            msg_self (bool or str, optional): If boolean True, echo `message` to self. If a string,
                return that message. If False or unset, don't echo to self.
            msg_location (str, optional): The message to echo to self's location.
            receivers (Object or iterable, optional): An eventual receiver or receivers of the
                message (by default only used by whispers).
            msg_receivers(str): Specific message to pass to the receiver(s). This will parsed
                with the {receiver} placeholder replaced with the given receiver.
        Keyword Args:
            whisper (bool): If this is a whisper rather than a say. Kwargs
                can be used by other verbal commands in a similar way.
            mapping (dict): Pass an additional mapping to the message.

        Notes:


            Messages can contain {} markers. These are substituted against the values
            passed in the `mapping` argument.

                msg_self = 'You say: "{speech}"'
                msg_location = '{object} says: "{speech}"'
                msg_receivers = '{object} whispers: "{speech}"'

            Supported markers by default:
                {self}: text to self-reference with (default 'You')
                {speech}: the text spoken/whispered by self.
                {object}: the object speaking.
                {receiver}: replaced with a single receiver only for strings meant for a specific
                    receiver (otherwise 'None').
                {all_receivers}: comma-separated list of all receivers,
                                 if more than one, otherwise same as receiver
                {location}: the location where object is.

        """  # noqa: E501

        def format_receivers(self, receiver, receivers, type):
            """Format the receivers' list into a readable string."""
            if type == "self":
                display_names = [
                    recv.get_display_name(self) for recv in receivers
                ]
            elif type == "receiver":
                display_names = [
                    (
                        "you"
                        if character == receiver
                        else character.get_display_name(receiver)
                    )
                    for character in receivers
                ]
            else:
                display_names = [
                    recv.get_display_name(receiver) for recv in receivers
                ]

            if len(display_names) > 2:
                return (
                    ", ".join(display_names[:-2])
                    + ", and "
                    + " and ".join(display_names[-2:])
                )
            elif len(display_names) == 2:
                return " and ".join(display_names)
            elif display_names:
                return display_names[0]
            return ""

        def construct_self_message(
            self,
            receivers,
            location,
            message,
            msg_self,
            msg_type,
            custom_mapping,
        ):
            all_receivers = format_receivers(self, self, receivers, "self")
            self_mapping = {
                "self": "You",
                "to": " to " if receivers else "",
                "object": self.get_display_name(self),
                "location": location.get_display_name(self)
                if location
                else None,
                "receiver": None,
                "all_receivers": all_receivers,
                "speech": message,
            }
            self_mapping.update(custom_mapping)
            self.msg(
                text=(msg_self.format_map(self_mapping), {"type": msg_type}),
                from_obj=self,
                wrap="say",
                width=kwargs.get("width", None),
            )

        def construct_receiver_messages(
            self, receivers, location, message, msg_receivers, msg_type
        ):
            for receiver in receivers:
                all_receivers = format_receivers(
                    self, receiver, receivers, "receiver"
                )
                receiver_mapping = {
                    "self": "You",
                    "to": " to " if receivers else "",
                    "object": self.get_display_name(receiver),
                    "location": (
                        location.get_display_name(receiver)
                        if location
                        else None
                    ),
                    "receiver": None,
                    "all_receivers": all_receivers,
                    "speech": message,
                }
                receiver.msg(
                    text=(
                        msg_receivers.format_map(receiver_mapping),
                        {"type": msg_type},
                    ),
                    from_obj=self,
                    wrap="say",
                    width=kwargs.get("width", None),
                )

        def construct_location_message(
            self,
            receivers,
            location,
            message,
            msg_location,
            msg_type,
            custom_mapping,
        ):
            exclude = [self]
            if receivers:
                exclude.extend(receivers)

            for individual in location.contents:
                if individual in exclude:
                    continue
                all_receivers = format_receivers(
                    self, individual, receivers, "location"
                )
                location_mapping = {
                    "self": "You",
                    "object": self,
                    "to": " to " if receivers else "",
                    "location": location,
                    "all_receivers": all_receivers,
                    "receiver": None,
                    "speech": message,
                }
                location_mapping.update(custom_mapping)
                individual.msg(
                    text=(
                        msg_location.format_map(location_mapping),
                        {"type": msg_type},
                    ),
                    from_obj=self,
                    wrap="say",
                    width=kwargs.get("width", None),
                )

        msg_type = kwargs.get("msg_type", "say")
        if msg_type == "say":
            msg_self = (
                '{self} say{to}{all_receivers}, "|n{speech}|n"'
                if msg_self is True
                else msg_self
            )
            msg_location = (
                msg_location or '{object} says{to}{all_receivers}, "{speech}"'
            )
            msg_receivers = (
                msg_receivers or '{object} says{to}{all_receivers}, "{speech}"'
            )

            custom_mapping = kwargs.get("mapping", {})
            receivers = make_iter(receivers) if receivers else []
            location = self.location
        elif msg_type == "whisper":
            msg_self = (
                '{self} whisper to {all_receivers}, "|n{speech}|n"'
                if msg_self is True
                else msg_self
            )
            msg_receivers = msg_receivers or '{object} whispers, "|n{speech}|n"'
            custom_mapping = kwargs.get("mapping", {})
            msg_location = None
            location = None
        if msg_self:
            construct_self_message(
                self,
                receivers,
                location,
                message,
                msg_self,
                msg_type,
                custom_mapping,
            )
        if receivers and msg_receivers:
            construct_receiver_messages(
                self, receivers, location, message, msg_receivers, msg_type
            )
        if location and msg_location:
            construct_location_message(
                self,
                receivers,
                location,
                message,
                msg_location,
                msg_type,
                custom_mapping,
            )

    # Appearance
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

        return self.appearance_template.format(
            desc=self.get_display_desc(looker, **kwargs),
            health=self.get_display_health(looker, **kwargs),
            equipment=self.get_display_equipment(looker, **kwargs),
            clothing=self.get_display_clothing(looker, **kwargs),
        ).strip()

    def get_display_desc(self, looker, **kwargs):
        """
        Get the 'desc' component of the object description. Called by `return_appearance`.

        Args:
            looker (DefaultObject): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The desc display string.

        """
        return self.db.desc or "You see nothing special."

    def get_display_health(self, looker, **kwargs):
        HEALTH_MAP = {
            0: "They are |xlifeless|n.",
            1: "They are |#ff0000barely clinging to life|n.",
            10: "They are |#ff3300critically wounded|n.",
            20: "They are |#ff6600severely injured|n.",
            30: "They are |#ff9933gravely hurt|n.",
            40: "They are |#ffcc00injured|n.",
            50: "They are |#ffff00wounded|n.",
            60: "They are |#ccff00hurt|n.",
            70: "They have |#99ff00some small cuts|n.",
            80: "They are |#66ff00bruised and scraped|n.",
            90: "They are |#33ff00lightly scuffed|n.",
            99: "They have |#1aff00a few scratches|n.",
            100: "They are |#00ff00in perfect condition|n.",
        }

        percentage = self.health.percent(formatting=None)
        for threshold, display in HEALTH_MAP.items():
            if percentage <= threshold:
                return f"{display}"
        return "They appear |xunknown|n."

    def get_display_equipment(self, looker, **kwargs):
        """
        Returns a formatted string representing the equipment of the entity.

        Args:
            looker (Entity): The entity that is looking at the equipment.
            **kwargs: Additional keyword arguments.

        Returns:
            str: A formatted string representing the equipment of the entity.

        """

        def _filter_visible(obj_list):
            return [
                obj
                for obj in obj_list
                if obj != looker and obj.access(looker, "view")
            ]

        equipment = _filter_visible(self.equipment.all())
        if not equipment:
            return ""

        string = "|wEquipment:|n"
        max_position = (
            max([len(item.position) for item in equipment]) + 8
            if equipment
            else 0
        )

        for item in equipment:
            spaces = " " * (max_position - len(f" <worn {item.position}>"))
            line = f" |x<{item.position}>|n{spaces} {item.get_display_name(looker)}"
            string += f"\n{line}"

        return string

    def get_display_clothing(self, looker, **kwargs):
        """
        Returns a formatted string representation of the clothing items worn by the entity.

        Args:
            looker (Entity): The entity observing the clothing items.

        Returns:
            str: A formatted string representation of the clothing items.

        """

        def _filter_visible(obj_list):
            return [
                obj
                for obj in obj_list
                if obj != looker and obj.access(looker, "view")
            ]

        clothing = _filter_visible(self.clothing.all())
        if not clothing:
            return ""

        string = "|wClothing:|n"
        max_position = (
            max([len(item.position) for item in clothing]) + 8
            if clothing
            else 0
        )

        for item in clothing:
            spaces = " " * (max_position - len(f" <worn {item.position}>"))
            if item.covered_by and looker is not self:
                continue

            line = f" |x<worn {item.position}>|n{spaces} {item.get_display_name(looker)}"
            if item.covered_by:
                line += " |x(hidden)|n"
            string += f"\n{line}"

        return string

    def get_pronoun(self, regex_match):
        """
        Get pronoun from the pronoun marker in the text. This is used as
        the callable for the re.sub function.

        Args:
            regex_match (MatchObject): the regular expression match.

        Notes:
            - `|s`, `|S`: Subjective form: he, she, it, He, She, It, They
            - `|o`, `|O`: Objective form: him, her, it, Him, Her, It, Them
            - `|p`, `|P`: Possessive form: his, her, its, His, Her, Its, Their
            - `|a`, `|A`: Absolute Possessive form: his, hers, its, His, Hers, Its, Theirs

        """  # noqa: E501
        typ = regex_match.group()[1]  # "s", "O" etc
        gender = self.gender.value
        pronoun = genders._GENDER_PRONOUN_MAP[gender][typ.lower()]
        return pronoun.capitalize() if typ.isupper() else pronoun

    def handle_search_results(self, searchdata, results, **kwargs):
        """
        This method is called by the search method to allow for handling of the final search result.

        Args:
            searchdata (str): The original search criterion (potentially modified by
                `get_search_query_replacement`).
            results (list): The list of results from the search.
            **kwargs (any): These are the same as passed to the `search` method.

        Returns:
            Object, None or list: Normally this is a single object, but if `quiet=True` it should be
            a list.  If quiet=False and we have to handle a no/multi-match error (directly messaging
            the user), this should return `None`.

        """
        if kwargs.get("quiet"):
            # don't care about no/multi-match errors, just return list of whatever we have
            return list(results)

        # handle any error messages, otherwise return a single result

        nofound_string = kwargs.get("nofound_string")
        multimatch_string = kwargs.get("multimatch_string")
        return_quantity = kwargs.get("return_quantity")
        return_type = kwargs.get("return_type")

        return _AT_SEARCH_RESULT(
            results,
            self,
            query=searchdata,
            nofound_string=nofound_string,
            multimatch_string=multimatch_string,
            return_quantity=return_quantity,
            return_type=return_type,
        )

    def search(
        self,
        searchdata,
        global_search=False,
        use_nicks=True,
        typeclass=None,
        location=None,
        attribute_name=None,
        quiet=False,
        exact=False,
        candidates=None,
        use_locks=True,
        nofound_string=None,
        multimatch_string=None,
        use_dbref=None,
        tags=None,
        stacked=0,
        return_quantity=1,
        return_type=None,
    ):
        """
        Search for objects based on the given search criteria.

        Args:
            searchdata (str): The search criteria.
            global_search (bool, optional): If True, perform a global search. Defaults to False.
            use_nicks (bool, optional): If True, use nicknames in the search. Defaults to True.
            typeclass (str, optional): The typeclass of the objects to search for. Defaults to None.
            location (str, optional): The location of the objects to search for. Defaults to None.
            attribute_name (str, optional): The name of the attribute to search for. Defaults to None.
            quiet (bool, optional): If True, suppress output messages. Defaults to False.
            exact (bool, optional): If True, perform an exact match search. Defaults to False.
            candidates (list, optional): A list of candidate objects to search within. Defaults to None.
            use_locks (bool, optional): If True, check object locks during the search. Defaults to True.
            nofound_string (str, optional): The message to display when no objects are found. Defaults to None.
            multimatch_string (str, optional): The message to display when multiple objects are found. Defaults to None.
            use_dbref (bool, optional): If True, allow searching by dbref. Defaults to None.
            tags (list, optional): A list of tags to search for. Defaults to None.
            stacked (int, optional): The number of stacked objects to return. Defaults to 0.
            return_quantity (int, optional): The number of objects to return. Defaults to 1.
            return_type (str, optional): The type of object to return. Defaults to None.

        Returns:
            list or object or None: The search results based on the given criteria.
        """
        # store input kwargs for sub-methods (this must be done first in this method)
        input_kwargs = {
            key: value
            for key, value in locals().items()
            if key not in ("self", "searchdata")
        }

        # replace incoming searchdata string with a potentially modified version
        searchdata = self.get_search_query_replacement(
            searchdata, **input_kwargs
        )

        # handle special input strings, like "me" or "here".
        should_return, searchdata = self.get_search_direct_match(
            searchdata, **input_kwargs
        )
        if should_return:
            # we got an actual result, return it immediately
            return [searchdata] if quiet else searchdata

        # if use_dbref is None, we use a lock to determine if dbref search is allowed
        use_dbref = (
            self.locks.check_lockstring(self, "_dummy:perm(Builder)")
            if use_dbref is None
            else use_dbref
        )

        # convert tags into tag tuples suitable for query
        tags = [
            (tagkey, tagcat[0] if tagcat else None)
            for tagkey, *tagcat in make_iter(tags or [])
        ]

        # always use exact match for dbref/global searches
        exact = True if global_search or dbref(searchdata) else exact

        # get candidates
        candidates = self.get_search_candidates(searchdata, **input_kwargs)

        # do the actual search
        results = self.get_search_result(
            searchdata,
            attribute_name=attribute_name,
            typeclass=typeclass,
            candidates=candidates,
            exact=exact,
            use_dbref=use_dbref,
            tags=tags,
        )

        # filter out objects we are not allowed to search
        if use_locks:
            results = [
                x
                for x in list(results)
                if x.access(self, "search", default=True)
            ]

        # handle stacked objects
        is_stacked, results = self.get_stacked_results(results, **input_kwargs)
        if is_stacked:
            # we have a stacked result, return it immediately (a list)
            return results

        # handle the end (unstacked) results, returning a single object, a list or None
        return self.handle_search_results(searchdata, results, **input_kwargs)
