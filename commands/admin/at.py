"""
Command module containing the CmdAt class for executing commands at a specified location.
"""

from evennia.utils.utils import inherits_from

from commands.command import Command
from server.conf import logger


class CmdAt(Command):
    """
    Execute a command as if you were in another location.

    Usage:
        at <object/location> <command>

    This command allows an admin to execute commands as though they are in a specified location.
    The target location can be an object or a location path.
    """

    key = "at"
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        """
        Core command function to parse arguments, validate locations, and
        execute the command in the specified location.
        """
        if not self.args:
            return self._syntax_error()

        target, command = self._parse_args(self.args)
        if not command:
            return self._syntax_error()

        target_location = self._get_target_location(target)
        if not target_location:
            return  # Error message already handled in _get_target_location

        self._execute_at_location(target_location, command)

    def _syntax_error(self):
        """Display the correct syntax for using this command."""
        self.caller.msg("Syntax: at <object/location> <command>")

    def _parse_args(self, args):
        """
        Parse the input arguments.

        Args:
            args (str): Command arguments as a single string.

        Returns:
            tuple: (target, command) where target is the location string and
                   command is the command to execute.
        """
        parsed_args = args.split(None, 1)
        return parsed_args if len(parsed_args) == 2 else (parsed_args[0], None)

    def _get_target_location(self, target):
        """
        Search and validate the target location.

        Args:
            target (str): The location or object path.

        Returns:
            Object: The validated target location, or None if invalid.
        """
        obj = self.caller.search(target, global_search=True)
        if not obj:
            return None

        if inherits_from(obj, "typeclasses.rooms.Room"):
            return obj
        elif obj.location:
            return obj.location
        else:
            self.caller.msg(f"{obj} has no valid location.")
            return None

    def _execute_at_location(self, location, command):
        """
        Temporarily move the caller to a new location to execute a command,
        then move back to the original location.

        Args:
            location (Object): The target location to move to.
            command (str): The command to execute at the target location.
        """
        original_location = self.caller.location
        self.caller.move_to(location, quiet=True, move_hooks=False)
        self.caller.execute_cmd(command)
        logger.log_info(f"{self.caller} executed '{command}' at {location}.")
        self.caller.move_to(original_location, quiet=True, move_hooks=False)
