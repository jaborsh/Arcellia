"""
Command module containing CmdAt.
"""

from evennia.utils.utils import inherits_from

from commands.command import Command
from server.conf import logger


class CmdAt(Command):
    """
    Execute a command as if you were in another location.

    Syntax: at <object/location> <command>

    Provide the path to where the command should be executed, and the command
    itself, and it will be so.
    """

    key = "at"
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        if not self.args:
            self.caller.msg("Syntax: at <object/location> <command>")
            return

        args = self.args.split(None, 1)
        if len(args) < 2:
            self.caller.msg("Syntax: at <object/location> <command>")
            return

        obj = self.caller.search(args[0], global_search=True)
        if not obj:
            return

        og_loc = self.caller.location
        if inherits_from(obj, "typeclasses.rooms.Room"):
            at_loc = obj
        else:
            if not obj.location:
                return self.caller.msg(f"{obj} has no location.")
            at_loc = obj.location

        self.caller.move_to(at_loc, quiet=True, move_hooks=False)
        self.caller.execute_cmd(args[1])
        self.caller.move_to(og_loc, quiet=True, move_hooks=False)
        logger.log_info(f"{self.caller} executed '{args[1]}' at {obj}.")
