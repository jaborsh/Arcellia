import re

from django.conf import settings
from handlers.clothing import CLOTHING_OVERALL_LIMIT, CLOTHING_TYPE_COVER
from parsing.colors import strip_ansi
from prototypes import spawner
from prototypes.miscellaneous import currency
from server.conf import logger
from typeclasses.clothing import Clothing
from typeclasses.currency import Currency
from typeclasses.menus import InteractionMenu

from commands.command import Command
from evennia import InterruptCommand
from evennia.commands.default import general, system
from evennia.typeclasses.attributes import NickTemplateInvalid
from evennia.utils import (
    class_from_module,
    create,
    inherits_from,
    utils,
)

_AT_SEARCH_RESULT = utils.variable_from_module(
    *settings.SEARCH_AT_RESULT.rsplit(".", 1)
)

COMMAND_DEFAULT_CLASS = class_from_module(settings.COMMAND_DEFAULT_CLASS)
__all__ = [
    "CmdAlias",
    "CmdBlock",
    "CmdCover",
    "CmdDrop",
    "CmdEmote",
    "CmdFeel",
    "CmdGet",
    "CmdGive",
    "CmdInteract",
    "CmdInteractions",
    "CmdInventory",
    "CmdListen",
    "CmdLook",
    "CmdPut",
    "CmdRemove",
    "CmdSay",
    "CmdSmell",
    "CmdTaste",
    "CmdTell",
    "CmdTime",
    "CmdUncover",
    "CmdWealth",
    "CmdWear",
    "CmdWhisper",
]


