from evennia.utils import (
    inherits_from,
)

from commands.command import Command
from typeclasses.consumables.consumables import Consumable


class CmdEat(Command):
    """
    Eat something.

    Syntax: eat <food>

    This command lets you consume a food item from your inventory.
    Eating food can restore health or provide other benefits depending
    on the type of food consumed.
    """

    key = "eat"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            return caller.msg("Eat what?")

        food = caller.search(args)
        if not food:
            return

        if not inherits_from(food, Consumable):
            return caller.msg("You can't eat that.")

        if not food.at_pre_eat(caller):
            return

        food.at_eat(caller)
