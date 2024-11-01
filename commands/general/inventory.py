from commands.command import Command
from utils.colors import strip_ansi


class CmdInventory(Command):
    """
    Syntax: inventory

    Shows your inventory.
    """

    # Alternate version of the inventory command which separates
    # worn and carried items.

    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"
    arg_regex = r"$"
    max_length = 0

    def func(self):
        """check inventory"""
        caller = self.caller
        if not caller.contents:
            caller.msg("You are not carrying or wearing anything.")
            return

        equipment_table = self.create_table(caller.equipment.all(), "Equipment")
        worn_table = self.create_table(caller.clothing.all(), "Clothing")
        carried_items = [
            obj
            for obj in caller.contents
            if obj not in caller.clothing.all()
            and obj not in caller.equipment.all()
        ]
        carried_table = self.create_table(carried_items, "Carrying")
        header = self.create_header(caller)
        footer = self.create_footer()

        caller.msg(
            f"{header}{equipment_table}{worn_table}{carried_table}{footer}"
        )

    def create_header(self, caller):
        item_count_line = "|C" + f"Number of Items: {len(caller.contents)}"
        self.max_length = (
            max(self.max_length, len(strip_ansi(item_count_line))) + 2
        )
        header = "|x" + "-" * self.max_length + "|n"
        title = "|C" + "Inventory".center(self.max_length) + "|n"
        curr_weight = caller.weight.value
        max_weight = caller.weight.max
        weight_line = (
            "|C"
            + f"Weight: {int(curr_weight)} / {int(max_weight)}".center(
                self.max_length
            )
            + "|n"
        )
        item_count_line = item_count_line.center(self.max_length + 2) + "|n"

        return f"{header}\n{title}\n{weight_line}\n{item_count_line}\n{header}"

    def create_table(self, items, item_type):
        if not items:
            return ""

        output = [f"|w{item_type}:|n"]

        if item_type == "Clothing":
            max_position = max([len(item.position) for item in items]) + 8
            for item in items:
                spaces = " " * (max_position - len(f"<worn {item.position}>"))
                line = f"|x<worn {item.position}>|n{spaces}{item.get_display_name(self.caller)}"
                if item.covered_by:
                    line += " |x(hidden)|n"
                output.append(line)
        elif item_type == "Equipment":
            max_position = max([len(item.position) for item in items]) + 8
            for item in items:
                spaces = " " * (max_position - len(f"<worn {item.position}>"))
                line = f"|x<worn {item.position}>|n{spaces}{item.get_display_name(self.caller)}"
                output.append(line)
        else:
            output.extend(
                [item.get_display_name(self.caller) for item in items]
            )

        max_line_length = max([len(strip_ansi(line)) for line in output])
        self.max_length = max(max_line_length, self.max_length) + 1

        return "\n" + "\n ".join(output) + "\n"

    def create_footer(self):
        return "|x" + "-" * self.max_length + "|n"
