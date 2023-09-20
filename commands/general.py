import re

from django.conf import settings
from evennia.commands.default import general as default_general
from evennia.typeclasses.attributes import NickTemplateInvalid
from evennia.utils import class_from_module, utils

COMMAND_DEFAULT_CLASS = class_from_module(settings.COMMAND_DEFAULT_CLASS)
__all__ = ["CmdAlias", "CmdLook"]


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


class CmdLook(default_general.CmdLook):
    """
    Usage: look
           look <obj>

    Observes your location or objects in your vicinity.
    """
