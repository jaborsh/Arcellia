from commands.command import Command
from server.conf import logger


class CmdWizInv(Command):
    """
    Be invisible to all players.

    Syntax: wizinv

    Make yourself invisible to all players.
    """

    key = "wizinv"
    locks = "cmd:perm(Admin)"
    help_category = "Admin"

    def func(self):
        caller = self.caller

        if "pperm(Admin)" in caller.locks.get("view"):
            caller.locks.add("view:all()")
            caller.msg("You are now visible to all players.")
            logger.log_info(f"{caller} toggled wizinv off.")
        else:
            caller.locks.add("view:pperm(Admin)")
            caller.msg("You are now invisible to all players.")
            logger.log_info(f"{caller} toggled wizinv on.")
