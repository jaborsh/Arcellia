import re
import time

from evennia.commands.default import account, admin, batchprocess, building
from evennia.server.models import ServerConfig
from server.conf import logger

from commands.command import Command

__all__ = (
    "CmdBan",
    "CmdUnban",
    "CmdBatchCommands",
    "CmdBatchCode",
    "CmdBoot",
    "CmdListCmdSets",
    "CmdQuell",
    "CmdScripts",
    "CmdSetPassword",
    "CmdSetPerm",
)


# regex matching IP addresses with wildcards, eg. 233.122.4.*
IPREGEX = re.compile(r"[0-9*]{1,3}\.[0-9*]{1,3}\.[0-9*]{1,3}\.[0-9*]{1,3}")


def list_bans(cmd, banlist):
    """
    Helper function to display a list of active bans. Input argument
    is the banlist read into the two commands ban and unban below.

    Args:
        cmd (Command): Instance of the Ban command.
        banlist (list): List of bans to list.
    """
    if not banlist:
        return "No active bans were found."

    table = cmd.styled_table("|wid", "|wname/ip", "|wdate", "|wreason")
    for inum, ban in enumerate(banlist):
        table.add_row(str(inum + 1), ban[0] and ban[0] or ban[1], ban[3], ban[4])
    return f"|wActive bans:|n\n{table}"


class CmdBan(Command):
    """
    Command to ban a player or IP address.

    Usage:
      ban <name or IP>[:reason] - Bans a player or IP address.
      bans - Lists all current bans.

    Switches:
      ip - Bans an IP address.
      name - Bans a player by name.
    """

    key = "ban"
    aliases = ["bans"]
    locks = "pperm(Developer)"
    help_category = "Developer"

    def func(self):
        banlist = ServerConfig.objects.conf("server_bans") or []

        if not self.args or (
            self.switches
            and not any(switch in ("ip", "name") for switch in self.switches)
        ):
            self.msg(list_bans(self, banlist))
            return

        now = time.ctime()
        reason = ""
        if ":" in self.args:
            ban, reason = self.args.rsplit(":", 1)
        else:
            ban = self.args
        ban = ban.lower()

        ipban = IPREGEX.findall(ban)
        if ipban:
            typ = "IP"
            ban = ipban[0]
            ipregex = re.compile(ban.replace(".", "\.").replace("*", "[0-9]{1,3}"))
            bantup = ("", ban, ipregex, now, reason)
        else:
            typ = "Name"
            bantup = (ban, "", "", now, reason)

        ret = yield (f"Are you sure you want to {typ}-ban '|w{ban}|n' [Y]/N?")
        if str(ret).lower() in ("no", "n"):
            self.msg("Aborted.")
            return

        banlist.append(bantup)
        ServerConfig.objects.conf("server_bans", banlist)
        self.msg(f"{typ}-ban '|w{ban}|n' was added. Use |wunban|n to reinstate.")
        logger.log_sec(
            f"Banned {typ}: {ban.strip()} (Caller: {self.caller}, IP: {self.session.address})."
        )


class CmdUnban(Command):
    """
    Command to unban a player from the server.

    Usage:
      unban [ban_id]

    Arguments:
      ban_id - The ID of the ban to clear.

    This command allows developers to remove bans from the server's banlist.
    If no ban_id is provided, it will display the list of bans.
    """

    key = "unban"
    locks = "cmd:pperm(Developer)"
    help_category = "Developer"

    def func(self):
        banlist = ServerConfig.objects.conf("server_bans")

        if not self.args:
            self.msg(list_bans(self, banlist))
            return

        try:
            num = int(self.args)
        except ValueError:
            self.msg("You must supply a valid ban id to clear.")
            return

        if not banlist:
            self.msg("There are no bans to clear.")
        elif not 0 < num <= len(banlist):
            self.msg(f"Ban id |w{self.args}|n was not found.")
        else:
            ban = banlist[num - 1]
            value = " ".join(filter(None, ban[:2]))
            ret = yield (f"Are you sure you want to unban {num}: '|w{value}|n' [Y]/N?")
            if str(ret).lower() in ("n", "no"):
                self.msg("Aborted.")
                return

            del banlist[num - 1]
            ServerConfig.objects.conf("server_bans", banlist)
            self.msg(f"Cleared ban {num}: '{value}'")
            logger.log_sec(
                f"Unbanned: {value.strip()} (Caller: {self.caller}, IP: {self.session.address})."
            )