class CmdAlias(general.CmdNick):
    """
    Syntax: alias[/switches] <string> [= [replacement_string]]
            alias[/switches] <template> = <replacement_template>
            alias/delete <string> or number
            aliases

    Switches:
      inputline - replace on the inputline (default)
      object    - replace on object-lookup
      account   - replace on account-lookup
      list      - show all defined aliases (also "nicks" works)
      delete    - remove nick by index in /list
      clearall  - clear all nicks

    Examples:
      alias hi = say Hello, I'm Sarah!
      alias/object tom = the tall man
      alias build $1 $2 = create/drop $1;$2
      alias tm?$1=tell tallman=$1
      alias tm\=$1=tell tallman=$1

    An 'alias' is a personal string replacement. Use $1, $2, ... to catch arguments.
    Put the last $-marker without an ending space to catch all remaining text. You
    can also use unix-glob matching for the left-hand side <string>:

        * - matches everything
        ? - matches 0 or 1 single characters
        [abcd] - matches these chars in any order
        [!abcd] - matches everything not among these chars
        \= - escape literal '=' you want in your <string>

    Note that no objects are actually renamed or changed by this command - your nicks
    are only available to you. If you want to permanently add keywords to an object
    for everyone to use, you need build privileges and the alias command.
    """

    key = "alias"
    aliases = ["aliases", "nick", "nicks"]

    def func(self):
        """Create the nickname"""

        def _cy(string):
            "add color to the special markers"
            return re.sub(r"(\$[0-9]+|\*|\?|\[.+?\])", r"|Y\1|n", string)

        caller = self.caller
        switches = self.switches
        nicktypes = [
            switch
            for switch in switches
            if switch in ("object", "account", "inputline")
        ]
        specified_nicktype = bool(nicktypes)
        nicktypes = nicktypes if specified_nicktype else ["inputline"]

        nicklist = (
            utils.make_iter(
                caller.nicks.get(category="inputline", return_obj=True) or []
            )
            + utils.make_iter(
                caller.nicks.get(category="object", return_obj=True) or []
            )
            + utils.make_iter(
                caller.nicks.get(category="account", return_obj=True) or []
            )
        )

        if "list" in switches or self.cmdstring in ("aliases",):
            if not nicklist:
                string = "|wNo aliases defined.|n"
            else:
                table = self.styled_table("#", "Type", "Alias match", "Replacement")
                for inum, nickobj in enumerate(nicklist):
                    _, _, nickvalue, replacement = nickobj.value
                    table.add_row(
                        str(inum + 1),
                        nickobj.db_category,
                        _cy(nickvalue),
                        _cy(replacement),
                    )
                string = "|wDefined Aliases:|n\n%s" % table
            caller.msg(string)
            return

        if "clearall" in switches:
            caller.nicks.clear()
            caller.account.nicks.clear()
            caller.msg("Cleared all aliases.")
            return

        if "delete" in switches or "del" in switches:
            if not self.args or not self.lhs:
                caller.msg("usage alias/delete <nick> or <#num> ('aliases' for list)")
                return
            # see if a number was given
            arg = self.args.lstrip("#")
            oldnicks = []
            if arg.isdigit():
                # we are given a index in nicklist
                delindex = int(arg)
                if 0 < delindex <= len(nicklist):
                    oldnicks.append(nicklist[delindex - 1])
                else:
                    caller.msg("Not a valid alias index. See 'aliases' for a list.")
                    return
            else:
                if not specified_nicktype:
                    nicktypes = ("object", "account", "inputline")
                for nicktype in nicktypes:
                    oldnicks.append(
                        caller.nicks.get(arg, category=nicktype, return_obj=True)
                    )

            oldnicks = [oldnick for oldnick in oldnicks if oldnick]
            if oldnicks:
                for oldnick in oldnicks:
                    nicktype = oldnick.category
                    nicktypestr = "%s-alias" % nicktype.capitalize()
                    _, _, old_nickstring, old_replstring = oldnick.value
                    caller.nicks.remove(old_nickstring, category=nicktype)
                    caller.msg(
                        f"{nicktypestr} removed: '|w{old_nickstring}|n' -> |w{old_replstring}|n."  # noqa: E501
                    )
            else:
                caller.msg("No matching aliases to remove.")
            return

        if not self.rhs and self.lhs:
            # check what a nick is set to
            strings = []
            if not specified_nicktype:
                nicktypes = ("object", "account", "inputline")
            for nicktype in nicktypes:
                nicks = [
                    nick
                    for nick in utils.make_iter(
                        caller.nicks.get(category=nicktype, return_obj=True)
                    )
                    if nick
                ]
                for nick in nicks:
                    _, _, nick, repl = nick.value
                    if nick.startswith(self.lhs):
                        strings.append(
                            f"{nicktype.capitalize()}-alias: '{nick}' -> '{repl}'"
                        )
            if strings:
                caller.msg("\n".join(strings))
            else:
                caller.msg(f"No aliases found matching '{self.lhs}'")
            return

        if not self.rhs and self.lhs:
            # check what a nick is set to
            strings = []
            if not specified_nicktype:
                nicktypes = ("object", "account", "inputline")
            for nicktype in nicktypes:
                if nicktype == "account":
                    obj = account  # noqa: F821
                else:
                    obj = caller
                nicks = utils.make_iter(
                    obj.nicks.get(category=nicktype, return_obj=True)
                )
                for nick in nicks:
                    _, _, nick, repl = nick.value
                    if nick.startswith(self.lhs):
                        strings.append(
                            f"{nicktype.capitalize()}-alias: '{nick}' -> '{repl}'"
                        )
            if strings:
                caller.msg("\n".join(strings))
            else:
                caller.msg(f"No aliases found matching '{self.lhs}'")
            return

        if not self.rhs and self.lhs:
            # check what a nick is set to
            strings = []
            if not specified_nicktype:
                nicktypes = ("object", "account", "inputline")
            for nicktype in nicktypes:
                if nicktype == "account":
                    obj = account  # noqa: F821
                else:
                    obj = caller
                nicks = utils.make_iter(
                    obj.nicks.get(category=nicktype, return_obj=True)
                )
                for nick in nicks:
                    _, _, nick, repl = nick.value
                    if nick.startswith(self.lhs):
                        strings.append(
                            f"{nicktype.capitalize()}-alias: '{nick}' -> '{repl}'"
                        )
            if strings:
                caller.msg("\n".join(strings))
            else:
                caller.msg(f"No aliases found matching '{self.lhs}'")
            return

        if not self.args or not self.lhs:
            caller.msg("Syntax: alias[/switches] alias = [realname]")
            return

        # setting new aliases

        nickstring = self.lhs
        replstring = self.rhs

        if replstring == nickstring:
            caller.msg("No point in setting alias same as the string to replace...")
            return

        # check so we have a suitable alias type
        errstring = ""
        string = ""
        for nicktype in nicktypes:
            nicktypestr = f"{nicktype.capitalize()}-alias"
            old_nickstring = None
            old_replstring = None

            oldnick = caller.nicks.get(
                key=nickstring, category=nicktype, return_obj=True
            )
            if oldnick:
                _, _, old_nickstring, old_replstring = oldnick.value
            if replstring:
                # creating new nick
                errstring = ""
                if oldnick:
                    if replstring == old_replstring:
                        string += f"\nIdentical {nicktypestr.lower()} already set."
                    else:
                        string += (
                            f"\n{nicktypestr} '|w{old_nickstring}|n' updated to map to"
                            f" '|w{replstring}|n'."
                        )
                else:
                    string += f"\n{nicktypestr} '|w{nickstring}|n' mapped to '|w{replstring}|n'."  # noqa: E501
                try:
                    caller.nicks.add(nickstring, replstring, category=nicktype)
                except NickTemplateInvalid:
                    caller.msg(
                        "You must use the same $-markers both in the alias and in the replacement."  # noqa: E501
                    )
                    return
            elif old_nickstring and old_replstring:
                # just looking at the nick
                string += f"\n{nicktypestr} '|w{old_nickstring}|n' maps to '|w{old_replstring}|n'."  # noqa: E501
                errstring = ""
        string = errstring if errstring else string
        caller.msg(_cy(string))


