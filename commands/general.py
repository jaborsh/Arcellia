import re

from django.conf import settings
from evennia.commands.default import general as default_general
from evennia.typeclasses.attributes import NickTemplateInvalid
from evennia.utils import class_from_module, create, utils

from commands.command import Command

COMMAND_DEFAULT_CLASS = class_from_module(settings.COMMAND_DEFAULT_CLASS)
__all__ = [
    "CmdAlias",
    "CmdBlock",
    "CmdDrop",
    "CmdGet",
    "CmdGive",
    "CmdInventory",
    "CmdLook",
    "CmdTell",
]


class CmdAlias(default_general.CmdNick):
    """
    Usage: alias[/switches] <string> [= [replacement_string]]
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
                        f"{nicktypestr} removed: '|w{old_nickstring}|n' -> |w{old_replstring}|n."
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
            caller.msg("Usage: alias[/switches] alias = [realname]")
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
                    string += f"\n{nicktypestr} '|w{nickstring}|n' mapped to '|w{replstring}|n'."
                try:
                    caller.nicks.add(nickstring, replstring, category=nicktype)
                except NickTemplateInvalid:
                    caller.msg(
                        "You must use the same $-markers both in the alias and in the replacement."
                    )
                    return
            elif old_nickstring and old_replstring:
                # just looking at the nick
                string += f"\n{nicktypestr} '|w{old_nickstring}|n' maps to '|w{old_replstring}|n'."
                errstring = ""
        string = errstring if errstring else string
        caller.msg(_cy(string))


class CmdBlock(Command):
    """
    Usage: block <character>

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


class CmdDrop(default_general.CmdDrop):
    """
    Usage: drop <obj>

    Drops an object from your inventory into your location.
    """


class CmdGet(default_general.CmdGet):
    """
    Usage: get <obj>

    Picks up an object from your location and puts it in your inventory.
    """


class CmdGive(default_general.CmdGive):
    """
    Usage: give <inventory object> to <target>

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
            caller.msg("Usage: give <inventory object> to <target>")
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


class CmdInventory(default_general.CmdInventory):
    """
    Usage: i
           inv
           inventory

    Shows your inventory
    """


class CmdLook(default_general.CmdLook):
    """
    Usage: look
           look <obj>

    Observes your location or objects in your vicinity.
    """


class CmdTell(Command):
    """
    Usage: tell <character> <message>                 # regular tells
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
        """
        create.create_message(caller, content, receivers=receivers)

        received = []
        rstrings = []
        for target in receivers:
            if not target.access(caller, "msg"):
                rstrings.append(
                    f"You are not allowed to send tells to {target.get_display_name(caller)}."
                )
                continue
            if is_emote:
                target.msg("Privately, %s" % (content))
            else:
                target.msg(f"{caller.get_display_name(target)} tells you: {content}")
            if hasattr(target, "sessions") and not target.sessions.count():
                rstrings.append(f"{target.get_display_name(caller)} is not awake.")
            else:
                received.append(f"{target.get_display_name(caller)}")

        if rstrings:
            self.msg("\n".join(rstrings))

        if not received:
            return

        if is_emote:
            self.msg("Privately to %s: %s" % (", ".join(received), content))
        else:
            self.msg("You tell %s: %s" % (", ".join(received), content))

    def func(self):
        caller = self.caller

        if not self.args:
            # No argument, show latest messages.
            return self.msg("Usage: tell <character[s]> <message>")

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
