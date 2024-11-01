import re
import time

from evennia.server.models import ServerConfig

from commands.command import Command
from server.conf import logger

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
        table.add_row(
            str(inum + 1), ban[0] and ban[0] or ban[1], ban[3], ban[4]
        )
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
            ipregex = re.compile(
                ban.replace(".", "\.").replace("*", "[0-9]{1,3}")
            )
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
        self.msg(
            f"{typ}-ban '|w{ban}|n' was added. Use |wunban|n to reinstate."
        )
        logger.log_sec(
            f"Banned {typ}: {ban.strip()} (Caller: {self.caller}, IP: {self.session.address})."
        )