class CmdBlock(Command):
    """
    Syntax: block <character>

    Block a character from sending you tells. If the character is already
    blocked, this command will unblock them.

    Example: block jake
    """

    key = "block"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        caller = self.caller

        if not self.args:
            return self.msg("Block who?")

        target_name = self.args.strip()
        target = caller.search(target_name, quiet=True, global_search=True)[0]
        if not target:
            return self.msg(f"No characters named '{target_name}' found.")

        # Check if the target is already blocked
        if f"{target.id}" in caller.locks.get("msg"):
            caller.locks.replace("msg:all()")
            caller.msg(f"You unblocked {target.get_display_name(caller)}.")
        else:
            caller.locks.replace(f"msg: not id({target.id})")
            caller.msg(f"You block {target.get_display_name(caller)}.")


class CmdCover(Command):
    """
    Syntax: cover <clothing> with <clothing>

    This command allows a character to cover one clothing object with another.
    Both the clothing objects must be in the character's inventory. The command
    takes two arguments: the first argument is the clothing object to be
    covered, and the second argument is the clothing object to be used as a
    cover.
    """

    key = "cover"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            return caller.msg("Cover what?")

        args = args.split(" with ")

        if len(args) != 2:
            return caller.msg("Cover what with what?")

        obj = caller.search(args[0], candidates=caller.contents)
        if not obj:
            return

        if not isinstance(obj, Clothing):
            return caller.msg("You can't cover that.")

        if obj not in caller.clothing.all():
            return caller.msg("You cannot cover something you aren't wearing.")

        cover = caller.search(args[1], candidates=caller.contents)
        if not cover:
            return

        if not isinstance(cover, Clothing):
            return caller.msg("You can't use that to cover something.")

        if cover not in caller.clothing.all():
            return caller.msg(
                "You cannot use something you aren't wearing to cover something."
            )

        if obj.clothing_type not in CLOTHING_TYPE_COVER[cover.clothing_type]:
            return caller.msg("You can't cover that with that.")

        if cover in obj.covered_by:
            return caller.msg(
                f"{cover.get_display_name(caller)} is already covering {obj.get_display_name(caller)}."
            )

        obj.covered_by.append(cover)
        cover.covering.append(obj)
        caller.location.msg_contents(
            f"$You() $conj(cover) {obj.get_display_name(caller)} with {cover.get_display_name(caller)}.",
            from_obj=caller,
        )


