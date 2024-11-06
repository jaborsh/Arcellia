from commands.command import Command


class CmdXp(Command):
    """
    Syntax: xp

    Display how much experience you have.
    """

    key = "xp"

    def func(self):
        caller = self.caller
        caller.msg(f"|CExperience: {int(caller.experience.value)}|n.")
