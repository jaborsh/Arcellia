import time
from codecs import lookup as codecs_lookup
from datetime import datetime

from django.conf import settings
from menus.amenu import AMenu
from server.conf import logger
from utils.colors import strip_ansi

from commands.command import Command
from evennia.objects.models import ObjectDB
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import create, search, utils
from evennia.utils.evmenu import get_input

_MAX_NR_CHARACTERS = settings.MAX_NR_CHARACTERS
_AUTO_PUPPET_ON_LOGIN = settings.AUTO_PUPPET_ON_LOGIN

__all__ = (
    "CmdCreate",
    "CmdDelete",
    "CmdDisconnect",
    "CmdOOCLook",
    "CmdOptions",
    "CmdPassword",
    "CmdPlay",
    "CmdQuit",
    "CmdSessions",
    "CmdSetMain",
    "CmdWho",
)


class CmdCreate(Command):
    """
    Command to create a new character.

    Syntax: create <name>

    This command allows players to create a new character. The name of the character
    should be provided as an argument. The command performs various checks to ensure
    the name is valid and not already taken. If the name passes all checks, a new
    character object is created and associated with the player's account.

    The command also prompts the player to confirm the name and check if it complies
    with the game's rules for character names.
    """

    key = "create"
    locks = "cmd:is_ooc() and pperm(Player)"
    help_category = "Account"
    account_caller = True

    def func(self):
        account = self.account
        session = self.session

        if not self.args:
            self.msg("Syntax: create <name>")
            return

        if (
            _MAX_NR_CHARACTERS is not None
            and not account.is_superuser
            and not account.check_permstring("Developer")
        ):
            if len(account.db._playable_characters) >= _MAX_NR_CHARACTERS:
                plural = "" if _MAX_NR_CHARACTERS == 1 else "s"
                self.msg(
                    f"You may only have a maximum of {_MAX_NR_CHARACTERS} character{plural}."
                )
                return

        key = self.args.replace(" ", "").capitalize()[:16]

        if not key.isalpha():
            self.msg("|rYour character's name may only contain letters.|n")
            return

        typeclass = settings.BASE_CHARACTER_TYPECLASS

        if ObjectDB.objects.filter(
            db_typeclass_path=typeclass, db_key__iexact=key
        ).exists():
            self.msg(f"|rA character named '|w{key}|r' already exists.|n")
            return

        rules_string = (
            "The following rules apply to names:\n\n"
            "1. |gNames should be distinct from iconic media characters.|n\n"
            "2. |gNames should suit the game's theme and setting.|n\n"
            "3. |gNames should be understandable and pronounceable.|n"
        )
        self.msg(rules_string)

        def _callback(caller, callback_prompt, result):
            if result.lower() not in ["yes", "y"]:
                self.msg("Creation aborted.")
                return

            start_location = ObjectDB.objects.get_id(settings.START_LOCATION)
            default_home = ObjectDB.objects.get_id(settings.DEFAULT_HOME)
            permissions = settings.PERMISSION_ACCOUNT_DEFAULT

            new_character = create.create_object(
                typeclass,
                key=key,
                location=start_location,
                home=default_home,
                permissions=permissions,
            )
            new_character.locks.add(
                f"puppet:id({new_character.id}) or pid({account.id}) or perm(Developer) or pperm(Developer);"
                f"delete:id({account.id}) or perm(Admin)"
            )
            account.db._playable_characters.append(new_character)
            new_character.db.desc = "This is a character."

            logger.log_sec(
                f"Character Created: {new_character} (Account: {account}, IP: {session.address})."
            )

            try:
                account.puppet_object(session, new_character)
                account.db._last_puppet = new_character
                logger.log_sec(f"{new_character} enters the game (Account: {account}).")
            except RuntimeError as error:
                self.msg(f"|rYou cannot become |C{new_character.name}|n: {error}")
                logger.log_sec(
                    f"{new_character} fails to enter the game (Account: {account})."
                )
                return

            AMenu(
                new_character,
                "world.chargen.menu",
                startnode="chargen_welcome",
                auto_look=True,
                auto_help=True,
                cmd_on_exit=None,
                persistent=True,
            )

        prompt = f"\nDid you enter '|w{key}|n' correctly and does this name comply with the rules? |r[Y/n]|n"
        get_input(account, prompt, _callback)