class CmdDrop(Command):
    """
    Syntax: drop [quantity] [obj] [number]
            drop all

    Drops an object or multiple objects from your inventory into your location.
    """

    key = "drop"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def parse(self):
        """
        Simplified parsing logic.
        """
        self.args = self.args.strip().lower()
        self.quantity, self.obj_name, self.number = 1, None, 1  # Default values

        if self.args == "all":
            self.quantity = "all"
        else:
            match = re.match(r"(\d+)\s+(\w+)|(\w+)\s*(\d*)", self.args)
            if match:
                self.obj_name = match.group(2) or match.group(3)
                self.quantity = int(match.group(1)) if match.group(1) else 1
                self.number = int(match.group(4)) if match.group(4) else 1

    def _drop_gold(self, number):
        """
        Handles the logic for dropping gold.
        """
        caller = self.caller
        if number > caller.wealth.value:
            return caller.msg("You don't have that much gold.")

        caller.wealth.base -= number
        self._spawn_gold(caller.location, number)
        caller.location.msg_contents("$You() $conj(drop) some gold.", from_obj=caller)

    def _spawn_gold(self, location, amount):
        """
        Spawns gold at the specified location.
        """
        gold_info = currency.GOLD.copy()
        gold_info.update({"price": amount, "location": location, "home": None})
        spawner.spawn(gold_info)

    def _drop_items(self, quantity, obj_name, number):
        """
        Handles the logic for dropping items other than gold.
        """
        caller = self.caller
        if quantity == "all":
            # Logic to drop all items
            inventory = caller.contents  # Assuming this gets all items in the inventory
            for obj in inventory:
                if not obj.at_pre_drop(caller):
                    continue
                obj.move_to(caller.location, quiet=True, move_type="drop")
                obj.at_drop(caller)
            # Send a consolidated message for all items dropped
            caller.location.msg_contents(
                "$You() $conj(drop) everything.", from_obj=caller
            )
        else:
            dropped_items = []
            for _ in range(quantity):
                obj = caller.search(
                    obj_name,
                    location=caller,
                    nofound_string=f"You aren't carrying {obj_name}.",
                    number=number,
                )

                if not obj:
                    break

                if not obj.at_pre_drop(caller):
                    continue

                obj.move_to(caller.location, quiet=True, move_type="drop")
                obj.at_drop(caller)
                if obj not in dropped_items:
                    dropped_items.append(obj)

            # Send a consolidated message for multiple dropped items
            if dropped_items:
                obj = dropped_items[0]
                quantity = len(dropped_items)
                single, plural = obj.get_numbered_name(quantity, caller)
                item = single if quantity == 1 else f"{quantity} {plural}"
                caller.location.msg_contents(
                    f"$You() $conj(drop) {item}.", from_obj=caller
                )

    def func(self):
        """Implement command"""

        caller = self.caller
        quantity = self.quantity
        obj_name = self.obj_name
        number = self.number

        if not self.args:
            caller.msg("Drop what?")
            return

        if obj_name == "gold":
            self._drop_gold(quantity)
        else:
            self._drop_items(quantity, obj_name, number)


class CmdEmote(Command):
    """
    Syntax: emote <pose>
            omote <pose>
            pmote <pose>

    Examples: emote waves.             -> Jake waves.
              omote Waving, ; smiles.  -> Waving, Jake smiles.
              pmote smile is dazzling. -> Jake's smile is dazzling.

    Describe an action being taken.
      'emote': Starts with your name.
      'omote': Place your name anywhere using ';'.
      'pmote': Starts with your name in possessive form.
    """

    key = "emote"
    aliases = [";", ":", "omote", "pmote"]
    locks = "cmd:all()"
    arg_regex = None

    def parse(self):
        """
        Custom parsing based on cmdstring and the given arguments.
        """
        if self.cmdstring == "emote" or self.cmdstring == ";":
            if self.args and self.args[0] not in ["'", ",", ":"]:
                self.args = " %s" % self.args.strip()

    def func(self):
        """Hook function"""
        if not self.args:
            return self.caller.msg(f"What do you want to {self.cmdstring}?")

        self.args = self.args.strip()

        if self.cmdstring == "emote" or self.cmdstring == ";":
            emote = f"{self.caller.name} {self.args}"
            emote_type = "emote"

        elif self.cmdstring == "omote" or self.cmdstring == ":":
            if self.args.startswith(";"):
                emote = f"{self.caller.name} " + self.args[1:]
                emote_type = "emote"
            else:
                emote = self.args
                emote_type = "omote"

        elif self.cmdstring == "pmote":
            emote = f"{self.caller.name}'s {self.args}"
            emote_type = "pmote"

        emote = self.caller.at_pre_emote(emote, emote_type=emote_type)
        self.caller.location.msg_contents(
            text=(emote, {"type": "pose"}), from_obj=self.caller
        )


class CmdFeel(Command):
    """
    Syntax: feel
            feel <obj>

    feel your surroundings or a specific object.
    """

    key = "feel"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            caller.location.msg_contents(
                "$You() $conj(feel) the air.", from_obj=caller, exclude=caller
            )
            return caller.msg(caller.location.feel)

        obj = caller.search(args)
        if not obj:
            return

        caller.location.msg_contents(
            "$You() $conj(feel) %s." % obj.display_name,
            from_obj=caller,
            exclude=caller,
        )

        caller.msg(obj.feel)


