import random

from django.conf import settings
from evennia.utils.utils import (
    dbref,
    lazy_property,
    make_iter,
    variable_from_module,
)

from handlers.appearance.living import LivingAppearanceHandler
from typeclasses.entity_mixins import (
    cooldown_mixin,
    equipment_mixin,
    feat_mixin,
    stat_mixin,
    trait_mixin,
)
from utils.text import grammarize

from .objects import Object

_AT_SEARCH_RESULT = variable_from_module(
    *settings.SEARCH_AT_RESULT.rsplit(".", 1)
)


class Entity(
    Object,
    cooldown_mixin.CooldownMixin,
    equipment_mixin.EquipmentMixin,
    feat_mixin.FeatMixin,
    stat_mixin.StatMixin,
    trait_mixin.TraitMixin,
):
    @lazy_property
    def appearance(self):
        return LivingAppearanceHandler(self)

    def at_object_creation(self):
        self.init_stats()  # StatMixin

    def at_object_post_spawn(self, prototype=None):
        spawns = self.attributes.get("spawn", {})
        if spawns:
            experience = spawns.get("experience", 0)
            if isinstance(experience, tuple):
                self.experience.current = random.randint(*experience)
            else:
                self.experience.current = experience
        super().at_object_post_spawn(prototype=prototype)

    def basetype_setup(self):
        """
        Setup character-specific security.

        You should normally not need to overload this, but if you do,
        make sure to reproduce at least the two last commands in this
        method (unless you want to fundamentally change how a
        Character object works).

        """
        super().basetype_setup()
        self.locks.add(
            ";".join(
                [
                    "attack:true()",  # attacks against this object
                    "call:false()",  # allow to call commands on this object
                    "get:false()",  # pick up the character
                    "teleport:perm(Admin)",  # teleport character
                    "teleport_here:perm(Admin)",  # teleport character here
                    "tell:all()",  # allow to tell the character
                ]
            )  # noone can pick up the character
        )  # no commands can be called on character from outside

    # Hooks
    def is_alive(self):
        return self.health.current > 0

    def at_damage(self, value):
        self.health.current -= value
        if not self.is_alive():
            self.at_die()

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
                and x.access(self, "view", default=True)
            ]

        # handle stacked objects
        is_stacked, results = self.get_stacked_results(results, **input_kwargs)
        if is_stacked:
            # we have a stacked result, return it immediately (a list)
            return results

        # handle the end (unstacked) results, returning a single object, a list or None
        return self.handle_search_results(searchdata, results, **input_kwargs)