class CmdDelete(Command):
    """
    Command to delete a character associated with the account.

    Usage:
      delete <name>

    This command allows the player to delete one of their characters. The character
    to be deleted is specified by its name. If there are multiple characters with
    the same name, an admin needs to be contacted to delete the correct one.

    Deleting a character is a permanent action and cannot be undone. The command
    checks if the player has permission to delete the character before proceeding.

    Example:
      delete JohnDoe

    This will permanently delete the character named 'JohnDoe' associated with
    the player's account.
    """

    key = "delete"
    locks = "cmd:is_ooc() and pperm(Player)"
    help_category = "Account"
    account_caller = True

    def func(self):
        account = self.account

        if not self.args:
            self.msg("Syntax: delete <name>")
            return

        char_name = self.args.strip().lower()
        match = [
            char
            for char in utils.make_iter(account.db._playable_characters)
            if char.key.lower() == char_name
        ]

        if not match:
            self.msg("You have no such character to delete.")
            return

        if len(match) > 1:
            self.msg(
                "Aborting - there are two characters with the same name. Ask an admin to delete the right one."
            )
            return

        char_to_delete = match[0]

        if not char_to_delete.access(account, "delete"):
            self.msg("You do not have permission to delete this character.")
            return

        def _delete_character(account, prompt, result):
            if result.lower() not in ["yes", "y"]:
                self.msg("Deletion aborted.")
                return

            key = char_to_delete.key
            account.db._playable_characters = [
                pc for pc in account.db._playable_characters if pc != char_to_delete
            ]
            char_to_delete.delete()
            self.msg(f"Character '|w{key}|n' permanently deleted.")
            logger.log_sec(f"Character Deleted: {key} (Account: {account}).")

        prompt = f"|rThis will permanently delete |n'|w{char_to_delete.key}|n'|r. This cannot be undone!|n Continue? |r[Y/n]|n"
        get_input(account, prompt, _delete_character)


class CmdDisconnect(Command):
    """
    Command to disconnect a character from the game.

    Usage:
      disconnect

    This command allows a player to disconnect their character from the game,
    effectively going out-of-character (OOC). The character will no longer be
    visible or interactable in the game world.
    """

    key = "disconnect"
    aliases = ["disc", "unpuppet"]
    help_category = "Account"

    def func(self):
        """Implement function"""
        account = self.account
        session = self.session
        old_char = account.get_puppet(session)

        if not old_char:
            self.msg("You are already OOC.")
            return

        account.db._last_puppet = old_char

        try:
            account.unpuppet_object(session)
            self.msg("\n|GYou go OOC.|n\n")
            logger.log_sec(f"{old_char} exits the game (Account: {account}).")

            if _AUTO_PUPPET_ON_LOGIN and _MAX_NR_CHARACTERS == 1 and self.playable:
                self.msg(
                    "You are out-of-character (OOC).\n"
                    "Use |wconnect|n to get back into the game."
                )
            else:
                self.msg(account.at_look(target=None, session=session))

        except RuntimeError as exc:
            self.msg(f"|rCould not unpuppet from |c{old_char}|n: {exc}")
            logger.log_sec(f"{old_char} fails to exit the game (Account: {account}).")


class CmdOOCLook(Command):
    """
    Command to implement the OOC look functionality.

    Usage:
        look

    This command allows players to look around when they are out-of-character (OOC).
    """

    key = "look"
    aliases = ["l", "ls"]
    locks = "cmd:is_ooc()"
    help_category = "Account"
    account_caller = True

    def parse(self):
        playable = self.account.characters
        # store playable property
        if self.args:
            self.playable = dict(
                (utils.to_str(char.key.lower()), char) for char in playable
            ).get(self.args.lower(), None)
        else:
            self.playable = playable

    def func(self):
        if self.session.puppet:
            self.msg("You currently have no ability to look around.")
            return

        if _AUTO_PUPPET_ON_LOGIN and _MAX_NR_CHARACTERS == 1 and self.playable:
            self.msg(
                "You are out-of-character (OOC).\nUse |wic|n to get back into the game."
            )
            return

        self.msg(self.account.at_look(account=self.playable, session=self.session))


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

            header = ("Name", "Value", "Saved") if saved_options else ("Name", "Value")
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
            self.msg(f"|wClient settings ({self.session.protocol_key}):|n\n{table}|n")

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
                raise RuntimeError(f"The encoding '|w{new_encoding}|n' is invalid. ")
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
                    self.msg(f"Option |w{new_name}|n was kept as '|w{old_val}|n'.")
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
                self.account.attributes.add("_saved_protocol_flags", saved_options)
                for key in optiondict:
                    self.msg(f"|gSaved option {key}.|n")
            if "clear" in self.switches:
                # clear this save
                for key in optiondict:
                    self.account.attributes.get("_saved_protocol_flags", {}).pop(
                        key, None
                    )
                    self.msg(f"|gCleared saved {key}.")
            self.session.update_flags(**optiondict)


