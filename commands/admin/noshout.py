from commands.command import Command
from server.conf import logger


class CmdNoShout(Command):
    """
    Prevent user(s) from being able to use the "shout" command.

    Syntax: noshout <player(s)>

    Example: noshout jake
             noshout jake,kiana

    Players targeted by this command will receive the message "You suddenly
    get a sore throat!" Further attempts by the player(s) to use the "shout"
    command will result in the message "Your throat is still sore."

    Upon reversal, the player(s) will receive the message "Your sore throat
    fades away."
    """

    key = "noshout"
    locks = "cmd:perm(Admin)"
    help_category = "Admin"

    def func(self):
        if not self.args:
            self.msg("Syntax: noshout <player(s)>")
            return

        players = self.args.split(",")
        for player in players:
            target = self.caller.search(player, global_search=True)
            if not target:
                self.msg(f"Player '{player}' not found.")
                continue

            if target.permissions.check("no_shout"):
                target.permissions.remove("no_shout")
                target.msg("|gYour sore throat fades away.|n")
                self.msg(f"{target} can now shout.")
                logger.log_info(
                    f"{self.caller} restored shout permissions for {target}."
                )
            else:
                target.permissions.add("no_shout")
                target.msg("|rYou suddenly get a sore throat!|n")
                self.msg(f"{target} can no longer shout.")
                logger.log_info(
                    f"{self.caller} removed shout permissions for {target}."
                )