class CmdGet(Command):
    """
    Syntax: get [quantity] [obj] [number] [from [container] [number]]

    Examples: get wand
              get 2 wands
              get wand 2
              get wand from backpack
              get 2 wands from backpack
              get wand 2 from backpack
              get wand from backpack 2
              get 2 wands from backpack 2
              get wand 2 from backpack 2

    Picks up an object from your location or a container in your inventory.
    """

    key = "get"
    aliases = ["take"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def parse(self):
        """
        Parses the input to extract the quantity, object name, container name, and their respective numbers.
        """
        # Regular expression to match various command formats
        regex_pattern = (
            r"(?:(\d+)\s+)?(\w+)(?:\s+(\d+))?(?:\s+from\s+(\w+)(?:\s+(\d+))?)?$"
        )
        match = re.match(regex_pattern, self.args.strip())

        if match:
            # Extracting quantity, object name, object number, container name, and container number
            self.quantity = int(match.group(1)) if match.group(1) else 1
            self.obj_name = match.group(2)
            self.obj_number = int(match.group(3)) if match.group(3) else 1
            self.container_name = match.group(4) if match.group(4) else None
            self.container_number = int(match.group(5)) if match.group(5) else 1
        else:
            # Default values if no match is found
            (
                self.quantity,
                self.obj_name,
                self.obj_number,
                self.container_name,
                self.container_number,
            ) = (1, None, 1, None, 1)

    def _retrieve_currency(self, caller, currency):
        caller.wealth.base += currency.price
        caller.location.msg_contents(
            f"$You() $conj(get) some {currency.get_display_name(caller)}.",
            from_obj=caller,
        )
        currency.delete()

    def _retrieve_obj(self, caller, quantity, obj_name, obj_number, location):
        retrieved_items = []
        for _ in range(quantity):
            obj = caller.search(
                obj_name,
                location=location,
                nofound_string=f"You don't see {obj_name} here.",
                number=obj_number,
                multimatch_string=f"You see more than one {obj_name}:",
            )

            if isinstance(obj, Currency):
                self._retrieve_currency(caller, obj)
                return

            if not obj:
                break

            if not obj.at_pre_get(caller):
                continue

            obj.move_to(caller, quiet=True, move_type="get")
            obj.at_get(caller)
            retrieved_items.append(obj)

        if retrieved_items:
            obj = retrieved_items[0]
            quantity = len(retrieved_items)
            single, plural = obj.get_numbered_name(quantity, caller)
            item = single if quantity == 1 else f"{quantity} {plural}"
            if location == caller.location:
                caller.location.msg_contents(
                    f"$You() $conj(get) {item}.", from_obj=caller
                )
            else:
                caller.location.msg_contents(
                    f"$You() $conj(get) {item} from {location.display_name}.",
                    from_obj=caller,
                )

    def func(self):
        caller = self.caller
        quantity = self.quantity
        obj_name = self.obj_name
        obj_number = self.obj_number
        container_name = self.container_name
        container_number = self.container_number

        if not self.args:
            caller.msg("Get what?")
            return

        if container_name:
            container = caller.search(
                container_name,
                number=container_number,
            )

            if not container:
                return

            if not container.access(caller, "get_from"):
                if container.db.get_from_err_msg:
                    return self.msg(container.db.get_from_err_msg)
                return self.msg("You can't get things from that.")

            location = container
        else:
            location = caller.location

        self._retrieve_obj(caller, quantity, obj_name, obj_number, location)


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
                number=obj_number,
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
                f"$You() $conj(give) {item} to {target.display_name}.",
                from_obj=caller,
            )


class CmdInteract(Command):
    """
    Syntax: interact
            interact <target>

    This command allows the player to interact with the specified target.
    """

    key = "interact"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            if not (interaction := caller.location.db.interaction):
                return caller.msg("Interact with what?")
        else:
            target = caller.search(args)
            if not target:
                return

            if not (interaction := target.db.interaction):
                return caller.msg(
                    f"{target.get_display_name(caller)} is not interactive."
                )

        InteractionMenu(
            caller,
            interaction,
            startnode="node_start",
            auto_look=True,
            auto_help=True,
            persistent=True,
        )


