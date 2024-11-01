from commands.command import Command
from server.conf import logger


class CmdPetrify(Command):
    """
    Toggle the petrification state of a target character.

    Syntax:
        petrify <target>

    Examples:
        petrify john
        petrify jane

    Functionality:
        - Turns the target character to stone, making them unable to take any actions.
        - Players can be returned to their original fleshy state by repeating the command.
    """

    key = "petrify"
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        """Execute the petrify command to toggle petrification on the specified target."""
        target_name = self.args.strip()
        if not target_name:
            self.msg("Syntax: petrify <target>")
            return

        target = self.caller.search(target_name, global_search=True)
        if not target:
            self.msg(f"Player '{target_name}' not found.")
            return

        if target == self.caller:
            self.msg("|#6C6C6CYou probably shouldn't petrify yourself.")
            return

        self.toggle_petrification(target)

    def toggle_petrification(self, target):
        """
        Toggle the 'petrified' permission for the target player.

        Args:
            target (Player): The player to petrify or restore.
        """
        if target.permissions.check("petrified"):
            self.restore_flesh(target)
        else:
            self.petrify_target(target)

    def petrify_target(self, target):
        """
        Petrify the target player, preventing them from taking any actions.

        Args:
            target (Player): The player to petrify.
        """
        target.permissions.add("petrified")
        target.msg(
            "|#6C6C6CYou feel your body stiffen and turn to stone, unable to move.|n"
        )
        self.msg(f"|#6C6C6C{target} is now petrified.|n")
        logger.log_info(f"{self.caller} petrified {target}.")

    def restore_flesh(self, target):
        """
        Restore the target player to their original fleshy state.

        Args:
            target (Player): The player to restore.
        """
        target.permissions.remove("petrified")
        target.msg("|#6C6C6CThe stone encasing you crumbles away.|n")
        self.msg(f"|#6C6C6C{target} is no longer petrified.|n")
        logger.log_info(f"{self.caller} restored {target} to flesh.")
