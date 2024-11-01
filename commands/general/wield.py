from commands.command import Command
from typeclasses.equipment.equipment import EquipmentType


class CmdWield(Command):
    """
    Command to wield a weapon.

    Usage:
        wield <weapon>

    Description:
        This command allows you to wield a weapon from your inventory.
        Ensure you have the weapon in your possession before attempting
        to wield it. Only items classified as weapons can be wielded.

    Examples:
        wield sword
        wield dagger
    """

    key = "wield"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            return caller.msg("Wield what?")

        weapon = caller.search(args, location=caller, quiet=True)
        if not weapon:
            return caller.msg("You don't have anything like that.")

        weapon = weapon[0]

        if not weapon.equipment_type == EquipmentType.WEAPON:
            return caller.msg("You can't wield that.")

        caller.equipment.wear(weapon)