class CmdInteractions(Command):
    """
    Syntax: interactions

    View all the available interactions in your current location.
    """

    key = "interactions"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller

        interactions = [
            item.get_display_name(caller)
            for item in caller.location.contents
            if item.db.interaction
        ]

        if not interactions:
            return caller.msg("There are no interactions here.")

        string = "Interactions:\n - "
        string += "\n - ".join(interactions)
        caller.msg(string)


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

        worn_table = self.create_table(caller.clothing.all(), "Clothing")
        carried_items = [
            obj for obj in caller.contents if obj not in caller.clothing.all()
        ]
        carried_table = self.create_table(carried_items, "Carrying")
        header = self.create_header(caller)
        footer = self.create_footer()

        caller.msg(f"{header}{worn_table}{carried_table}{footer}")

    def create_header(self, caller):
        item_count_line = "|C" + f"Number of Items: {len(caller.contents)}"
        self.max_length = max(self.max_length, len(strip_ansi(item_count_line))) + 2
        header = "|x" + "-" * self.max_length + "|n"
        title = "|C" + "Inventory".center(self.max_length) + "|n"
        weight_line = "|C" + "Weight: 0 / 0".center(self.max_length) + "|n"
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
        else:
            output.extend([item.get_display_name(self.caller) for item in items])

        max_line_length = max([len(strip_ansi(line)) for line in output])
        self.max_length = max(max_line_length, self.max_length) + 1

        return "\n" + "\n ".join(output) + "\n"

    def create_footer(self):
        return "|x" + "-" * self.max_length + "|n"


class CmdListen(Command):
    """
    Syntax: listen

    Listen to your surroundings.
    """

    key = "listen"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            caller.location.msg_contents(
                "$You() $conj(listen) to the surroundings.",
                from_obj=caller,
                exclude=caller,
            )
            return caller.msg(caller.location.smell)

        obj = caller.search(args)
        if not obj:
            return

        caller.location.msg_contents(
            "$You() $conj(listen) to %s." % obj.display_name,
            from_obj=caller,
            exclude=caller,
        )

        caller.msg(obj.sound)


class CmdLook(general.CmdLook):
    """
    Syntax: look
            look <obj>
            look in <container>

    Observes your location or objects in your vicinity.
    """

    rhs_split = (" in ",)

    def look_detail(self):
        """
        Look for detail on room.
        """
        caller = self.caller
        if hasattr(self.caller.location, "get_detail"):
            detail = self.caller.location.get_detail(self.args, looker=self.caller)
            if detail:
                caller.location.msg_contents(
                    f"$You() $conj(look) closely at {self.args}.\n",
                    from_obj=caller,
                    exclude=caller,
                )
                caller.msg(detail)
                return True
        return False

    def func(self):
        """
        Handle the looking.
        """
        caller = self.caller
        if not self.args:
            target = caller.location
            if not target:
                caller.msg("You have no location to look at!")
                return
        else:
            # search, waiting to return errors so we can also check details
            target = caller.search(self.args, quiet=True)
            # if there's no target, check details
            if not target:
                # no target AND no detail means run the normal no-results message
                if not self.look_detail():
                    _AT_SEARCH_RESULT(target, caller, self.args, quiet=False)
                return
            # otherwise, run normal search result handling
            target = caller.search(self.args)
            if not target:
                return
        desc = caller.at_look(target)
        # add the type=look to the outputfunc to make it
        # easy to separate this output in client.
        self.msg(text=(desc, {"type": "look"}), options=None)


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
        regex_pattern = r"(?:(\d+)\s+)?(\w+)(?:\s+(\d+))?\s+in\s+(\w+)(?:\s+(\d+))?"
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
                location=container,
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


class CmdRemove(Command):
    """
    Syntax: remove <obj>

    Removes an item of clothing you are wearing. You can't remove
    clothes that are covered up by something else - you must take
    off the covering item first.
    """

    key = "remove"
    aliases = ["rem"]

    def func(self):
        caller = self.caller
        clothing = caller.search(self.args, candidates=self.caller.contents)
        if not clothing:
            caller.msg("You don't have anything like that.")
            return
        if clothing not in caller.clothing.all():
            caller.msg("You're not wearing that!")
            return
        caller.clothing.remove(clothing)


