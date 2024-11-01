from commands.command import Command


class CmdWealth(Command):
    """
    Syntax: wealth

    Display how much money you have.
    """

    key = "wealth"

    def func(self):
        caller = self.caller
        caller.msg("Total Wealth: %s" % int(caller.wealth))
