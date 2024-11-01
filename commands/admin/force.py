"""
Command module containing CmdForce for forcing objects to execute commands.
"""

from commands.command import Command
from server.conf import logger


class CmdForce(Command):
    """
    Admin command to force an object to execute a command.

    Usage:
        force <object> <command>

    This command allows administrators to force an object to execute a specified command.
    The <object> parameter specifies the target object, and the <command> parameter specifies
    the command to be executed by the object.

    Example:
        force jake look

    This will force the object named 'jake' to execute the 'look' command.
    """

    key = "force"
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        """
        Executes the force command by parsing arguments, validating the target object,
        executing the specified command, and logging the action.
        """
        if not self.args:
            self._display_syntax_error()
            return

        target_obj, command = self._parse_arguments(self.args)
        if not command:
            self._display_syntax_error()
            return

        obj = self._find_target_object(target_obj)
        if not obj:
            return  # Error message already handled in _find_target_object

        if self._execute_command_on_object(obj, command):
            self._notify_caller(obj, command)
            self._log_action(obj, command)

    def _display_syntax_error(self):
        """Displays the correct syntax for using the force command."""
        self.caller.msg("Syntax: force <object> <command>")

    def _parse_arguments(self, args):
        """
        Parses the input arguments to extract the target object and command.

        Args:
            args (str): The raw argument string.

        Returns:
            tuple: A tuple containing the target object name and the command string.
        """
        parsed_args = args.split(None, 1)
        if len(parsed_args) == 2:
            return parsed_args[0], parsed_args[1].strip()
        return parsed_args[0], None

    def _find_target_object(self, obj_name):
        """
        Searches for the target object based on the provided name.

        Args:
            obj_name (str): The name of the object to search for.

        Returns:
            Object or None: The found object or None if not found.
        """
        obj = self.caller.search(obj_name, global_search=True)
        if not obj:
            self.caller.msg(f"Object '{obj_name}' not found.")
        return obj

    def _execute_command_on_object(self, obj, command):
        """
        Attempts to execute the specified command on the target object.

        Args:
            obj (Object): The target object.
            command (str): The command to execute.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        try:
            obj.execute_cmd(command)
            return True
        except Exception as e:
            self.caller.msg(f"Failed to execute command on '{obj}': {e}")
            logger.log_error(
                f"Error executing command '{command}' on '{obj}': {e}"
            )
            return False

    def _notify_caller(self, obj, command):
        """
        Notifies the caller that the command was successfully forced.

        Args:
            obj (Object): The target object.
            command (str): The command that was executed.
        """
        self.caller.msg(f"You force {obj} to '{command}'.")

    def _log_action(self, obj, command):
        """
        Logs the action of forcing a command on an object.

        Args:
            obj (Object): The target object.
            command (str): The command that was executed.
        """
        logger.log_info(f"{self.caller} forced {obj} to execute '{command}'.")
