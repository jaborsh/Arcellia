from evennia.utils import (
    inherits_from,
)

from commands.command import Command
from handlers.config.clothing_config import ClothingConfig
from typeclasses.clothing import Clothing
from typeclasses.equipment.equipment import Equipment

_CLOTHING_OVERALL_LIMIT = ClothingConfig.OVERALL_LIMIT


class CmdWear(Command):
    """
    Syntax: wear <obj>

    Examples:
        wear red shirt

    All the clothes and equipment you are wearing appear in your description.
    """

    key = "wear"
    locks = "cmd:all()"

    def wear_clothing(self, clothing):
        caller = self.caller
        clothes = caller.clothing.all()

        if clothing in clothes:
            caller.msg("You are already wearing that.")
            return

        if _CLOTHING_OVERALL_LIMIT and len(clothes) >= _CLOTHING_OVERALL_LIMIT:
            caller.msg("You can't wear any more clothes.")
            return

        caller.clothing.wear(clothing)

    def wear_equipment(self, gear):
        caller = self.caller
        equipment = caller.equipment.all()

        if gear in equipment:
            caller.msg("You are already wearing that.")
            return

        caller.equipment.wear(gear)

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            caller.msg("Usage: wear <obj>")
            return

        item = caller.search(args, location=caller, quiet=True)
        if not item:
            caller.msg("You don't have anything like that.")
            return

        item = item[0]
        if inherits_from(item, Clothing):
            self.wear_clothing(item)
        elif inherits_from(item, Equipment):
            self.wear_equipment(item)
        else:
            caller.msg(
                f"{item.get_display_name(caller)} isn't something you can wear."
            )
            return