class CmdSay(Command):
    """
    Syntax: say <message>
            say to <character> <message>
            say to <character>,[character,...] <message>

    Example: say to jake,john Hi there!

    Talk to those in your current location or directly to specific people
    nearby.
    """

    key = "say"
    aliases = ['"', "'"]
    locks = "cmd:all()"
    arg_regex = None

    def func(self):
        caller = self.caller
        args = self.args.strip()
        receivers = []
        if not args:
            caller.msg("Say what?")
            return

        speech = args
        if args.startswith("to "):
            for obj in args.split(" ", 2)[1].split(","):
                receiver = caller.search(obj)
                if not receiver:
                    continue
                receivers.append(receiver)

            if not receivers:
                return caller.msg("Who do you want to talk to?")
            try:
                speech = args.split(" ", 2)[2]
            except IndexError:
                return caller.msg("Have you forgotten what you'd like to say to them?")

        speech = caller.at_pre_say(speech)

        if not speech:
            return

        caller.at_say(
            speech,
            msg_self=True,
            receivers=receivers or None,
            width=self.client_width(),
        )


class CmdSmell(Command):
    """
    Syntax: smell
            smell <obj>

    Smell your surroundings or a specific object.
    """

    key = "smell"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            caller.location.msg_contents(
                "$You() $conj(smell) the air.", from_obj=caller, exclude=caller
            )
            return caller.msg(caller.location.smell)

        obj = caller.search(args)
        if not obj:
            return

        caller.location.msg_contents(
            "$You() $conj(smell) %s." % obj.display_name,
            from_obj=caller,
            exclude=caller,
        )

        caller.msg(obj.smell)


class CmdTaste(Command):
    """
    Syntax: taste
            taste <obj>

    Taste your surroundings or a specific object.
    """

    key = "taste"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            caller.location.msg_contents(
                "$You() $conj(taste) the air.", from_obj=caller, exclude=caller
            )
            return caller.msg(caller.location.taste)

        obj = caller.search(args)
        if not obj:
            return

        caller.location.msg_contents(
            "$You() $conj(taste) %s." % obj.display_name,
            from_obj=caller,
            exclude=caller,
        )

        caller.msg(obj.taste)


class CmdTell(Command):
    """
    Syntax: tell <character> <message>                 # regular tells
            tell <character>,<character>,... <message> # multiple characters tell
            tell <character> ;<emote>                  # emoted tells
            tell <character>,<character>,... ;<emote>  # multiple characters emote

    Example: tell jake,john Hi there!

    Send a message to a character if online. If no argument is given, you
    will receive your most recent message. If sending to multiple
    characters, separate names with commas.
    """

    key = "tell"
    locks = "cmd:all()"
    help_category = "General"

    def _send_message(self, caller, content, receivers, is_emote=False):
        """
        Sends a message to a list of receivers.

        Args:
            caller (Object): The object sending the message.
            content (str): The message content.
            receivers (list): A list of objects to receive the message.
            is_emote (bool, optional): Whether the message is an emote. Defaults to False.
        """  # noqa: E501
        create.create_message(caller, content, receivers=receivers)

        received = []
        rstrings = []
        for target in receivers:
            if not target.access(caller, "msg"):
                rstrings.append(
                    f"You are not allowed to send tells to {target.get_display_name(caller)}."  # noqa: E501
                )
                continue

            if caller == target:
                rstrings.append("Telepathy isn't for inner monologues!")
                continue

            if is_emote:
                target.msg(
                    "Silently from %s: %s" % (caller.get_display_name(target), content)
                )
                logger.log_file(
                    "Silently from %s: %s" % (caller.get_display_name(target), content),
                    filename=f"{target.log_folder}/tells.log",
                )
            else:
                target.msg(f"{caller.get_display_name(target)} tells you: {content}")
                logger.log_file(
                    f"{caller.get_display_name(target)} tells you: {content}",
                    filename=f"{target.log_folder}/tells.log",
                )
            if hasattr(target, "sessions") and not target.sessions.count():
                rstrings.append(f"{target.get_display_name(caller)} is not awake.")
            else:
                received.append(f"{target.get_display_name(caller)}")

        if rstrings:
            self.msg("\n".join(rstrings))

        if not received:
            return

        if is_emote:
            self.msg("Silently to %s: %s" % (", ".join(received), content))
            logger.log_file(
                "Silently to %s: %s" % (", ".join(received), content),
                filename=f"{caller.log_folder}/tells.log",
            )
        else:
            self.msg("You tell %s: %s" % (", ".join(received), content))
            logger.log_file(
                "You tell %s: %s" % (", ".join(received), content),
                filename=f"{caller.log_folder}/tells.log",
            )

    def func(self):
        caller = self.caller

        if not self.args:
            # No argument, show latest messages.
            return self.msg("Syntax: tell <character[s]> <message>")

        args = self.args.strip().split(" ", 1)
        targets, message = args[0].split(","), args[1]

        receivers = [
            caller.search(target, quiet=True, global_search=True)[0]
            for target in targets
            if caller.search(target, quiet=True, global_search=True)
        ]

        message = message.strip()

        if not receivers:
            return self.msg("Who do you want to tell?")

        if not message:
            return self.msg("What do you want to tell them?")

        if message.startswith(";"):
            # Emoted tell
            emote = message[1:].strip()
            if not emote:
                return self.msg("What do you want to emote to them?")
            self._send_message(
                caller, f"{caller.name} {emote}", receivers, is_emote=True
            )
        else:
            # Regular tell
            message = message.strip()
            self._send_message(caller, message, receivers)


