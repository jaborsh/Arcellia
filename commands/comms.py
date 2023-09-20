from django.conf import settings
from evennia.commands.default import comms as default_comms
from evennia.utils.ansi import strip_ansi
from evennia.utils.evmenu import ask_yes_no
from evennia.utils.utils import class_from_module
from server.conf import logger

from commands.command import Command

COMMAND_DEFAULT_CLASS = class_from_module(settings.COMMAND_DEFAULT_CLASS)
CHANNEL_DEFAULT_TYPECLASS = class_from_module(
    settings.BASE_CHANNEL_TYPECLASS, fallback=settings.FALLBACK_CHANNEL_TYPECLASS
)
__all__ = (
    "CmdChannel",
    "CmdObjectChannel",
    "CmdLast",
    "CmdTune",
)


class CmdChannel(default_comms.CmdChannel):
    """
    Usage: channel            (show all tuned channels)
           channels           (show all channels)
           <channel> <msg>    (send message to channel)

    This sends a message to the channel. Note that you will rarely use this
    command like this; instead you will use the channelname.
    """

    ADMIN_DOCSTRING = """
        Usage: channel                   (show all tuned channels)
               channels                  (show all channels)
               <channel> <msg>           (send message to channel)  

        This sends a message to the channel. Note that you will rarely use this
        command like this; instead you will use the channelname.

        Admin Usage: channel/desc <channel> <description>
                     channel/ban[/quiet] <channel> [player]
                     channel/unban[/quiet] <channel> [player]
                     channel/create <channel>  
                     channel/destroy <channel> 
                     channel/lock <channel> <lockstring>
                     channel/unlock <channel> <lockstring>
                     channel/mute <channel>    
                     channel/unmute <channel> 

        # subtopics

        ## ban and unban
        Usage: channel/ban[/quiet] <channel> [player]
               channel/unban[/quiet] <channel> [player]

        Ban or unban a player from a channel. If no player is given, list all bans.           

        ## create and destroy
        Usage: channel/create <channel>  (create channel)
               channel/destroy <channel> (destroy channel)

        Creates a new channel or destroys one you control. You will automatically
        join the channel you create and everyone will be kicked from a destroyed
        channel.

        ## lock and unlock
        Usage: channel/lock <channel> <lockstring>    (lock channel)
               channel/unlock <channel> <lockstring>  (unlock channel)

        Edit permissions associated with a channel.

        ## mute and unmute
        Usage: channel/mute <channel>    (mute channel)
               channel/unmute <channel>  (unmute channel)

        Muting silences all input from players. Admins are the only 
        individuals who can use a muted channel.
        """

    key = "channel"
    aliases = ["chan", "chans", "channels"]
    help_category = "General"
    locks = (
        "cmd:not pperm(channel_banned);"
        "admin:pperm(Admin);"
        "manage:pperm(Admin);"
        "changelocks:pperm(Developer);"
        "send:all();"
        "listen:all();"
    )

    switch_options = (
        "create",
        "destroy",
        "desc",
        "ban",
        "unban",
        "lock",
        "unlock",
        "mute",
        "unmute",
    )

    # disable this in child command classes if wanting in-character channel.
    account_caller = True

    def get_help(self, caller, cmdset):
        """Return admin or player docstring."""
        if caller.check_permstring("Admin"):
            return self.ADMIN_DOCSTRING

        return self.__doc__

    def func(self):
        """Main functionality of command."""
        caller = self.caller
        switches = self.switches
        channel_names = [name for name in self.lhslist if name]

        if self.cmdstring == "channels" or self.cmdstring == "chans" or not self.args:
            # show all available channels
            subscribed, available = self.list_channels()
            table = self.display_all_channels(subscribed, available)

            self.msg(f"\n|wAvailable channels|n:\n{table}")
            return

        if not channel_names:
            # empty arg show only subscribed channels
            subscribed, _ = self.list_channels()
            table = self.display_subbed_channels(subscribed)

            self.msg(f"\n|wTuned channels|n:\n{table}")
            return

        possible_lhs_message = ""
        if not self.rhs and self.args and " " in self.args:
            """
            Since we want to support messaging with `channel name text`, we
            need to check if the first 'channel name' is in fact 'channelname
            text' and if so, split it up into lhs and rhs.
            """
            no_rhs_channel_name = self.args.split(" ", 1)[0]
            possible_lhs_message = self.args[len(no_rhs_channel_name) :]
            if possible_lhs_message.strip() == "=":
                possible_lhs_message = ""
            channel_names.append(no_rhs_channel_name)

        if "create" in switches:
            # Create a channel
            if not self.access(caller, "changelocks"):
                self.msg("You are not allowed to create channels.")
                return

            config = self.lhs
            if not config:
                self.msg(
                    "Usage: channel/create <name>[;aliases][:typeclass] [= description]"
                )
                return

            name, *typeclass = config.rsplit(":", 1)
            typeclass = typeclass[0] if typeclass else None
            name, *aliases = name.rsplit(";")
            description = self.rhs or ""
            chan, err = self.create_channel(
                name, description, typeclass=typeclass, aliases=aliases
            )
            if chan:
                logger.log_info(f"{chan.key} channel created by {self.caller}.")
                self.msg(f"Created channel: '{chan.key}'.")
            else:
                self.msg(err)
            return

        channels = []
        errors = []
        for channel_name in channel_names:
            """
            Find a channel by fuzzy-matching. This also checks listen/control.
            """
            found_channels = self.search_channel(
                channel_name, exact=False, handle_errors=False
            )
            if not found_channels:
                errors.append(
                    f"No channel found matching '{channel_name}' "
                    "(could also be due to missing access)."
                )
            elif len(found_channels) > 1:
                errors.append(
                    f"Multiple possible channel matches for '{channel_name}':\n"
                    + ", ".join(chan.key for chan in found_channels)
                )
            else:
                channels.append(found_channels[0])

        if not channels:
            self.msg("\n".join(errors))
            return

        # We have found at least one channel.
        channel = channels[0]

        if not switches:
            if self.rhs:
                # send message to channel
                self.msg_channel(channel, self.rhs.strip())
            elif channel and possible_lhs_message:
                # called on the form channelname message without =
                self.msg_channel(channel, possible_lhs_message.strip())
            else:
                # send error message
                self.msg(f"Usage: {channel.key.lower()} <message>.")
            return

        elif "destroy" in switches:
            # Destroy a channel
            if not self.access(caller, "changelocks"):
                self.msg("You are not allowed to destroy channels.")
                return

            if not channel.access(caller, "control"):
                self.msg("You are not allowed to destroy this channel.")
                return

            reason = self.rhs or None

            def _perform_delete(caller, *args, **kwargs):
                self.destroy_channel(channel, message=reason)
                logger.log_info(f"{channel.key} channel destroyed by {self.caller}.")
                self.msg(f"Destroyed channel: '{channel.key}'.")

            ask_yes_no(
                caller,
                prompt=(
                    f"Are you sure you want to destroy the {channel.key} channel? "
                    "This will disconnect and remove all users. {options}?"
                ),
                yes_action=_perform_delete,
                no_action="Channel deletion aborted.",
                default="N",
            )

        elif "desc" in switches:
            # Set channel description

            if not self.access(caller, "manage"):
                self.msg("You are not allowed to set channel descriptions.")
                return

            if not channel.access(caller, "control"):
                self.msg("You are not allowed to set this channel's description.")
                return

            desc = self.args.strip().split(" ", 1)[1]
            if not desc:
                self.msg("Usage: channel/desc <channel> <description>")
                return

            self.set_desc(channel, desc)
            logger.log_info(f"{channel.key} channel description set by {self.caller}.")
            self.msg("Updated channel description.")

        elif "ban" in switches:
            # ban a user from channel
            if not self.access(caller, "admin"):
                self.msg("You are not allowed to ban users from channels.")
                return

            if not len(self.args.strip().split(" ", 1)) > 1:
                # view bans on channel
                if not channel.access(caller, "control"):
                    self.msg("You are not allowed to view this channel's bans.")
                    return

                bans = ["Channel bans:"]
                bans.extend(self.channel_list_bans(channel))
                self.msg("\n".join(bans))
                return

            target_str = self.args.split(" ", 1)[1]

            if not channel.access(caller, "control"):
                self.msg("You are not allowed to ban users from this channel.")
                return

            target = caller.search(target_str, candidates=channel.subscriptions.all())
            if not target:
                self.msg("No valid target found.")
                return

            success, err = self.ban_user(channel, target, quiet=False, reason="")
            if success:
                logger.log_info(
                    f"{target.key} banned from {channel.key} by {self.caller}."
                )
                self.msg(f"|rYou ban {target.key} from the {channel.key} channel.|n")
                target.msg(f"|rYou have lost access to the {channel.key} channel.|n")
            else:
                self.msg(f"Cannot ban {target.key} from channel {channel.key}: {err}")

        elif "unban" in switches:
            # unban a user from channel
            if not self.access(caller, "admin"):
                self.msg("You are not allowed to unban users from channels.")
                return

            if not len(self.args.strip().split(" ", 1)) > 1:
                self.msg("Usage: channel/unban <channel> <target>")
                return

            target_str = self.args.split(" ", 1)[1]

            if not channel.access(caller, "control"):
                self.msg("You are not allowed to unban users from this channel.")
                return

            banlists = []
            banlists.extend(channel.banlist)

            target = caller.search(target_str, candidates=channel.subscriptions.all())
            if not target:
                self.msg("No valid target found.")
                return

            success, err = self.unban_user(channel, target)
            if success:
                logger.log_info(
                    f"{target.key} unbanned from {channel.key} by {self.caller}."
                )
                self.msg(f"|gYou unban {target.key} from the {channel.key} channel.|n")
                target.msg(
                    f"|gYou have regained access to the {channel.key} channel.|n"
                )
            else:
                self.msg(f"Cannot unban {target.key} from channel {channel.key}: {err}")

        elif "lock" in switches:
            # add a lockstring to channel
            if not self.access(caller, "changelocks"):
                self.msg("You are not allowed to change channel lockstrings.")
                return

            if not channel.access(caller, "control"):
                self.msg("You are not allowed to change this channel's lockstring.")
                return

            lockstring = self.args.strip().split(" ", 1)[1]
            if not lockstring:
                self.msg("Usage: channel/lock <channel> <lockstring>")
                return

            success, err = self.set_lock(channel, lockstring)
            if success:
                logger.log_info(
                    f"{channel.key} channel lockstring {lockstring} set by {self.caller}."
                )
                self.msg("Added/updated lock on channel.")
            else:
                self.msg(f"Could not add/update lock: {err}")
            return

        elif "unlock" in switches:
            # remove a lockstring from channel
            if not self.access(caller, "changelocks"):
                self.msg("You are not allowed to change channel lockstrings.")
                return

            if not channel.access(caller, "control"):
                self.msg("You are not allowed to change this channel's lockstring.")
                return

            lockstring = self.args.strip().split(" ", 1)[1]
            if not lockstring:
                logger.log_info(
                    f"{channel.key} channel lockstring removed by {self.caller}."
                )
                self.msg("Usage: channel/unlock <channel> <lockstring>")
                return

            success, err = self.unset_lock(channel, lockstring)
            if success:
                logger.log_info(
                    f"{channel.key} channel lockstring {lockstring} removed by {self.caller}."
                )
                self.msg("Removed lock from channel.")
            else:
                self.msg(f"Could not remove lock: {err}")
            return

        elif "mute" in switches:
            # Mute the channel.
            channel.locks.remove("send:all()")
            channel.locks.add("send:perm(Admin)")
            logger.log_info(f"{channel.key} channel muted by {self.caller}.")
            self.msg(f"You mute the {channel.key} channel.")
            return

        elif "unmute" in switches:
            # Unmute the channel.
            channel.locks.remove("send:perm(Admin)")
            channel.locks.add("send:all()")
            logger.log_info(f"{channel.key} channel unmuted by {self.caller}.")
            self.msg(f"You unmute the {channel.key} channel.")
            return


