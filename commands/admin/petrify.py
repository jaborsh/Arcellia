from commands.command import Command
from server.conf import logger


class CmdPetrify(Command):
    """
    Petrify a target character.

    Syntax: petrify <target>

    Turns the target character to stone. They will be unable to take any
    actions at all while petrified. Players may be returned to their original
    fleshy state by repeating the command.
    """

    key = "petrify"
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        if not self.args:
            self.msg("Syntax: petrify <target>")
            return

        target = self.caller.search(self.args, global_search=True)
        if not target:
            return

        if target == self.caller:
            self.msg("|#6C6C6CYou probably shouldn't petrify yourself.")
            return

        if target.permissions.check("petrified"):
            target.permissions.remove("petrified")
            target.msg("|#6C6C6CThe stone encasing you crumbles away.")
            self.msg(f"{target} is no longer petrified.")
            logger.log_info(f"{self.caller} restored {target} to flesh.")
        else:
            target.permissions.add("petrified")
            target.msg(
                "|#6C6C6CYou feel your body stiffen and turn to stone, unable to move."
            )
            self.msg(f"{target} is now petrified.")
            logger.log_info(f"{self.caller} petrified {target}.")
