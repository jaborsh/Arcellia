from django.conf import settings
from evennia.commands.default import comms as default_comms
from evennia.utils.ansi import strip_ansi
from evennia.utils.utils import class_from_module, strip_unsafe_input
from server.conf.logger import tail_log_file

from commands.command import Command

COMMAND_DEFAULT_CLASS = class_from_module(settings.COMMAND_DEFAULT_CLASS)
CHANNEL_DEFAULT_TYPECLASS = class_from_module(
    settings.BASE_CHANNEL_TYPECLASS, fallback=settings.FALLBACK_CHANNEL_TYPECLASS
)
__all__ = (
    "CmdChannel",
    "CmdLast",
    "CmdTune",
)


def search_channel(self, channelname, exact=False, handle_errors=True):
    """
    Helper function for searching for a single channel with some error
    handling.

    Args:
        channelname (str): Name, alias #dbref or partial name/alias to search
            for.
        exact (bool, optional): If an exact or fuzzy-match of the name should be done.
            Note that even for a fuzzy match, an exactly given, unique channel name
            will always be returned.
        handle_errors (bool): If true, use `self.msg` to report errors if
            there are non/multiple matches. If so, the return will always be
            a single match or None.
    Returns:
        object, list or None: If `handle_errors` is `True`, this is either a found Channel
            or `None`. Otherwise it's a list  of zero, one or more channels found.
    Notes:
        The 'listen' and 'control' accesses are checked before returning.

    """
    caller = self.caller
    # first see if this is a personal alias
    channelname = caller.nicks.get(key=channelname, category="channel") or channelname

    # always try the exact match first.
    channels = CHANNEL_DEFAULT_TYPECLASS.objects.channel_search(channelname, exact=True)

    if not channels and not exact:
        # try fuzzy matching as well
        channels = CHANNEL_DEFAULT_TYPECLASS.objects.channel_search(
            channelname, exact=exact
        )

    # check permissions
    channels = [
        channel
        for channel in channels
        if channel.access(caller, "listen") or channel.access(caller, "control")
    ]

    if handle_errors:
        if not channels:
            self.msg(
                f"No channel found matching '{channelname}' "
                "(could also be due to missing access)."
            )
            return None
        elif len(channels) > 1:
            self.msg(
                f"Multiple possible channel matches/alias for '{channelname}':\n"
                + ", ".join(chan.key for chan in channels)
            )
            return None
        return channels[0]
    else:
        if not channels:
            return []
        elif len(channels) > 1:
            return list(channels)
        return [channels[0]]


