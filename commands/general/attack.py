from commands.command import Command


class CmdAttack(Command):
    """
    Command to initiate an attack on a target.

    Usage:
      attack <target>

    This command allows you to attack a specified target. The target must be a valid living entity.
    """

    key = "attack"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            return caller.msg("Attack who?")

        target = caller.search(args)
        if not target:
            return

        if target == caller:
            return caller.msg("You cannot attack yourself.")

        caller.location.combat.add_combatant(caller, target)
