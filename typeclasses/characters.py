"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
import os

from django.conf import settings
from evennia.objects.objects import DefaultCharacter
from evennia.utils.utils import lazy_property, make_iter, to_str
from server.conf import logger

from .objects import ObjectParent


class Character(ObjectParent, DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_post_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """

    def at_object_creation(self):
        self.create_log_folder()
        self.locks.add("msg:all()")

    def create_log_folder(self):
        """
        Creates a log folder for the character.
        """
        char_log_dir = f"{settings.CHARACTER_LOG_DIR}/{self.key.lower()}/"
        os.makedirs(char_log_dir, exist_ok=True)
        self.attributes.add("_log_folder", f"characters/{self.key.lower()}/")

    @lazy_property
    def log_folder(self):
        return self.attributes.get("_log_folder", f"characters/{self.key.lower()}/")

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

        """

        def format_receivers(receiver, receivers, type, self_obj):
            """Format the receivers' list into a readable string."""
            if type == "self":
                display_names = [recv.get_display_name(self_obj) for recv in receivers]
            elif type == "receiver":
                display_names = [
                    "you"
                    if character == receiver
                    else character.get_display_name(receiver)
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
            self_obj, receivers, location, message, msg_self, msg_type, custom_mapping
        ):
            all_receivers = format_receivers(self_obj, receivers, "self", self_obj)
            self_mapping = {
                "self": "You",
                "to": " to " if receivers else "",
                "object": self_obj.get_display_name(self_obj),
                "location": location.get_display_name(self_obj) if location else None,
                "receiver": None,
                "all_receivers": all_receivers,
                "speech": message,
            }
            self_mapping.update(custom_mapping)
            self_obj.msg(
                text=(msg_self.format_map(self_mapping), {"type": msg_type}),
                from_obj=self_obj,
            )

        def construct_receiver_messages(
            self_obj, receivers, location, message, msg_receivers, msg_type
        ):
            for receiver in receivers:
                all_receivers = format_receivers(
                    receiver, receivers, "receiver", self_obj
                )
                receiver_mapping = {
                    "self": "You",
                    "to": " to " if receivers else "",
                    "object": self_obj.get_display_name(receiver),
                    "location": location.get_display_name(receiver)
                    if location
                    else None,
                    "receiver": None,
                    "all_receivers": all_receivers,
                    "speech": message,
                }
                receiver.msg(
                    text=(
                        msg_receivers.format_map(receiver_mapping),
                        {"type": msg_type},
                    ),
                    from_obj=self_obj,
                )

        def construct_location_message(
            self_obj,
            receivers,
            location,
            message,
            msg_location,
            msg_type,
            custom_mapping,
        ):
            exclude = [self_obj]
            if receivers:
                exclude.extend(receivers)

            for individual in location.contents:
                if individual in exclude:
                    continue
                all_receivers = format_receivers(
                    individual, receivers, "location", self_obj
                )
                location_mapping = {
                    "self": "You",
                    "object": self_obj,
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
                    from_obj=self_obj,
                )

        msg_type = "say"
        msg_self = (
            '{self} say{to}{all_receivers}, "|n{speech}|n"'
            if msg_self is True
            else msg_self
        )
        msg_location = msg_location or '{object} says{to}{all_receivers}, "{speech}"'
        msg_receivers = msg_receivers or '{object} says{to}{all_receivers}, "{speech}"'

        custom_mapping = kwargs.get("mapping", {})
        receivers = make_iter(receivers) if receivers else []
        location = self.location

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
            kwargs["text"] = text

        # relay to session(s)
        sessions = make_iter(session) if session else self.sessions.all()
        for session in sessions:
            session.data_out(**kwargs)

        # relay to watcher(s)
        watchers = self.ndb._watchers or []
        for watcher in watchers:
            watcher.msg(text=kwargs["text"])
