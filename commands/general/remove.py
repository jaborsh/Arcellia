from evennia.utils import (
    inherits_from,
)

from commands.command import Command
from typeclasses.clothing import Clothing
from typeclasses.equipment.equipment import Equipment


class CmdRemove(Command):
    """
    Syntax: remove <obj>

    Removes an item of clothing you are wearing. You can't remove
    clothes that are covered up by something else - you must take
    off the covering item first.
    """

    key = "remove"
    aliases = ["rem", "unwear", "unwield"]

    def remove_clothing(self, item):
        caller = self.caller
        if item not in caller.clothing.all():
            caller.msg("You are not wearing that.")
            return

        caller.clothing.remove(item)

    def remove_equipment(self, item):
        caller = self.caller
        if item not in caller.equipment.all():
            caller.msg("You are not wearing that.")
            return

        caller.equipment.remove(item)

    def func(self):
        caller = self.caller
        item = caller.search(self.args, candidates=self.caller.contents)
        if not item:
            caller.msg("You don't have anything like that.")
            return

        if inherits_from(item, Clothing):
            self.remove_clothing(item)
        elif inherits_from(item, Equipment):
            self.remove_equipment(item)
        else:
            caller.msg("You can't remove that.")
            return
