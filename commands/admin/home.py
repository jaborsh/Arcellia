from commands.command import Command


class CmdHome(Command):
    """
    Teleport the player to their home location.

    Usage:
        home

    This command allows the player to teleport to their home location.
    If the player has no home, they will receive a message indicating so.
    If the player is already at their home location, they will receive a
    message indicating so. Otherwise, the player will be teleported to
    their home location.
    """

    key = "home"
    locks = "cmd:perm(home) or perm(Admin)"
    help_category = "Admin"
    arg_regex = r"$"

    def func(self):
        """Execute the home command to teleport the player."""
        caller = self.caller
        home = caller.home

        if not home:
            caller.msg("You have no home!")
            return

        if home == caller.location:
            caller.msg("You are already home!")
            return

        caller.msg("There's no place like home ...")
        caller.move_to(home, move_type="teleport")
