"""
Channel

The channel class represents the out-of-character chat-room usable by
Accounts in-game. It is mostly overloaded to change its appearance, but
channels can be used to implement many different forms of message
distribution systems.

Note that sending data to channels are handled via the CMD_CHANNEL
syscommand (see evennia.syscmds). The sending should normally not need
to be modified.

"""
import os

from django.conf import settings
from evennia.comms.comms import DefaultChannel
from server.conf import logger


class Channel(DefaultChannel):
    """
    Working methods:
        at_channel_creation() - called once, when the channel is created
        has_connection(account) - check if the given account listens to this channel
        connect(account) - connect account to this channel
        disconnect(account) - disconnect account from channel
        access(access_obj, access_type='listen', default=False) - check the
                    access on this channel (default access_type is listen)
        delete() - delete this channel
        message_transform(msg, emit=False, prefix=True,
                          sender_strings=None, external=False) - called by
                          the comm system and triggers the hooks below
        msg(msgobj, header=None, senders=None, sender_strings=None,
            persistent=None, online=False, emit=False, external=False) - main
                send method, builds and sends a new message to channel.
        tempmsg(msg, header=None, senders=None) - wrapper for sending non-persistent
                messages.
        distribute_message(msg, online=False) - send a message to all
                connected accounts on channel, optionally sending only
                to accounts that are currently online (optimized for very large sends)

    Useful hooks:
        channel_prefix() - how the channel should be
                  prefixed when returning to user. Returns a string
        format_senders(senders) - should return how to display multiple
                senders to a channel
        pose_transform(msg, sender_string) - should detect if the
                sender is posing, and if so, modify the string
        format_external(msg, senders, emit=False) - format messages sent
                from outside the game, like from IRC
        format_message(msg, emit=False) - format the message body before
                displaying it to the user. 'emit' generally means that the
                message should not be displayed with the sender's name.

        pre_join_channel(joiner) - if returning False, abort join
        post_join_channel(joiner) - called right after successful join
        pre_leave_channel(leaver) - if returning False, abort leave
        post_leave_channel(leaver) - called right after successful leave
        pre_send_message(msg) - runs just before a message is sent to channel
        post_send_message(msg) - called just after message was sent to channel

    """

    log_file = "channels/{channelname}/channel_{channelname}.log"

    def at_channel_creation(self):
        """
        Called once, when the channel is first created.

        """
        self.create_log_folder()

    def create_log_folder(self):
        """
        Creates a log folder for the channel.
        """
        chan_log_dir = f"{settings.CHANNEL_LOG_DIR}/{self.key.lower()}/"
        os.makedirs(chan_log_dir, exist_ok=True)

    def at_post_msg(self, message, **kwargs):
        """
        This is called after sending to *all* valid recipients. It is normally
        used for logging/channel history.

        Args:
            message (str): The message sent.
            **kwargs (any): Keywords passed on from `msg`, including `senders`.
        """

        # save channel history to log file
        log_file = self.get_log_filename()
        if log_file:
            senders = ",".join(sender.key for sender in kwargs.get("senders", []))
            senders = f"{senders}" if senders else ""
            if message.startswith(";"):
                senders += " "
                message = message[1:]
            else:
                senders += ": "
            message = f"{senders}{message}"
            logger.log_file(message, log_file)
