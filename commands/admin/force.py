"""
Command module containing CmdForce.
"""

from commands.command import Command
from server.conf import logger


class CmdForce(Command):
    """
    Admin command to force an object to execute a command.

    Usage:
        force <object> <command>

    This command allows administrators to force an object to execute a command.
    The <object> parameter specifies the name of the object to be forced, and
    the <command> parameter specifies the command to be executed by the object.

    Example:
        force jake look

    This will force the object named 'jake' to execute the 'look' command.
    """

    key = "force"
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        if not self.args:
            self.msg("Syntax: force <object> <command>")
            return

        args = self.args.split(None, 1)
        if len(args) < 2:
            self.msg("Syntax: force <object> <command>")
            return

        obj_name, command = args
        obj = self.account.search(
            obj_name, global_search=True, search_object=True
        )
        if not obj:
            self.msg(f"Object '{obj_name}' not found.")
            return

        obj.execute_cmd(command)
        self.msg(f"You force {obj} to {command}")
        logger.log_info(f"{self.caller} forced {obj} to {command}.")