class CmdBatchCommands(batchprocess.CmdBatchCommands):
    """
    Syntax: batchcommands[/interactive] <python.path.to.file>

    Switch:
       interactive - this mode will offer more control when
                     executing the batch file, like stepping,
                     skipping, reloading etc.

    Runs batches of commands from a batch-cmd text file (*.ev).
    """

    key = "batchcommands"
    aliases = ["batchcommand", "batchcmd"]
    switch_options = ("interactive",)
    locks = "cmd:pperm(Developer)"
    help_category = "System"


class CmdBatchCode(batchprocess.CmdBatchCode):
    """
    Syntax: batchcode[/interactive] <python path to file>

    Switch:
       interactive - this mode will offer more control when
                     executing the batch file, like stepping,
                     skipping, reloading etc.
       debug - auto-delete all objects that has been marked as
               deletable in the script file (see example files for
               syntax). This is useful so as to to not leave multiple
               object copies behind when testing out the script.

    Runs batches of commands from a batch-code text file (*.py).
    """

    key = "batchcode"
    aliases = ["batchcodes"]
    switch_options = ("interactive", "debug")
    locks = "cmd:superuser()"
    help_category = "System"


class CmdBoot(admin.CmdBoot):
    """
    Syntax: boot[/switches] <target> [:reason]

    Switches:
      quiet - Silently boot without informing the account.
      sid   - Boot by session id instead of name or dbref.

    Boot an object from the server. If a reason is supplied, it will be echoed
    to the user unless /quiet is set.
    """

    locks = "cmd:pperm(Developer)"
    help_category = "System"


class CmdListCmdSets(building.CmdListCmdSets):
    """
    Syntax: cmdsets <obj>

    This displays all cmdsets assigned to a user. Defaults to yourself.
    """

    key = "cmdsets"
    locks = "cmd:pperm(Developer)"
    help_category = "System"


class CmdQuell(account.CmdQuell):
    """
    Syntax: quell
            unquell

    Normally the permission level of the account is used when puppeting a
    character/object to determine access. Queeling will switch the lock system
    to make use of the puppeted object's permissions instead. This is useful
    mainly for testing.

    Hierarchical permission quelling only works downwards, thus an account
    cannot use a higher-permission character to escalate their permission
    level.

    Use 'unquell' to revert to normal permissions.
    """

    locks = "cmd:pperm(Developer)"
    help_category = "System"


class CmdScripts(building.CmdScripts):
    """
    Syntax: script[/switches] [script-#dbref, key, script.path]
            script[/start||stop] <obj> = [<script.path or script-key>]

    Switches:
        start - start/unpause an existing script's timer.
        stop - stops an existing script's timer
        pause - pause a script's timer
        delete - deletes script. This will also stop the timer as needed

    Examples:
        script                            - list all scripts
        script foo.bar.Script             - create a new global Script
        script/pause foo.bar.Script       - pause global script
        script scriptname|#dbref          - examine named existing global script
        script/delete #dbref[-#dbref]     - delete script or range by #dbref

        script myobj =                    - list all scripts on object
        script myobj = foo.bar.Script     - create and assign script to object
        script/stop myobj = name|#dbref   - stop named script on object
        script/delete myobj = name|#dbref - delete script on object
        script/delete myobj =             - delete ALL scripts on object

    When given with an `<obj>` as left-hand-side, this creates and
    assigns a new script to that object. Without an `<obj>`, this
    manages and inspects global scripts.

    If no switches are given, this command just views all active
    scripts. The argument can be either an object, at which point it
    will be searched for all scripts defined on it, or a script name
    or #dbref. For using the /stop switch, a unique script #dbref is
    required since whole classes of scripts often have the same name.

    Use the `script` build-level command for managing scripts attached to
    objects.
    """

    key = "scripts"
    aliases = ["script"]
    locks = "cmd:perm(Developer)"
    help_category = "System"


class CmdSetPassword(Command):
    """
    Syntax: setpass <account> <password>

    Set an account's password.
    """

    key = "setpass"
    aliases = ["setpassword"]
    locks = "cmd:perm(Developer)"
    help_category = "System"


class CmdSetPerm(admin.CmdPerm):
    """
    Syntax: setperm[/switch] <object> [=<permission>[,<permission>,...]]
            setperm[/switch] *<account> [=<permission>[,<permission>,...]]

    Switches: account - set the permission on an account
              del     - delete the permission from the object

    This command manages individual permission strings on an object or account.
    If no permission is given, list all permissions.
    """

    key = "setperm"
    aliases = ["perm"]
    locks = "cmd:perm(Developer)"
    help_category = "System"