class CmdPassword(Command):
    """
    Command to change the password of an account.

    Usage:
      password

    This command allows the player to change their account password. It prompts the player
    to enter their current password, then their new password. The new password is validated
    to ensure it meets the account's password requirements. If the password change is
    successful, the account's password is updated and saved.
    """

    key = "password"
    locks = "cmd:pperm(Player)"
    help_category = "Account"
    account_caller = True

    def func(self):
        account = self.account

        def get_input(prompt):
            return (yield prompt)

        def validate_password(password):
            if not password:
                self.msg("Password change aborted.")
                return False
            return True

        def change_password():
            oldpass = yield from get_input("Enter your password:")
            if not validate_password(oldpass):
                return

            if not account.check_password(oldpass):
                self.msg("The specified password is incorrect.")
                return

            newpass = yield from get_input("Enter your new password:")
            if not validate_password(newpass):
                return

            validated, error = account.validate_password(newpass)
            if not validated:
                errors = [e for suberror in error.messages for e in error.messages]
                self.msg("\n".join(errors))
                return

            account.set_password(newpass)
            account.save()
            self.msg("Password changed.")
            logger.log_sec(f"Password Changed: {account} (IP: {self.session.address}).")

        yield from change_password()


class CmdPlay(Command):
    """
    Command to play as a character.

    Usage:
      play <character>

    This command allows a player to switch to playing as a different character.
    The player can specify the character they want to play as, and if the character
    is valid and accessible to the player, they will be able to switch to that character.
    """

    key = "play"
    locks = "cmd:is_ooc()"
    aliases = ["connect", "ic", "puppet"]
    help_category = "Account"

    def get_character_candidates(self, account, args):
        """
        Get a list of character candidates based on the given arguments.

        Args:
            account (Account): The player's account.
            args (str): The arguments provided by the player.

        Returns:
            list: A list of character candidates.

        This method determines the character candidates based on the given arguments.
        If no arguments are provided, it checks if the player has a main character or
        a last puppet character. If arguments are provided, it searches for playable
        characters that match the arguments. If the player has builder permissions, it
        also searches for characters that can be puppeted by the player.
        """
        character_candidates = []

        if not args:
            if account.db._main_character:
                character_candidates.append(account.db._main_character)
            elif account.db._last_puppet:
                character_candidates.append(account.db._last_puppet)
        else:
            if account.db._playable_characters:
                character_candidates.extend(
                    utils.make_iter(
                        account.search(
                            args,
                            candidates=account.db._playable_characters,
                            search_object=True,
                            quiet=True,
                        )
                    )
                )

            if account.locks.check_lockstring(account, "perm(Builder)"):
                if self.session.puppet:
                    character_candidates = [
                        char
                        for char in self.session.puppet.search(args, quiet=True)
                        if char.access(account, "puppet")
                    ]
                else:
                    character_candidates.extend(
                        [
                            char
                            for char in search.object_search(args)
                            if char.access(account, "puppet")
                        ]
                    )

        return character_candidates

    def func(self):
        """
        Execute the play command.

        This method is called when the player executes the play command.
        It retrieves the player's account and session, checks the arguments,
        gets the character candidates, and performs the necessary actions
        to switch to the chosen character.
        """
        account = self.account
        session = self.session

        if (
            not self.args
            and not account.db._main_character
            and not account.db._last_puppet
        ):
            self.msg("Syntax: play <character>")
            return

        if account.db._main_character:
            character_candidates = self.get_character_candidates(
                account, account.db._main_character.key
            )
        elif account.db._last_puppet:
            character_candidates = self.get_character_candidates(
                account, account.db._last_puppet.key
            )
        else:
            character_candidates = self.get_character_candidates(account, self.args)
            if not character_candidates:
                self.msg("That is not a valid character choice.")
                return

        new_character = character_candidates[0]

        try:
            account.puppet_object(session, new_character)
            account.db._last_puppet = new_character
            logger.log_sec(f"{new_character} enters the game (Account: {account}).")
        except RuntimeError as exc:
            self.msg(f"|rYou cannot become |C{new_character.name}|n: {exc}")
            logger.log_sec(
                f"{new_character} fails to enter the game (Account: {account})."
            )