class CmdChannel(default_comms.CmdChannel):
    """
    Usage: channel            (show all subscription)
           channelname <msg>

    This sends a message to the channel. Note that you will rarely use this
    command like this; instead you can use the alias
    """

    ADMIN_DOCSTRING = """
        Usage: channel        (show all channels)
               channelname <msg>
               channel/create channelname[;alias;alias[:typeclass]] [= description]
               channel/destroy channelname [= reason]
               channel/lock channelname = lockstring
               channel/unlock channelname = lockstring
               channel/ban channelname   (list bans)
               channel/ban[/quiet] channelname[, channelname, ...] = subscribername [: reason]
               channel/unban[/quiet] channelname[, channelname, ...] = subscribername
               channel/boot[/quiet] channelname[,channelname,...] = subscribername [: reason]

        # subtopics

        ## sending

        Usage: channelname <msg>

        This sends a message to the channel. Note that you will rarely use this
        command like this; instead you can use the alias

        ## who

        Usage: channel/who channelname

        List the channel's subscribers. Shows who are currently offline or are
        muting the channel. Subscribers who are 'muting' will not see messages sent
        to the channel.

        ## create and destroy

        Usage: channel/create channelname[;alias;alias[:typeclass]] [= description]
            channel/destroy channelname [= reason]

        Creates a new channel (or destroys one you control). You will automatically
        join the channel you create and everyone will be kicked and loose all aliases
        to a destroyed channel.

        ## lock and unlock

        Usage: channel/lock channelname = lockstring
            channel/unlock channelname = lockstring

        Note: this is an admin command.

        A lockstring is on the form locktype:lockfunc(). Channels understand three
        locktypes:
            listen - who may listen or join the channel.
            send - who may send messages to the channel
            control - who controls the channel. This is usually the one creating
                the channel.

        Common lockfuncs are all() and perm(). To make a channel everyone can
        listen to but only builders can talk on, use this:

            listen:all()
            send: perm(Builders)

        ## boot and ban

        Usage:
            channel/boot[/quiet] channelname[,channelname,...] = subscribername [: reason]
            channel/ban channelname[, channelname, ...] = subscribername [: reason]
            channel/unban channelname[, channelname, ...] = subscribername
            channel/unban channelname
            channel/ban channelname    (list bans)

        Booting will kick a named subscriber from channel(s) temporarily. The
        'reason' will be passed to the booted user. Unless the /quiet switch is
        used, the channel will also be informed of the action. A booted user is
        still able to re-connect, but they'll have to set up their aliases again.

        Banning will blacklist a user from (re)joining the provided channels. It
        will then proceed to boot them from those channels if they were connected.
        The 'reason' and `/quiet` works the same as for booting.

        Example:
            boot mychannel1 = EvilUser : Kicking you to cool down a bit.
            ban mychannel1,mychannel2= EvilUser : Was banned for spamming.
        """

    key = "channel"
    aliases = ["chan", "channels"]
    locks = (
        "cmd:not pperm(channel_banned);"
        "admin:perm(Admin);"
        "manage:perm(Admin);"
        "changelocks:perm(Developer);"
        "send:all();"
    )
    switch_options = (
        "all",
        "create",
        "destroy",
        "desc",
        "lock",
        "unlock",
        "mute",
        "unmute" "ban",
        "boot",
        "unban",
        "who",
    )

    # disable this in child command classes if wanting on-character channels
    account_caller = True

    def get_help(self, caller, cmdset):
        """
        Return the help message for this command and this caller.

        Returns:
            docstring (str): the help text provided for this command.
        """
        if caller.check_permstring("Admin"):
            return self.ADMIN_DOCSTRING

        return self.__doc__

    def msg_channel(self, channel, message, **kwargs):
        """
        Send a message to a given channel. This will check the 'send'
        permission on the channel.

        Args:
            channel (Channel): The channel to send to.
            message (str): The message to send.
            **kwargs: Unused by default. These kwargs will be passed into
                all channel messaging hooks for custom overriding.

        """
        if not channel.access(self.caller, "send"):
            self.caller.msg(
                f"You are not allowed to send messages to channel {channel}"
            )
            return

        # avoid unsafe tokens in message
        message = strip_unsafe_input(message, self.session)

        channel.msg(message, senders=self.caller, **kwargs)

    def mute_channel(self, channel):
        """
        Temporarily mute a channel.

        Args:
            channel (Channel): The channel to alias.

        Returns:
            bool, str: True, None if muting successful. If False,
                       error string.
        """

        if channel.mute(self.caller):
            return True, ""

        return False, f"Channel {channel.key} is already muted."

    def unmute_channel(self, channel):
        """
        Unmute a channel.
        """

        if channel.unmute(self.caller):
            return True, ""

        return False, f"Channel {channel.key} is already unmuted."


class CmdLast(Command):
    """
    Usage: last <channel>

    View a channel's history.
    """

    key = "last"
    locks = "cmd:all()"
    help_category = "comms"

    def func(self):
        args = self.args.strip().split(" ", 1)
        channel = search_channel(self, args[0])
        log_file = channel.get_log_filename()

        def send_msg(lines):
            header = f"|GHistory of {channel.key} Channel|n"
            border = "\n" + "|G" + "-" * len(strip_ansi(header)) + "|n"
            message = (
                header
                + border
                + "\n|C"
                + "".join(
                    line.split("[-]", 1)[1] if "[-]" in line else line for line in lines
                )
                + "|G"
                + border
                + "|n"
            )

            return self.msg(message)

        # asynchronously tail the log file
        tail_log_file(log_file, 0, 10, callback=send_msg)


class CmdTune(Command):
    """
    Usage: tune <channel>

    Subscribe to a channel.
    """

    key = "tune"
    aliases = ["sub"]
    locks = "cmd:all()"
    help_category = "comms"

    def func(self):
        caller = self.caller
        channel = search_channel(self, self.args.strip())

        # Disconnect from the channel.
        if channel.has_connection(caller):
            result = channel.disconnect(caller)
            return result, "" if result else f"You cannot tune out of {channel.key}."

        # Connect to the channel.
        result = channel.connect(caller)
        return result, "" if result else f"You cannot tune into {channel.key}."
