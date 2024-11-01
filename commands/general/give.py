import re

from commands.command import Command
from server.conf.at_search import SearchReturnType


class CmdGive(Command):
    """
    Syntax: give [quantity] <obj> [number] to <target>

    Examples: give wand to jake
              give 2 wands to jake
              give wand 2 to jake

    Gives an item from your inventory to another person, placing it in their
    inventory.
    """

    key = "give"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def parse(self):
        """
        Parses the input to extract the quantity, object name, object number, and target.
        """
        # Regular expression to match various command formats
        regex_pattern = r"(?:(\d+)\s+)?(\w+)(?:\s+(\d+))?\s+to\s+(\w+)"
        match = re.match(regex_pattern, self.args.strip())

        if match:
            # Extracting quantity, object name, object number, and target
            self.quantity = int(match.group(1)) if match.group(1) else 1
            self.obj_name = match.group(2)
            self.obj_number = int(match.group(3)) if match.group(3) else 1
            self.target = match.group(4)
        else:
            # Default values if no match is found
            self.quantity, self.obj_name, self.obj_number, self.target = (
                1,
                None,
                1,
                None,
            )

    def func(self):
        """Implement give"""
        caller = self.caller
        quantity = self.quantity
        obj_name = self.obj_name
        obj_number = self.obj_number
        target = self.target

        if not self.args:
            caller.msg("Give what to whom?")
            return

        target = caller.search(target)

        if not target:
            return

        given_items = []
        for _ in range(quantity):
            obj = caller.search(
                obj_name,
                location=caller,
                return_quantity=obj_number,
                return_type=SearchReturnType.ONE,
                nofound_string=f"You aren't carrying {obj_name}.",
            )

            if not obj:
                break

            if not obj.at_pre_give(caller, target):
                continue

            obj.move_to(target, quiet=True, move_type="give")
            obj.at_give(caller, target)
            given_items.append(obj)

        if given_items:
            obj = given_items[0]
            quantity = len(given_items)
            single, plural = obj.get_numbered_name(quantity, caller)
            item = single if quantity == 1 else f"{quantity} {plural}"
            caller.location.msg_contents(
                f"$You() $conj(give) {item} to $you(target).",
                from_obj=caller,
                mapping={"target": target},
            )
