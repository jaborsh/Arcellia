import re

from commands.command import Command


class CmdPut(Command):
    """
    Syntax: put [quantity] <obj> [number] in <container] [number]

    Examples: put wand in backpack
              put 2 wands in backpack
              put wand 2 in backpack

    Put an object into a container.
    """

    key = "put"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def parse(self):
        """
        Parses the input to extract the quantity, object name, object number, and container details.
        """
        # Regular expression to match various command formats
        regex_pattern = (
            r"(?:(\d+)\s+)?(\w+)(?:\s+(\d+))?\s+in\s+(\w+)(?:\s+(\d+))?"
        )
        match = re.match(regex_pattern, self.args.strip())

        if match:
            # Extracting quantity, object name, object number, container, and container number
            self.quantity = int(match.group(1)) if match.group(1) else 1
            self.obj_name = match.group(2)
            self.obj_number = int(match.group(3)) if match.group(3) else 1
            self.container = match.group(4)
            self.container_number = int(match.group(5)) if match.group(5) else 1
        else:
            # Default values if no match is found
            (
                self.quantity,
                self.obj_name,
                self.obj_number,
                self.container,
                self.container_number,
            ) = (1, None, 1, None, 1)

    def func(self):
        caller = self.caller
        quantity = self.quantity
        obj_name = self.obj_name
        obj_number = self.obj_number
        container_name = self.container
        container_number = self.container_number

        if not self.args:
            caller.msg("Put what in what?")
            return

        container = caller.search(
            container_name,
            number=container_number,
        )

        if not container:
            return

        if not container.access(caller, "get_from"):
            if container.db.get_from_err_msg:
                return self.msg(container.db.get_from_err_msg)
            return self.msg("You can't put things in that.")

        deposited_items = []
        for _ in range(quantity):
            obj = caller.search(
                obj_name,
                location=caller,
                nofound_string=f"You aren't carrying {obj_name}.",
                number=obj_number,
            )

            if not obj:
                break

            if not obj.at_pre_drop(caller):
                continue

            obj.move_to(container, quiet=True, move_type="drop")
            obj.at_drop(caller)
            deposited_items.append(obj)

        if deposited_items:
            obj = deposited_items[0]
            quantity = len(deposited_items)
            single, plural = obj.get_numbered_name(quantity, caller)
            item = single if quantity == 1 else f"{quantity} {plural}"
            caller.location.msg_contents(
                f"$You() $conj(put) {item} in {container.display_name}.",
                from_obj=caller,
            )
