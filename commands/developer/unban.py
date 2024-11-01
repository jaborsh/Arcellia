from evennia.server.models import ServerConfig

from commands.command import Command
from server.conf import logger

from .ban import list_bans


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
            ret = yield (
                f"Are you sure you want to unban {num}: '|w{value}|n' [Y]/N?"
            )
            if str(ret).lower() in ("n", "no"):
                self.msg("Aborted.")
                return

            del banlist[num - 1]
            ServerConfig.objects.conf("server_bans", banlist)
            self.msg(f"Cleared ban {num}: '{value}'")
            logger.log_sec(
                f"Unbanned: {value.strip()} (Caller: {self.caller}, IP: {self.session.address})."
            )
