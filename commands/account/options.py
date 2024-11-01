"""
Command module containing CmdOptions.
"""

from codecs import lookup as codecs_lookup

from evennia.utils import utils

from commands.command import Command


class CmdOptions(Command):
    """
    Set an account option

    Usage:
      options[/save] [name = value]

    Switches:
      save - Save the current option settings for future logins.
      clear - Clear the saved options.

    This command allows for viewing and setting client interface
    settings. Note that saved options may not be able to be used if
    later connecting with a client with different capabilities.
    """

    key = "options"
    aliases = "option"
    switch_options = ("save", "clear")
    locks = "cmd:all()"
    help_category = "Account"

    # this is used by the parent
    account_caller = True

    def func(self):
        """
        Implements the command
        """
        if self.session is None:
            return

        flags = self.session.protocol_flags

        # Display current options
        if not self.args:
            # list the option settings

            if "save" in self.switches:
                # save all options
                self.caller.db._saved_protocol_flags = flags
                self.msg("|gSaved all options. Use option/clear to remove.|n")
            if "clear" in self.switches:
                # clear all saves
                self.caller.db._saved_protocol_flags = {}
                self.msg("|gCleared all saved options.")

            options = dict(flags)  # make a copy of the flag dict
            saved_options = dict(
                self.caller.attributes.get("_saved_protocol_flags", default={})
            )

            if "SCREENWIDTH" in options:
                if len(options["SCREENWIDTH"]) == 1:
                    options["SCREENWIDTH"] = options["SCREENWIDTH"][0]
                else:
                    options["SCREENWIDTH"] = "  \n".join(
                        "%s : %s" % (screenid, size)
                        for screenid, size in options["SCREENWIDTH"].items()
                    )
            if "SCREENHEIGHT" in options:
                if len(options["SCREENHEIGHT"]) == 1:
                    options["SCREENHEIGHT"] = options["SCREENHEIGHT"][0]
                else:
                    options["SCREENHEIGHT"] = "  \n".join(
                        "%s : %s" % (screenid, size)
                        for screenid, size in options["SCREENHEIGHT"].items()
                    )
            options.pop("TTYPE", None)

            header = (
                ("Name", "Value", "Saved")
                if saved_options
                else ("Name", "Value")
            )
            table = self.styled_table(*header)
            for key in sorted(options):
                row = [key, options[key]]
                if saved_options:
                    saved = " |YYes|n" if key in saved_options else ""
                    changed = (
                        "|y*|n"
                        if key in saved_options
                        and flags[key] != saved_options[key]
                        else ""
                    )
                    row.append("%s%s" % (saved, changed))
                table.add_row(*row)
            self.msg(
                f"|wClient settings ({self.session.protocol_key}):|n\n{table}|n"
            )

            return

        if not self.rhs:
            self.msg("Usage: option [name = [value]]")
            return

        # Try to assign new values

        def validate_encoding(new_encoding):
            # helper: change encoding
            try:
                codecs_lookup(new_encoding)
            except LookupError:
                raise RuntimeError(
                    f"The encoding '|w{new_encoding}|n' is invalid. "
                )
            return val

        def validate_size(new_size):
            return {0: int(new_size)}

        def validate_bool(new_bool):
            return True if new_bool.lower() in ("true", "on", "1") else False

        def update(new_name, new_val, validator):
            # helper: update property and report errors
            try:
                old_val = flags.get(new_name, False)
                new_val = validator(new_val)
                if old_val == new_val:
                    self.msg(
                        f"Option |w{new_name}|n was kept as '|w{old_val}|n'."
                    )
                else:
                    flags[new_name] = new_val
                    self.msg(
                        f"Option |w{new_name}|n was changed from '|w{old_val}|n' to"
                        f" '|w{new_val}|n'."
                    )
                return {new_name: new_val}
            except Exception as err:
                self.msg(f"|rCould not set option |w{new_name}|r:|n {err}")
                return False

        validators = {
            "ANSI": validate_bool,
            "CLIENTNAME": utils.to_str,
            "ENCODING": validate_encoding,
            "MCCP": validate_bool,
            "NOGOAHEAD": validate_bool,
            "MXP": validate_bool,
            "NOCOLOR": validate_bool,
            "NOPKEEPALIVE": validate_bool,
            "OOB": validate_bool,
            "RAW": validate_bool,
            "SCREENHEIGHT": validate_size,
            "SCREENWIDTH": validate_size,
            "SCREENREADER": validate_bool,
            "TERM": utils.to_str,
            "UTF-8": validate_bool,
            "XTERM256": validate_bool,
            "INPUTDEBUG": validate_bool,
            "FORCEDENDLINE": validate_bool,
            "LOCALECHO": validate_bool,
        }

        name = self.lhs.upper()
        val = self.rhs.strip()
        optiondict = False
        if val and name in validators:
            optiondict = update(name, val, validators[name])
        else:
            self.msg("|rNo option named '|w%s|r'." % name)
        if optiondict:
            # a valid setting
            if "save" in self.switches:
                # save this option only
                saved_options = self.account.attributes.get(
                    "_saved_protocol_flags", default={}
                )
                saved_options.update(optiondict)
                self.account.attributes.add(
                    "_saved_protocol_flags", saved_options
                )
                for key in optiondict:
                    self.msg(f"|gSaved option {key}.|n")
            if "clear" in self.switches:
                # clear this save
                for key in optiondict:
                    self.account.attributes.get(
                        "_saved_protocol_flags", {}
                    ).pop(key, None)
                    self.msg(f"|gCleared saved {key}.")
            self.session.update_flags(**optiondict)
