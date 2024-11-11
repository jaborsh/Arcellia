"""
Command module containing CmdOptions for managing account settings.
"""

from codecs import lookup as codecs_lookup

from evennia.utils import utils

from commands.command import Command


class OptionValidator:
    """Handles validation of option values"""

    @staticmethod
    def validate_encoding(value):
        try:
            codecs_lookup(value)
            return value
        except LookupError:
            raise RuntimeError(f"Invalid encoding: '{value}'")

    @staticmethod
    def validate_size(value):
        return {0: int(value)}

    @staticmethod
    def validate_bool(value):
        return value.lower() in ("true", "on", "1")


class CmdOptions(Command):
    """
    Set an account option

    Usage:
      options[/save] [name value]

    Switches:
      save - Save the current option settings for future logins.
      clear - Clear the saved options.
    """

    key = "options"
    aliases = "option"
    switch_options = ("save", "clear")
    locks = "cmd:all()"
    help_category = "Account"
    account_caller = True

    def __init__(self):
        super().__init__()
        self._validator = OptionValidator()
        self._validators = {
            "ANSI": self._validator.validate_bool,
            "CLIENTNAME": utils.to_str,
            "ENCODING": self._validator.validate_encoding,
            "MCCP": self._validator.validate_bool,
            "NOGOAHEAD": self._validator.validate_bool,
            "MXP": self._validator.validate_bool,
            "NOCOLOR": self._validator.validate_bool,
            "NOPKEEPALIVE": self._validator.validate_bool,
            "OOB": self._validator.validate_bool,
            "RAW": self._validator.validate_bool,
            "SCREENHEIGHT": self._validator.validate_size,
            "SCREENWIDTH": self._validator.validate_size,
            "SCREENREADER": self._validator.validate_bool,
            "TERM": utils.to_str,
            "UTF-8": self._validator.validate_bool,
            "XTERM256": self._validator.validate_bool,
            "INPUTDEBUG": self._validator.validate_bool,
            "FORCEDENDLINE": self._validator.validate_bool,
            "LOCALECHO": self._validator.validate_bool,
        }

    def _format_dimensions(self, options, dimension):
        """Format screen dimensions for display"""
        if dimension in options:
            if len(options[dimension]) == 1:
                options[dimension] = options[dimension][0]
            else:
                options[dimension] = "  \n".join(
                    f"{screenid} : {size}"
                    for screenid, size in options[dimension].items()
                )

    def _display_options(self):
        """Display current option settings"""
        flags = self.session.protocol_flags
        options = dict(flags)
        saved_options = dict(
            self.caller.attributes.get("_saved_protocol_flags", default={})
        )

        self._format_dimensions(options, "SCREENWIDTH")
        self._format_dimensions(options, "SCREENHEIGHT")
        options.pop("TTYPE", None)

        header = (
            ("Name", "Value", "Saved") if saved_options else ("Name", "Value")
        )
        table = self.styled_table(*header)
        for key in sorted(options):
            row = [key, options[key]]
            if saved_options:
                saved = " |YYes|n" if key in saved_options else ""
                changed = (
                    "|y*|n"
                    if key in saved_options and flags[key] != saved_options[key]
                    else ""
                )
                row.append("%s%s" % (saved, changed))
            table.add_row(*row)
        self.msg(
            f"|wClient settings ({self.session.protocol_key}):|n\n{table}|n"
        )

    def _update_option(self, name, value):
        """Update a single option with validation"""
        flags = self.session.protocol_flags
        validator = self._validators.get(name)

        if not validator:
            self.msg(f"|rNo option named '{name}'.")
            return False

        try:
            old_val = flags.get(name, False)
            new_val = validator(value)

            if old_val == new_val:
                self.msg(f"Option {name} unchanged from '{old_val}'.")
            else:
                flags[name] = new_val
                self.msg(f"Option {name} changed: '{old_val}' -> '{new_val}'")
            return {name: new_val}

        except Exception as err:
            self.msg(f"|rError setting {name}: {err}")
            return False

    def _handle_save_clear(self, optiondict):
        """Handle save/clear switches for options"""
        if not optiondict:
            return

        if "save" in self.switches:
            saved_opts = self.account.attributes.get(
                "_saved_protocol_flags", default={}
            )
            saved_opts.update(optiondict)
            self.account.attributes.add("_saved_protocol_flags", saved_opts)
            for key in optiondict:
                self.msg(f"|gSaved option {key}.|n")

        if "clear" in self.switches:
            for key in optiondict:
                self.caller.attributes.get("_saved_protocol_flags", {}).pop(
                    key, None
                )
                self.msg(f"|gCleared saved {key}.")

    def func(self):
        """Main command function"""
        if not self.session:
            return

        if not self.args:
            self._display_options()
            return

        args = self.args.strip().split(None, 1)
        if len(args) != 2:
            self.msg("Usage: option [name] [value]")
            return

        name, value = args
        name = name.upper()
        value = value.strip()
        optiondict = self._update_option(name, value)

        self._handle_save_clear(optiondict)
        if optiondict:
            self.session.update_flags(**optiondict)
