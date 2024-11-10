from commands.command import Command
from server.conf.at_search import SearchReturnType


class CmdAttack(Command):
    """
    Command to initiate an attack on a target.

    Usage:
      attack <target>

    This command allows you to attack a specified target. The target must be a valid living entity.
    """

    key = "attack"
    aliases = ["kill"]
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            return caller.msg("Attack who?")

        target = caller.search(args, return_type=SearchReturnType.ONE)
        if not target:
            return

        if target == caller:
            return caller.msg("You cannot attack yourself.")

        if not target.access(caller, "attack"):
            return caller.msg("You cannot attack that target.")

        caller.location.combat.add_combatant(caller, target)
