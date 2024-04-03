"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from evennia.objects.objects import DefaultCharacter
from evennia.utils.utils import lazy_property, make_iter, to_str
from handlers import quests, traits
from server.conf import logger
from utils.text import grammarize, wrap
from world.characters import backgrounds, genders

from .mixins.living import LivingMixin
from .objects import ObjectParent


class Character(LivingMixin, ObjectParent, DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_post_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the prelogout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    prelogout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """

    def at_object_creation(self):
        self.locks.add("msg:all()")

    @lazy_property
    def appearance(self):
        return traits.TraitHandler(self, db_attribute_key="appearance")

    @lazy_property
    def quests(self):
        return quests.QuestHandler(self, db_attribute_key="quests")

    @property
    def background(self):
        return self.traits.get("background")

    @background.setter
    def background(self, value):
        if isinstance(value, str):
            value = backgrounds.BACKGROUND_MAP.get(value)
        elif isinstance(value, backgrounds.CharacterBackground):
            pass
        else:
            raise TypeError("Background must be a string or a Background class.")

        self.background.value = value

    # Hooks
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
                display_names = [recv.get_display_name(self) for recv in receivers]
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
                display_names = [recv.get_display_name(receiver) for recv in receivers]

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
            self, receivers, location, message, msg_self, msg_type, custom_mapping
        ):
            all_receivers = format_receivers(self, self, receivers, "self")
            self_mapping = {
                "self": "You",
                "to": " to " if receivers else "",
                "object": self.get_display_name(self),
                "location": location.get_display_name(self) if location else None,
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
                all_receivers = format_receivers(self, receiver, receivers, "receiver")
                receiver_mapping = {
                    "self": "You",
                    "to": " to " if receivers else "",
                    "object": self.get_display_name(receiver),
                    "location": (
                        location.get_display_name(receiver) if location else None
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
                self, receivers, location, message, msg_self, msg_type, custom_mapping
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

    # Methods
    def msg(self, text=None, from_obj=None, session=None, options=None, **kwargs):
        """
        Emits something to a session attached to the object.

        Args:
            text (str or tuple, optional): The message to send. This
                is treated internally like any send-command, so its
                value can be a tuple if sending multiple arguments to
                the `text` oob command.
            from_obj (obj or list, optional): object that is sending. If
                given, at_msg_send will be called. This value will be
                passed on to the protocol. If iterable, will execute hook
                on all entities in it.
            session (Session or list, optional): Session or list of
                Sessions to relay data to, if any. If set, will force send
                to these sessions. If unset, who receives the message
                depends on the MULTISESSION_MODE.
            options (dict, optional): Message-specific option-value
                pairs. These will be applied at the protocol level.
        Keyword Args:
            any (string or tuples): All kwarg keys not listed above
                will be treated as send-command names and their arguments
                (which can be a string or a tuple).
            wrap (string): The type of wrap

        Notes:
            `at_msg_receive` will be called on this Object.
            All extra kwargs will be passed on to the protocol.

        """
        # try send hooks
        if from_obj:
            for obj in make_iter(from_obj):
                try:
                    obj.at_msg_send(text=text, to_obj=self, **kwargs)
                except Exception:
                    logger.log_trace()
        kwargs["options"] = options
        try:
            if not self.at_msg_receive(text=text, from_obj=from_obj, **kwargs):
                # if at_msg_receive returns false, we abort message to this object
                return
        except Exception:
            logger.log_trace()

        if text is not None:
            if not (isinstance(text, str) or isinstance(text, tuple)):
                # sanitize text before sending across the wire
                try:
                    text = to_str(text)
                except Exception:
                    text = repr(text)

            if text and isinstance(text, tuple):
                text = (
                    genders._RE_GENDER_PRONOUN.sub(self.get_pronoun, text[0]),
                    *text[1:],
                )
            else:
                text = genders._RE_GENDER_PRONOUN.sub(self.get_pronoun, text)

            if kwargs.get("wrap") == "say":
                msg = text[0]
                pre_text = msg.split('"')[0] + '"'
                msg = '"'.join(msg.split('"')[1:])
                msg = wrap(msg, text_width=kwargs.get("width", None), pre_text=pre_text)
                text = msg
            kwargs["text"] = text

        # relay to session(s)
        sessions = make_iter(session) if session else self.sessions.all()
        for session in sessions:
            session.data_out(**kwargs)

    def return_appearance(self, looker, **kwargs):
        """
        Returns the appearance of the character.

        Args:
            looker (object): The object that is looking at the character.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The appearance of the character.

        """
        if not looker:
            return ""

        # populate the appearance_template string.
        return self.format_appearance(
            self.appearance_template.format(
                desc=self.get_display_desc(looker, **kwargs),
                things=self.get_display_things(looker, **kwargs),
            ),
            looker,
            **kwargs,
        )