class CmdQuit(Command):
    """
    Command class for quitting the game.

    This command allows the player to quit the game. It provides options to quit
    the current session or all sessions associated with the player's account.

    Usage:
      quit [all]

    Switches:
      all - Quit all sessions

    Example usage:
      quit        - Quit the current session
      quit all    - Quit all sessions
    """

    key = "quit"
    switch_options = ("all",)
    locks = "cmd:all()"
    help_category = "Account"
    account_caller = True

    def func(self):
        """Hook function"""
        account = self.account
        session = self.session

        if "all" in self.switches:
            self.quit_all_sessions(account, session)
        else:
            self.quit_current_session(account, session)

    def quit_all_sessions(self, account, session):
        """Quit all sessions"""
        account.msg(
            "|RQuitting|n all sessions. Hope to see you soon again.", session=session
        )
        reason = "quit/all"
        for session in account.sessions.all():
            account.disconnect_session_from_account(session, reason)

    def quit_current_session(self, account, session):
        """Quit the current session"""
        nsess = account.sessions.count()
        reason = "quit"

        if nsess == 2:
            message = "|RQuitting|n. One session is still connected."
        elif nsess > 2:
            message = f"|RQuitting|n. {nsess - 1} sessions are still connected."
        else:
            message = "|RQuitting|n. Hope to see you again, soon."

        account.msg(message, session=session)
        account.disconnect_session_from_account(session, reason)


class CmdSessions(Command):
    """
    Command to display the current sessions of the account.

    Usage:
      sessions

    This command displays information about the current sessions of the account.
    It shows the session ID, protocol, host, puppet/character, and location for each session.
    """

    key = "sessions"
    locks = "cmd:all()"
    help_category = "Account"
    account_caller = True

    def func(self):
        """Implement function"""
        account = self.account
        sessions = sorted(account.sessions.all(), key=lambda x: x.sessid)

        table = self.styled_table(
            "|wsessid", "|wprotocol", "|whost", "|wpuppet/character", "|wlocation"
        )

        for sess in sessions:
            char = account.get_puppet(sess)
            host = sess.address[0] if isinstance(sess.address, tuple) else sess.address

            table.add_row(
                str(sess.sessid),
                str(sess.protocol_key),
                host,
                str(char) if char else "None",
                str(char.location) if char else "N/A",
            )

        self.msg(f"|wYour current session(s):|n\n{table}")


class CmdSetMain(Command):
    """
    Command to set the main character for an account.

    Usage: setmain [character name]

    Arguments:
        character name - The name of the character to set as the main character.
                         Use "none" to unset the main character.

    This command allows players to set their main character, which is the
    character they primarily play with. The main character can be used for
    various purposes within the game.

    If no character name is provided, the current main character is displayed.
    If the character name is set to "none", the main character is unset.

    Examples:
        setmain John - Sets the character named "John" as the main character.
        setmain none - Unsets the main character.
        main - Displays the current main character.
    """

    key = "setmain"
    aliases = ["main"]
    locks = "cmd:is_ooc()"
    help_category = "Account"
    account_caller = True

    def func(self):
        account = self.account
        playable_characters = account.db._playable_characters

        if not playable_characters:
            self.msg("You have no playable characters.")
            return

        if not self.args:
            main_character = account.db._main_character
            self.msg(f"Main Character: {main_character}.")
            return

        args = self.args.strip().lower()
        if args == "none":
            account.db._main_character = None
            self.msg("Main Character set to None.")
            logger.log_sec(f"Main Character Set: None (Account: {account}).")
            return

        character = account.search(
            self.args,
            candidates=playable_characters,
            search_object=True,
            quiet=True,
        )

        if not character:
            self.msg("No matching character found.")
            return

        if len(character) > 1:
            character_list = ", ".join(f"{obj.key}(#{obj.id})" for obj in character)
            self.msg(f"Multiple targets with the same name:\n {character_list}")
            return

        character = character[0]
        if character not in account.characters:
            self.msg("You have no such character.")
            return

        account.db._main_character = character
        self.msg(f"Main Character set to: {character}.")
        logger.log_sec(f"Main Character Set: {character} (Account: {account}).")


