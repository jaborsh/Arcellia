from commands.command import Command
from server.conf import logger


class CmdNoShout(Command):
    """
    Toggle the ability of user(s) to use the "shout" command.

    Syntax:
        noshout <player(s)>

    Examples:
        noshout jake
        noshout jake,kiana

    Functionality:
        - Players targeted by this command will receive the message "You suddenly
          get a sore throat!" and lose the ability to use the "shout" command.
        - Further attempts by these players to use the "shout" command will
          result in the message "Your throat is still sore."
        - Reversing the command will restore the ability to shout, sending the
          message "Your sore throat fades away."
    """

    key = "noshout"
    locks = "cmd:perm(Admin)"
    help_category = "Admin"

    def func(self):
        """Execute the noshout command to toggle shout permissions for specified players."""
        args = self.args.strip()
        if not args:
            self.msg("Syntax: noshout <player(s)>")
            return

        player_names = [
            player.strip() for player in args.split(",") if player.strip()
        ]
        if not player_names:
            self.msg("No valid player names provided.")
            return

        for player_name in player_names:
            target = self.caller.search(player_name, global_search=True)
            if not target:
                self.msg(f"Player '{player_name}' not found.")
                continue

            self.toggle_shout_permission(target)

    def toggle_shout_permission(self, target):
        """
        Toggle the 'no_shout' permission for a given target player.

        Args:
            target (Player): The player whose shout permission is to be toggled.
        """
        if target.permissions.check("no_shout"):
            self.restore_shout(target)
        else:
            self.remove_shout(target)

    def remove_shout(self, target):
        """
        Remove the ability to shout from the target player.

        Args:
            target (Player): The player to restrict from shouting.
        """
        target.permissions.add("no_shout")
        target.msg("|rYou suddenly get a sore throat!|n")
        self.msg(f"|r{target} can no longer shout.|n")
        logger.log_info(
            f"{self.caller} removed shout permissions for {target}."
        )

    def restore_shout(self, target):
        """
        Restore the ability to shout for the target player.

        Args:
            target (Player): The player to restore shout permissions.
        """
        target.permissions.remove("no_shout")
        target.msg("|gYour sore throat fades away.|n")
        self.msg(f"|g{target} can now shout.|n")
        logger.log_info(
            f"{self.caller} restored shout permissions for {target}."
        )
