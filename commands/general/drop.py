import re

from evennia.prototypes import spawner

from commands.command import Command
from prototypes import currencies
from server.conf.at_search import SearchReturnType
from utils.colors import strip_ansi
from utils.text import singularize


class CmdDrop(Command):
    """
    Command: drop

    Usage:
        drop <item>
        drop <quantity> <item>
        drop <item> <number>
        drop all <item>

    The 'drop' command allows you to remove items from your inventory and place them
    onto the ground in your current location. You can drop a specific item, a certain
    quantity of an item, or even all items of a particular type. If you possess multiple
    instances of an item, you can specify which one to drop by its number.

    Examples:
        drop sword
        drop 3 apples
        drop apple 2
        drop all coins

    Notes:
        - Dropping 'all' will place every item in your inventory onto the ground.
        - You can drop coins or gold by specifying the amount.
    """

    key = "drop"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def parse(self):
        self.args = self.args.strip()
        if "all" in self.args:
            regex_pattern = (
                r"(?P<quantity>)(?P<item>all\s*\w*)(?P<item_number>)?$"
            )
        else:
            regex_pattern = r"(?:(?P<quantity>\d+)\s+)?(?P<item>[\w\s]+?)(?:\s+(?P<item_number>\d+))?$"

        match = re.match(regex_pattern, self.args.strip())
        if match:
            self.quantity = (
                int(match.group("quantity")) if match.group("quantity") else 1
            )
            self.item = match.group("item")
            self.item_number = (
                int(match.group("item_number"))
                if match.group("item_number")
                else 1
            )

    def _drop_all(self, caller, item):
        inventory = caller.contents
        location = caller.location

        if item in ("coins", "gold"):
            return self._drop_coins(caller, caller.db.wealth)

        for obj in inventory:
            if not obj.at_pre_drop(caller):
                continue

            obj.move_to(location, quiet=True, move_type="drop")
            obj.at_drop(caller)

        caller.location.msg_contents(
            "$You() $conj(drop) everything.", from_obj=caller
        )

    def _drop_single(self, caller, item, quantity, item_number):
        if item in ("coin", "coins", "gold"):
            return self._drop_coins(caller, quantity)

        obj = caller.search(
            item,
            location=caller,
            return_quantity=item_number,
            return_type=SearchReturnType.ONE,
        )
        if not obj:
            return

        if not obj.at_pre_drop(caller):
            return

        obj.move_to(caller.location, quiet=True, move_type="drop")
        obj.at_drop(caller)
        article = (
            "an" if strip_ansi(obj.display_name)[0].lower() in "aeiou" else "a"
        )
        article = (
            "some" if strip_ansi(obj.display_name).endswith("s") else article
        )
        caller.location.msg_contents(
            f"$You() $conj(drop) {article} $you(item).",
            from_obj=caller,
            mapping={"item": obj},
        )

    def _drop_multiple(self, caller, item, quantity, item_number):
        if item in ("coin", "coins", "gold"):
            return self._drop_coins(caller, quantity)

        objs = caller.search(
            item,
            location=caller,
            return_quantity=quantity,
            return_type=SearchReturnType.MULTIPLE,
        )
        if not objs:
            return

        for obj in objs:
            if not obj.at_pre_drop(caller):
                continue

            obj.move_to(caller.location, quiet=True, move_type="drop")
            obj.at_drop(caller)

        obj = objs[0]
        quantity = len(objs)
        single, plural = obj.get_numbered_name(quantity, caller)
        caller.location.msg_contents(
            f"$You() $conj(drop) {plural}.", from_obj=caller
        )

    def _drop_coins(self, caller, quantity):
        gold = spawner.spawn(currencies.GOLD)[0]
        gold.db.price = quantity
        caller.db.wealth -= quantity
        gold.move_to(caller.location, quiet=True, move_type="drop")
        return caller.location.msg_contents(
            f"$You() $conj(drop) {gold.price} {gold.get_display_name(caller)}.",
            from_obj=caller,
        )

    def func(self):
        caller = self.caller
        args = self.args

        if not args:
            return caller.msg("Drop what?")

        all = "all" in self.item
        quantity = self.quantity
        item = self.item.replace("all", "").strip()
        item_number = self.item_number

        if item:
            item = singularize(item) if singularize(item) else item

        if all:
            self._drop_all(caller, item)
        elif quantity == 1:
            self._drop_single(caller, item, quantity, item_number)
        else:
            self._drop_multiple(caller, item, quantity, item_number)
