import re

from django.conf import settings
from evennia.commands.default import general, system
from evennia.typeclasses.attributes import NickTemplateInvalid
from evennia.utils import (
    at_search_result,
    class_from_module,
    create,
    evtable,
    inherits_from,
    utils,
)
from server.conf import logger
from typeclasses import clothing as clothing_typeclass

from commands.command import Command

COMMAND_DEFAULT_CLASS = class_from_module(settings.COMMAND_DEFAULT_CLASS)
__all__ = [
    "CmdAlias",
    "CmdBlock",
    "CmdDrop",
    "CmdEmote",
    "CmdGet",
    "CmdGive",
    "CmdInventory",
    "CmdLook",
    "CmdRemove",
    "CmdSay",
    "CmdTell",
    "CmdTime",
    "CmdWhisper",
    "CmdWear",
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


class CmdDrop(general.CmdDrop):
    """
    Syntax: drop <obj>

    Drops an object from your inventory into your location.
    """


class CmdEmote(Command):
    """
    Syntax: emote <pose>
            omote <pose>
            pmote <pose>

    Examples: emote waves.           -> Jake waves.
              omote Waving, ; smiles. -> Waving, Jake smiles.
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


class CmdGet(general.CmdGet):
    """
    Syntax: get <obj>

    Picks up an object from your location and puts it in your inventory.
    """


class CmdGive(general.CmdGive):
    """
    Syntax: give <inventory object> to <target>

    Gives an item from your inventory to another person, placing it in their
    inventory.
    """

    key = "give"
    rhs_split = " to "
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement give"""

        caller = self.caller
        if not self.args or not self.rhs:
            caller.msg("Syntax: give <inventory object> to <target>")
            return
        to_give = caller.search(
            self.lhs,
            location=caller,
            nofound_string=f"You aren't carrying {self.lhs}.",
            multimatch_string=f"You carry more than one {self.lhs}:",
        )
        target = caller.search(self.rhs)
        if not (to_give and target):
            return

        singular, _ = to_give.get_numbered_name(1, caller)
        if target == caller:
            caller.msg(f"You keep {singular} to yourself.")
            return
        if not to_give.location == caller:
            caller.msg(f"You are not holding {singular}.")
            return

        # calling at_pre_give hook method
        if not to_give.at_pre_give(caller, target):
            return

        # give object
        success = to_give.move_to(target, quiet=True, move_type="give")
        if not success:
            caller.msg(f"You could not give {singular} to {target.key}.")
        else:
            caller.msg(f"You give {singular} to {target.key}.")
            target.msg(f"{caller.key} gives you {singular}.")
            # Call the object script's at_give() method.
            to_give.at_give(caller, target)


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

    def func(self):
        """check inventory"""
        if not self.caller.contents:
            self.caller.msg("You are not carrying or wearing anything.")
            return

        message_list = []

        items = self.caller.contents

        carry_table = evtable.EvTable(border="header")
        wear_table = evtable.EvTable(border="header")

        carried = [obj for obj in items if obj not in self.caller.clothes]
        worn = [obj for obj in items if obj in self.caller.clothes]

        message_list.append("|wYou are carrying:|n")
        for item in carried:
            carry_table.add_row(
                item.get_display_name(self.caller), item.get_display_desc(self.caller)
            )
        if carry_table.nrows == 0:
            carry_table.add_row("Nothing.", "")
        message_list.append(str(carry_table))

        message_list.append("|wYou are wearing:|n")
        for item in worn:
            item_name = item.get_display_name(self.caller)
            if item.db.covered_by:
                item_name += " (hidden)"
            wear_table.add_row(item_name, item.get_display_desc(self.caller))
        if wear_table.nrows == 0:
            wear_table.add_row("Nothing.", "")
        message_list.append(str(wear_table))

        self.caller.msg("\n".join(message_list))


class CmdLook(general.CmdLook):
    """
    Syntax: look
            look <obj>

    Observes your location or objects in your vicinity.
    """


class CmdRemove(Command):
    """
    Syntax: remove <obj>

    Removes an item of clothing you are wearing. You can't remove
    clothes that are covered up by something else - you must take
    off the covering item first.
    """

    key = "remove"
    help_category = "clothing"

    def func(self):
        clothing = self.caller.search(self.args, candidates=self.caller.contents)
        if not clothing:
            self.caller.msg("You don't have anything like that.")
            return
        if clothing not in self.caller.clothes.get():
            self.caller.msg("You're not wearing that!")
            return
        if clothing.covered_by:
            self.caller.msg(
                f"You have to take off {', '.join(clothing.covered_by)} first."
            )
            return
        clothing.remove(self.caller)


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

        caller.at_say(speech, msg_self=True, receivers=receivers or None)


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

    List Server time statistics such as uptime
    and the current time stamp.
    """

    key = "time"
    aliases = "uptime"
    locks = "cmd:all()"
    help_category = "General"


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


class CmdWear(Command):
    """
    Syntax: wear <obj> [wear style]

    Examples:
        wear red shirt
        wear scarf wrapped loosely around the neck

    All the clothes you are wearing appear in your description. If you provide
    a style, the message you provide will be displayed after the clothing name.
    """

    key = "wear"
    help_category = "General"

    def func(self):
        if not self.args:
            self.caller.msg("Usage: wear <obj> [=] [wear style]")
            return
        if not self.rhs:
            # check if the whole string is an object
            clothing = self.caller.search(
                self.lhs, candidates=self.caller.contents, quiet=True
            )
            if not clothing:
                # split out the first word as the object and the rest as the wearstyle
                argslist = self.lhs.split()
                self.lhs = argslist[0]
                self.rhs = " ".join(argslist[1:])
                clothing = self.caller.search(self.lhs, candidates=self.caller.contents)
            else:
                # pass the result through the search-result hook
                clothing = at_search_result(clothing, self.caller, self.lhs)

        else:
            # it had an explicit separator - just do a normal search for the lhs
            clothing = self.caller.search(self.lhs, candidates=self.caller.contents)

        if not clothing:
            return
        if not inherits_from(clothing, clothing_typeclass.Clothing):
            self.caller.msg(f"{clothing.name} isn't something you can wear.")
            return

        if clothing in self.caller.clothes.get():
            if not self.rhs:
                # If no wearstyle was provided and the clothing is already being worn, do nothing
                self.caller.msg(f"You're already wearing your {clothing.name}.")
                return
            elif len(self.rhs) > clothing_typeclass.WEARSTYLE_MAXLENGTH:
                self.caller.msg(
                    f"Please keep your wear style message to less than {clothing_typeclass.WEARSTYLE_MAXLENGTH} characters."
                )
                return
            else:
                # Adjust the wearstyle
                clothing.db.worn = self.rhs
                self.caller.location.msg_contents(
                    f"$You() $conj(wear) {clothing.name} {self.rhs}.",
                    from_obj=self.caller,
                )
                return

        already_worn = clothing_typeclass.get_worn_clothes(self.caller)

        # Enforce overall clothing limit.
        if (
            clothing_typeclass.CLOTHING_OVERALL_LIMIT
            and len(already_worn) >= clothing_typeclass.CLOTHING_OVERALL_LIMIT
        ):
            self.caller.msg("You can't wear any more clothes.")
            return

        # Apply individual clothing type limits.
        if clothing_type := clothing.db.type:
            if clothing_type in clothing_typeclass.CLOTHING_TYPE_LIMIT:
                type_count = clothing_typeclass.single_type_count(
                    already_worn, clothing_type
                )
                if type_count >= clothing_typeclass.CLOTHING_TYPE_LIMIT[clothing_type]:
                    self.caller.msg(
                        "You can't wear any more clothes of the type '{clothing_type}'."
                    )
                    return

        wearstyle = self.rhs or True
        clothing.wear(self.caller, wearstyle)
