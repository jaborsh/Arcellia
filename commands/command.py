"""
Commands

Commands describe the input the account can do to the game.

"""

from evennia.commands.command import Command as BaseCommand
from evennia.utils import utils

# from evennia import default_cmds


class Command(BaseCommand):
    """
    Base command (you may see this if a child command had no help text defined)

    Note that the class's `__doc__` string is used by Evennia to create the
    automatic help entry for the command, so make sure to document consistently
    here. Without setting one, the parent's docstring will show (like now).

    """

    # Each Command class implements the following methods, called in this order
    # (only func() is actually required):
    #
    #     - at_pre_cmd(): If this returns anything truthy, execution is aborted.
    #     - parse(): Should perform any extra parsing needed on self.args
    #         and store the result on self.
    #     - func(): Performs the actual work.
    #     - at_post_cmd(): Extra actions, often things done after
    #         every command, like prompts.
    #

    def parse(self):
        """
        This method is called by the cmdhandler once the command name
        has been identified. It creates a new set of member variables
        that can be later accessed from self.func() (see below)

        The following variables are available for our use when entering this
        method (from the command definition, and assigned on the fly by the
        cmdhandler):
           self.key - the name of this command ('look')
           self.aliases - the aliases of this cmd ('l')
           self.permissions - permission string for this command
           self.help_category - overall category of command

           self.caller - the object calling this command
           self.cmdstring - the actual command name used to call this
                            (this allows you to know which alias was used,
                             for example)
           self.args - the raw input; everything following self.cmdstring.
           self.cmdset - the cmdset from which this command was picked. Not
                         often used (useful for commands like 'help' or to
                         list all available commands etc)
           self.obj - the object on which this command was defined. It is often
                         the same as self.caller.

        A MUX command has the following possible syntax:

          name[ with several words][/switch[/switch..]] arg1[,arg2,...] [[=|,] arg[,..]]

        The 'name[ with several words]' part is already dealt with by the
        cmdhandler at this point, and stored in self.cmdname (we don't use
        it here). The rest of the command is stored in self.args, which can
        start with the switch indicator /.

        Optional variables to aid in parsing, if set:
          self.switch_options  - (tuple of valid /switches expected by this
                                  command (without the /))
          self.rhs_split       - Alternate string delimiter or tuple of strings
                                 to separate left/right hand sides. tuple form
                                 gives priority split to first string delimiter.

        This parser breaks self.args into its constituents and stores them in the
        following variables:
          self.switches = [list of /switches (without the /)]
          self.raw = This is the raw argument input, including switches
          self.args = This is re-defined to be everything *except* the switches
          self.lhs = Everything to the left of = (lhs:'left-hand side'). If
                     no = is found, this is identical to self.args.
          self.rhs: Everything to the right of = (rhs:'right-hand side').
                    If no '=' is found, this is None.
          self.lhslist - [self.lhs split into a list by comma]
          self.rhslist - [list of self.rhs split into a list by comma]
          self.arglist = [list of space-separated args (stripped, including '=' if it exists)]

          All args and list members are stripped of excess whitespace around the
          strings, but case is preserved.
        """
        raw = self.args
        args = raw.strip()
        # Without explicitly setting these attributes, they assume default values:
        if not hasattr(self, "switch_options"):
            self.switch_options = None
        if not hasattr(self, "rhs_split"):
            self.rhs_split = "="
        if not hasattr(self, "account_caller"):
            self.account_caller = False

        # split out switches
        switches, delimiters = [], self.rhs_split
        if self.switch_options:
            self.switch_options = [opt.lower() for opt in self.switch_options]
        if args and len(args) > 1 and raw[0] == "/":
            # we have a switch, or a set of switches. These end with a space.
            switches = args[1:].split(None, 1)
            if len(switches) > 1:
                switches, args = switches
                switches = switches.split("/")
            else:
                args = ""
                switches = switches[0].split("/")
            # If user-provides switches, parse them with parser switch options.
            if switches and self.switch_options:
                valid_switches, unused_switches, extra_switches = [], [], []
                for element in switches:
                    option_check = [
                        opt for opt in self.switch_options if opt == element
                    ]
                    if not option_check:
                        option_check = [
                            opt
                            for opt in self.switch_options
                            if opt.startswith(element)
                        ]
                    match_count = len(option_check)
                    if match_count > 1:
                        extra_switches.extend(
                            option_check
                        )  # Either the option provided is ambiguous,
                    elif match_count == 1:
                        valid_switches.extend(
                            option_check
                        )  # or it is a valid option abbreviation,
                    elif match_count == 0:
                        unused_switches.append(
                            element
                        )  # or an extraneous option to be ignored.
                if extra_switches:  # User provided switches
                    self.msg(
                        "|g%s|n: |wAmbiguous switch supplied: Did you mean /|C%s|w?"
                        % (self.cmdstring, " |nor /|C".join(extra_switches))
                    )
                if unused_switches:
                    plural = "" if len(unused_switches) == 1 else "es"
                    self.msg(
                        '|g%s|n: |wExtra switch%s "/|C%s|w" ignored.'
                        % (
                            self.cmdstring,
                            plural,
                            "|n, /|C".join(unused_switches),
                        )
                    )
                switches = valid_switches  # Only include valid_switches in command function call
        arglist = [arg.strip() for arg in args.split()]

        # check for arg1, arg2, ... = argA, argB, ... constructs
        lhs, rhs = args.strip(), None
        if lhs:
            if delimiters and hasattr(
                delimiters, "__iter__"
            ):  # If delimiter is iterable,
                best_split = delimiters[0]  # (default to first delimiter)
                for this_split in delimiters:  # try each delimiter
                    if this_split in lhs:  # to find first successful split
                        best_split = this_split  # to be the best split.
                        break
            else:
                best_split = delimiters
            # Parse to separate left into left/right sides using best_split delimiter string
            if best_split in lhs:
                lhs, rhs = lhs.split(best_split, 1)
        # Trim user-injected whitespace
        rhs = rhs.strip() if rhs is not None else None
        lhs = lhs.strip()
        # Further split left/right sides by comma delimiter
        lhslist = (
            [arg.strip() for arg in lhs.split(",")] if lhs is not None else []
        )
        rhslist = (
            [arg.strip() for arg in rhs.split(",")] if rhs is not None else []
        )
        # save to object properties:
        self.raw = raw
        self.switches = switches
        self.args = args.strip()
        self.arglist = arglist
        self.lhs = lhs
        self.lhslist = lhslist
        self.rhs = rhs
        self.rhslist = rhslist

        # if the class has the account_caller property set on itself, we make
        # sure that self.caller is always the account if possible. We also create
        # a special property "character" for the puppeted object, if any. This
        # is convenient for commands defined on the Account only.
        if self.account_caller:
            if utils.inherits_from(
                self.caller, "evennia.objects.objects.DefaultObject"
            ):
                # caller is an Object/Character
                self.character = self.caller
                self.caller = self.caller.account
            elif utils.inherits_from(
                self.caller, "evennia.accounts.accounts.DefaultAccount"
            ):
                # caller was already an Account
                self.character = self.caller.get_puppet(self.session)
            else:
                self.character = None

    def at_pre_cmd(self):
        if self.account:
            for watcher in self.caller.ndb._watchers or []:
                watcher.msg(
                    f"|y[{self.caller}]|Y> {self.cmdstring}{self.args}|n"
                )

            if (
                self.caller.permissions.check("petrified")
                and not self.caller.is_superuser
            ):
                self.caller.msg(
                    "|#6C6C6CYou are petrified and cannot perform actions.|n"
                )
                return True
            return False

    def at_post_cmd(self):
        self.caller.msg(prompt="> ")
