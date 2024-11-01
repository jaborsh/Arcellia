from commands.command import Command


class CmdHome(Command):
    """
    Command to teleport the player to their home location.

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
        """Implement the command"""
        caller = self.caller
        home = caller.home

        if not home:
            self.msg_no_home()
        elif home == caller.location:
            self.msg_already_home()
        else:
            self.msg_teleport_home()
            caller.move_to(home, move_type="teleport")

    def msg_no_home(self):
        """Send message when player has no home"""
        self.caller.msg("You have no home!")

    def msg_already_home(self):
        """Send message when player is already at home"""
        self.caller.msg("You are already home!")

    def msg_teleport_home(self):
        """Send message when player is teleporting home"""
        self.caller.msg("There's no place like home ...")