class CmdTime(system.CmdTime):
    """
    Syntax: time

    Shows the current in-game time and season.
    """

    key = "time"
    locks = "cmd:all()"
    help_category = "General"

    def parse(self):
        location = self.caller.location
        if (
            not location
            or not hasattr(location, "get_time_of_day")
            or not hasattr(location, "get_season")
        ):
            self.caller.msg("No location available - you are outside time.")
            raise InterruptCommand()
        self.location = location

    def func(self):
        location = self.location

        season = location.get_season()
        timeslot = location.get_time_of_day()

        prep = "an" if season == "autumn" else "a"
        self.caller.msg(f"It's {prep} {season} day, in the {timeslot}.")


class CmdUncover(Command):
    """
    Syntax: uncover <clothing>

    This command allows a character to uncover a specific clothing object that
    is currently covered by another clothing object. The command takes one
    argument, which is the name or key of the object to be uncovered.
    """

    key = "uncover"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            return caller.msg("Uncover what?")

        obj = caller.search(args, candidates=caller.contents)
        if not obj:
            return

        if not isinstance(obj, Clothing):
            return caller.msg("You can't uncover that.")

        if not obj.covered_by:
            return caller.msg(
                f"{obj.get_display_name(caller)} isn't covered by anything."
            )

        for cover in obj.covered_by:
            cover.covering.remove(obj)
            obj.covered_by.remove(cover)

            caller.location.msg_contents(
                f"$You() $conj(uncover) {obj.get_display_name(caller)} from beneath {cover.get_display_name(caller)}.",
                from_obj=caller,
            )


class CmdWealth(Command):
    """
    Syntax: wealth

    Display how much money you have.
    """

    key = "wealth"

    def func(self):
        caller = self.caller
        caller.msg("Total Wealth: %s" % int(caller.wealth.value))


class CmdWear(Command):
    """
    Syntax: wear <obj>

    Examples:
        wear red shirt

    All the clothes you are wearing appear in your description. If you provide
    a style, the message you provide will be displayed after the clothing name.
    """

    key = "wear"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            caller.msg("Usage: wear <obj>")
            return

        clothing = caller.search(args, candidates=caller.contents, quiet=True)
        if not clothing:
            caller.msg("You don't have anything like that.")
            return
        clothing = clothing[0]

        if not inherits_from(clothing, Clothing):
            caller.msg(
                f"{clothing.get_display_name(caller)} isn't something you can wear."
            )
            return

        clothes = caller.clothing.all()

        if clothing in clothes:
            caller.msg("You are already wearing that.")
            return

        if CLOTHING_OVERALL_LIMIT and len(clothes) >= CLOTHING_OVERALL_LIMIT:
            caller.msg("You can't wear any more clothes.")
            return

        caller.clothing.wear(clothing)


class CmdWhisper(Command):
    """
    Syntax: whisper <character> <message>
            whisper <character>,[[character],...] <message>

    Speak privately to one or more characters in your current location without
    others in the room being informed.
    """

    key = "whisper"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()
        if not args:
            caller.msg("Whisper what?")
            return

        args = args.split(" ", 1)
        if len(args) == 1:
            return caller.msg("What do you want to whisper?")

        receivers, whisper = args[0].split(","), args[1] or None
        receivers = [caller.search(target) for target in receivers] or []
        if not receivers:
            return caller.msg("Who do you want to whisper to?")
        if not whisper:
            return caller.msg("What do you want to whisper to them?")

        whisper = caller.at_pre_say(whisper, whisper=True, receivers=receivers)

        if not whisper:
            return

        caller.at_say(
            whisper, msg_self=True, receivers=receivers or None, msg_type="whisper"
        )
