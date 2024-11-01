from commands.command import Command


class CmdAttackStop(Command):
    """
    Command to stop the combat for the caller.

    Usage:
        attackstop

    This command allows the caller to disengage from combat, effectively stopping any ongoing combat actions.
    """

    key = "attackstop"
    locks = "cmd:all()"

    def func(self):
        self.caller.location.combat.remove_combatant(self.caller)
        self.caller.msg("You stop combat.")