# a channel-command parent for use with Characters/Objects.
class CmdObjectChannel(CmdChannel):
    account_caller = False


class CmdLast(Command):
    """
    Usage: last <channel>

    View a channel's recent history.
    """

    key = "last"
    locks = "cmd:all()"
    help_category = "General"

    account_caller = True

    def func(self):
        if not self.args:
            return self.msg("Usage: last <channel/tell>")

        # Get tell history
        if self.args.lower().strip() == "tell":
            return self.msg("Tell history has not been implemented yet.")

        channel = CmdChannel.search_channel(self, self.args.strip())
        log_file = channel.get_log_filename()

        def send_msg(lines):
            header = f"|G{channel.key} Channel History|n"
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
        logger.tail_log_file(log_file, 0, 10, callback=send_msg)


class CmdTune(Command):
    """
    Usage:
        tune <channel>

    This command allows the user to tune in or out of a communication channel.
    If the user is already tuned in to the channel, they will be tuned out.
    If the user is not tuned in to the channel, they will be tuned in.
    """

    key = "tune"
    locks = "cmd:all()"
    help_category = "General"

    account_caller = True

    def func(self):
        if not self.args:
            return self.msg("Usage: tune <channel>")

        channel = CmdChannel.search_channel(self, self.args.strip())
        if not channel:
            return

        # Check if account is tuned into the channel.
        if channel.has_connection(self.caller):
            success, err = CmdChannel.unsub_from_channel(self, channel)
            if success:
                self.msg(f"You tune out of the {channel.key} channel.")
            else:
                self.msg(err)
            return

        # Tune into the channel.
        success, err = CmdChannel.sub_to_channel(self, channel)
        if success:
            self.msg(f"You tune into the {channel.key} channel.")
        else:
            self.msg(err)
