from commands.command import Command
from server.conf import logger


class CmdRestore(Command):
    """
    Command to restore a target character.

    Usage:
        restore <target>

    This command allows an admin to restore a target character. The target is searched globally, and if found, the target is restored. Both the caller and the target receive messages indicating the restoration.
    """

    key = "restore"
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        caller = self.caller
        args = self.args

        if not args:
            return caller.msg("Usage: restore <target>")

        target = caller.search(args, global_search=True)
        if not target:
            return

        target.at_restore()
        caller.msg(f"You restore {target.get_display_name(caller)}.")
        target.msg(f"{caller.get_display_name(target)} restores you.")
        logger.log_info(f"{caller} restored {target}.")
