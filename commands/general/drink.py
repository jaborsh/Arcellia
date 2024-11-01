from evennia.utils import inherits_from

from commands.command import Command
from typeclasses.consumables.consumables import Consumable


class CmdDrink(Command):
    """
    Allows the player to drink a consumable item.

    Usage:
        drink <item>

    This command lets the player drink a specified consumable item. The player
    must provide the name of the item they wish to drink. If the item is not
    found or is not a consumable, an appropriate message will be displayed.

    Example:
        > drink water
        You drink the water and feel refreshed.
    """

    key = "drink"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            return caller.msg("Drink what?")

        drink = caller.search(args)
        if not drink:
            return

        if not inherits_from(drink, Consumable):
            return caller.msg("You can't drink that.")

        if not drink.at_pre_drink(caller):
            return

        drink.at_drink(caller)
