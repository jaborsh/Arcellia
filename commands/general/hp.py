from commands.command import Command


class CmdHP(Command):
    """
    Syntax: hp

    Command to display your health, mana, and stamina.
    """

    key = "hp"
    aliases = ["h", "health"]
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        caller.msg(
            "|rHealth|n: |r%s|n/|r%s|n  |cMana|n: |c%s|n/|c%s|n  |gStamina|n: |g%s|n/|g%s|n"
            % (
                int(caller.health.value),
                int(caller.health.max),
                int(caller.mana.value),
                int(caller.mana.max),
                int(caller.stamina.value),
                int(caller.stamina.max),
            )
        )
