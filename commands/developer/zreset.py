from commands.command import Command
from server.conf import logger
from world.xyzgrid.xyzgrid import get_xyzgrid


class CmdZReset(Command):
    """
    Reset a zone.

    Syntax: reset <zone>

    Resets a zone, loading/resetting/updating all objects in the zone.
    """

    key = "zreset"
    locks = "cmd:pperm(Developer)"
    help_category = "Developer"

    def func(self):
        caller = self.caller
        if not self.args:
            return self.msg("You must specify a zone to reset.")

        grid = get_xyzgrid()
        grid.spawn(xyz=("*", "*", self.args.strip()))
        caller.msg(f"Zone {self.args.strip()} reset.")
        logger.log_info(f"Zone '{self.args.strip()}' reset by {caller}.")