class CmdWho(Command):
    key = "who"
    aliases = ["wh"]
    locks = "cmd:all()"
    help_category = "Account"

    def create_header(self, width):
        header_string = f"{self.get_header(width)}\n"
        header_string += f"{self.get_time_display(width)}\n"
        header_string += f"{self.get_admin_display(width)}\n"
        header_string += f"{self.format_admin(['Jake'], width)}\n"
        header_string += f"{self.get_player_display(width)}"
        return header_string

    def get_header(self, width):
        return f" |145[ {settings.SERVERNAME} ]|n ".center(width + 6, "-")

    def get_time_display(self, width):
        current_time = datetime.now().strftime("%H:%M:%S %p, %A, %B %d, %Y")
        return current_time.center(width)

    def get_admin_display(self, width):
        return " |r[ Administrators ]|n ".center(width + 4, "-")

    def format_admin(self, names, width):
        total_names_length = sum(len(name) for name in names)
        num_gaps = len(names) + 1
        remaining_space = width - total_names_length
        if remaining_space <= 0:
            return " ".join(names)[:width]
        gap, extra_space = divmod(remaining_space, num_gaps)
        formatted_string = " " * gap
        for name in names:
            formatted_string += name + " " * (gap + (1 if extra_space > 0 else 0))
            extra_space -= 1
        return formatted_string

    def get_player_display(self, width):
        return " [ Players ] ".center(width, "-")

    def get_footer(self, width):
        return "-" * width

    def add_row_to_table(self, table, session, caller):
        delta_cmd = time.time() - session.cmd_last_visible
        delta_conn = time.time() - session.conn_time
        session_account = session.get_account()
        puppet = session.get_puppet()
        location = puppet.location.key if puppet and puppet.location else "None"
        table.add_row(
            utils.crop(session_account.get_display_name(caller), width=25),
            utils.crop(location, width=25),
            utils.time_format(delta_conn, 0),
            utils.time_format(delta_cmd, 1),
            (
                session.address[0]
                if isinstance(session.address, tuple)
                else session.address
            ),
        )

    def get_admin_and_table(self, session_list, caller, width):
        admin = []
        table = self.styled_table(
            "|wPlayer",
            "|wRoom",
            "|wOn for",
            "|wIdle",
            "|wHost",
            header=True,
            border="header",
            pad_left=2,
            width=width,
            evenwidth=False,
        )
        for session in session_list:
            if session.get_account().permissions.check("Admin"):
                admin.append(session.get_account().get_display_name(caller))
            elif session.logged_in:
                self.add_row_to_table(table, session, caller)
        return admin, table

    def func(self):
        caller = self.caller
        session_list = sorted(SESSIONS.get_sessions(), key=lambda x: x.account.key)
        width = 49 + 5 * ((self.client_width() - 49) // 5)
        if caller.permissions.check("Admin"):
            admin, table = self.get_admin_and_table(session_list, caller, width)
        else:
            table = self.styled_table(header=False, border=None, pad_left=2)
            admin = []
            for session in session_list:
                if session.get_account().permissions.check("Admin"):
                    admin.append(
                        strip_ansi(session.get_account().get_display_name(caller))
                    )
                elif session.logged_in:
                    table.add_row(session.get_account().get_display_name(caller))
        naccounts = SESSIONS.account_count()
        is_one = naccounts == 1
        header = self.create_header(width)
        footer = self.get_footer(width)
        string = f"{header}\n{table}\n{footer}\n"
        string += f"{naccounts} player{'s' if not is_one else ''} logged in.".rjust(
            width
        )
        caller.msg(string)
