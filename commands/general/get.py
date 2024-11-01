import re

from commands.command import Command
from server.conf.at_search import SearchReturnType
from utils.colors import strip_ansi
from utils.text import pluralize, singularize


class CmdGet(Command):
    """
    Command to get/take items from the game world.

    Usage:
        get all [items] [from <container>] [container_number]
        get <item> [item_number] [from <container>] [container_number]

    Examples:
        get all
        get sword
        get sword 2
        get 2 swords
        get all from bag
        get apple from bag
        get 2 apples from bag
        get 2 apples from bag 2

    This command allows the player to get/take items from the game world. The
    player can specify the name of the item to get, an optional container from
    which to get the item, and an optional quantity of items to get. If no
    quantity is specified, the default is 1.

    If the player specifies a container, the command will attempt to find the
    item within the container. If no container is specified, the command will
    search for the item in the player's current location.

    If the item is found and the player has the necessary permissions to get
    the item, it will be moved to the player's inventory. The appropriate
    messages will be displayed to the player and other characters in the
    location.
    """

    key = "get"
    aliases = ["take"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def parse(self):
        if "all" in self.args:
            regex_pattern = r"(?P<quantity>)(?P<item>all\s*\w*)(?P<item_number>)(?:\s+from\s+(?P<container>[\w\s]+?)(?:\s+(?P<container_number>\d+))?)?$"
        else:
            regex_pattern = r"(?:(?P<quantity>\d+)\s+)?(?P<item>[\w\s]+?)(?:\s+(?P<item_number>\d+))?(?:\s+from\s+(?P<container>[\w\s]+?)(?:\s+(?P<container_number>\d+))?)?$"

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
            self.container = (
                match.group("container") if match.group("container") else None
            )
            self.container_number = (
                int(match.group("container_number"))
                if match.group("container_number")
                else 1
            )

    def _get_single(self, caller, item, quantity, item_number, container=None):
        # return_quantity doubles as the specific item in singular form.
        location = container or caller.location

        obj = caller.search(
            item,
            location=location,
            return_quantity=item_number,
            return_type=SearchReturnType.ONE,
        )
        if not obj:
            return

        if not obj.access(caller, "get"):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("You can't get that.")
            return

        if not obj.at_pre_get(caller, quantity=quantity):
            return

        obj.move_to(caller, quiet=True, move_type="get")
        obj.at_get(caller)
        single, plural = obj.get_numbered_name(quantity, caller)
        if container:
            single, plural = obj.get_numbered_name(quantity, caller)
            article = (
                "an"
                if strip_ansi(obj.display_name)[0].lower() in "aeiou"
                else "a"
            )
            article = "some" if strip_ansi(single).endswith("s") else article
            return caller.location.msg_contents(
                f"$You() $conj(get) {article} $you(item) from $you(container).",
                from_obj=caller,
                mapping={"item": obj, "container": container},
            )

        single, plural = obj.get_numbered_name(quantity, caller)
        article = (
            "an" if strip_ansi(obj.display_name)[0].lower() in "aeiou" else "a"
        )
        article = "some" if strip_ansi(single).endswith("s") else article
        caller.location.msg_contents(
            f"$You() $conj(get) {article} $you(item).",
            from_obj=caller,
            mapping={"item": obj},
        )

    def _get_multiple(
        self, caller, item, quantity, item_number, container=None
    ):
        location = container or caller.location
        objs = caller.search(
            item,
            location=location,
            return_quantity=quantity,
            return_type=SearchReturnType.MULTIPLE,
        )

        if not objs:
            return

        if not isinstance(objs, list):
            objs = [objs]

        for obj in objs:
            if not obj.access(caller, "get"):
                if obj.db.get_err_msg:
                    caller.msg(obj.db.get_err_msg)
                else:
                    caller.msg("You can't get that.")
                continue

            if not obj.at_pre_get(caller, quantity=quantity):
                return  # This should only proc with currency.
                # continue

            obj.move_to(caller, quiet=True, move_type="get")
            obj.at_get(caller)

        obj = objs[0]
        quantity = len(objs)
        single, plural = obj.get_numbered_name(quantity, caller)
        if container:
            return caller.location.msg_contents(
                f"$You() $conj(get) {plural} from {container.get_display_name(caller)}.",
                from_obj=caller,
            )

        caller.location.msg_contents(
            f"$You() $conj(get) {plural}.", from_obj=caller
        )

    def _get_all(self, caller, item, container=None):
        location = container or caller.location

        if item:
            objs = caller.search(
                item,
                location=location,
                return_type=SearchReturnType.ALL,
            )
        else:
            objs = location.contents

        if not objs:
            return

        if not isinstance(objs, list):
            objs = [objs]

        for obj in objs:
            if obj == caller:
                continue

            if not obj.access(caller, "get"):
                if obj.db.get_err_msg:
                    caller.msg(obj.db.get_err_msg)
                else:
                    caller.msg("You can't get that.")
                continue

            if not obj.at_pre_get(caller):
                return

            obj.move_to(caller, quiet=True, move_type="get")
            obj.at_get(caller)

        items = str(len(objs)) + " " + pluralize(item) if item else "everything"
        if "gold" in items:
            return

        if container:
            return caller.location.msg_contents(
                f"$You() $conj(get) {items} from {container.get_display_name(caller)}.",
                from_obj=caller,
            )

        caller.location.msg_contents(
            f"$You() $conj(get) {items}.", from_obj=caller
        )

    def func(self):
        caller = self.caller

        if not self.args:
            return caller.msg("Get what?")

        all = "all" in self.item
        quantity = self.quantity
        item = self.item.replace("all", "").strip()
        item_number = self.item_number
        container = self.container
        container_number = self.container_number

        if container:
            container = caller.search(
                container,
                return_quantity=container_number,
                return_type=SearchReturnType.ONE,
            )
            if not container:
                return

        if item:
            item = singularize(item) if singularize(item) else item

        if all:
            self._get_all(caller, item, container)
        elif quantity == 1:
            self._get_single(caller, item, quantity, item_number, container)
        else:
            self._get_multiple(caller, item, quantity, item_number, container)
