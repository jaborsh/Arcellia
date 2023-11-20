import time
from datetime import datetime

from django.conf import settings
from evennia.commands.default import account
from evennia.objects.models import ObjectDB
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import create, search, utils
from evennia.utils.ansi import strip_ansi
from evennia.utils.evmenu import get_input
from parsing.text import wrap
from server.conf import logger

from commands.command import Command

_MAX_NR_CHARACTERS = settings.MAX_NR_CHARACTERS
_AUTO_PUPPET_ON_LOGIN = settings.AUTO_PUPPET_ON_LOGIN

# limit symbol import for  API
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
    Syntax: create <name>

    Create a new character. Names will automatically capitalize. Follow the
    provided rules when creating a new character.
    """

    key = "create"
    locks = "cmd:is_ooc() and pperm(Player)"
    help_category = "General"
    account_caller = True

    def func(self):
        account = self.account
        session = self.session
        if not self.args:
            self.msg("Syntax: create <name>")
            return

        if _MAX_NR_CHARACTERS is not None:
            if (
                not account.is_superuser
                and not account.check_permstring("Developer")
                and account.db._playable_characters
                and len(account.db._playable_characters) >= _MAX_NR_CHARACTERS
            ):
                plural = "" if _MAX_NR_CHARACTERS == 1 else "s"
                self.msg(
                    f"You may only have a maximum of {_MAX_NR_CHARACTERS} character{plural}."  # noqa: E501
                )
                return
        if not self.args.isalpha():
            self.msg("|rYour character's name may only contain letters.|n")
            return

        key = self.args.replace(" ", "").capitalize()[:16]
        typeclass = settings.BASE_CHARACTER_TYPECLASS

        # check if the character already exists
        if ObjectDB.objects.filter(db_typeclass_path=typeclass, db_key__iexact=key):
            self.msg(f"|rA character named '|w{key}|r' already exists.|n")
            return

        # check if the name is valid
        rules_string = "The following rules apply to names:\n\n"
        rules_string += (
            wrap(
                "|gNames should be distinct from iconic media characters.",
                pre_text="1. ",
            )
            + "\n"
        )
        rules_string += (
            wrap(
                "|gNames should suit the game's theme and setting.",
                pre_text="2. ",
            )
            + "\n"
        )
        rules_string += (
            wrap(
                "|gNames should be understandable and pronounceable.",
                pre_text="3. ",
            )
            + "\n"
        )
        self.msg(rules_string)

        def _callback(caller, callback_prompt, result):
            if result.lower() not in ["yes", "y"]:
                self.msg("Creation aborted.")
                return

            # create the character
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
                "puppet:id(%i) or pid(%i) or perm(Developer) or pperm(Developer);"
                "delete:id(%i) or perm(Admin)"
                % (new_character.id, account.id, account.id)
            )
            account.db._playable_characters.append(new_character)
            new_character.db.desc = "This is a character."
            logger.log_sec(
                f"Character Created: {new_character} "
                f"(Account: {account}, IP: {session.address})."
            )

            # start puppeting the character
            try:
                account.puppet_object(session, new_character)
                account.db._last_puppet = new_character
                logger.log_sec(
                    f"{new_character} enters the game (Account: {account})."
                    # f"IP: {self.session.address})."
                )
            except RuntimeError as error:
                self.msg(f"|rYou cannot become |C{new_character.name}|n: {error}")
                logger.log_sec(
                    f"{new_character} fails to enter the game (Account: {account})."
                    # f"IP: {self.session.address})."
                )

        prompt = f"Did you enter '|w{key}|n' correctly and does this name comply with the rules? |r[Y/n]|n"  # noqa: E501
        get_input(account, prompt, _callback)


class CmdDelete(Command):
    """
    Syntax: delete <name>

    Permanently delete one of your characters. This cannot be undone!
    """

    key = "delete"
    locks = "cmd:is_ooc() and pperm(Player)"
    help_category = "General"
    account_caller = True

    def func(self):
        account = self.account

        if not self.args:
            self.msg("Syntax: delete <name>")
            return

        match = [
            char
            for char in utils.make_iter(account.db._playable_characters)
            if char.key.lower() == self.args.lower()
        ]
        if not match:
            self.msg("You have no such character to delete.")
            return
        elif len(match) > 1:
            self.msg(
                "Aborting - there are two characters with the same name. Ask an admin to delete the right one."  # noqa: E501
            )
            return

        def _callback(caller, callback_prompt, result):
            if result.lower() not in ["yes", "y"]:
                self.msg("Deletion aborted.")
                return

            delobj = caller.ndb._char_to_delete
            key = delobj.key
            caller.db._playable_characters = [
                pc for pc in caller.db._playable_characters if pc != delobj
            ]
            delobj.delete()
            self.msg(f"Character '|w{key}|n' permanently deleted.")
            logger.log_sec(
                f"Character Deleted: {key} (Account: {account})."  # , IP: {session.address})."  # noqa: E501
            )
            del caller.ndb._char_to_delete

        match = match[0]
        account.ndb._char_to_delete = match

        # Return if caller has no permission to delete this
        if not match.access(account, "delete"):
            self.msg("You do not have permission to delete this character.")
            return

        prompt = f"|rThis will permanently delete |n'|w{match.key}|n'|r. This cannot be undone!|n Continue? |r[Y/n]|n"  # noqa: E501
        get_input(account, prompt, _callback)


# move this to characters eventually
class CmdDisconnect(account.CmdOOC):
    """
    Syntax: disconnect

    Go out-of-character (OOC)
    """

    key = "disconnect"
    aliases = ["disc", "unpuppet"]

    def func(self):
        """Implement function"""

        account = self.account
        session = self.session
        self.args = None

        old_char = account.get_puppet(session)
        if not old_char:
            string = "You are already OOC."
            self.msg(string)
            return

        account.db._last_puppet = old_char

        # disconnect
        try:
            account.unpuppet_object(session)
            self.msg("\n|GYou go OOC.|n\n")

            logger.log_sec(
                f"{old_char} exits the game (Account: {account})."
                # f"IP: {session.address})."
            )

            if _AUTO_PUPPET_ON_LOGIN and _MAX_NR_CHARACTERS == 1 and self.playable:
                # only one character exists and is allowed - simplify
                self.msg(
                    "You are out-of-character (OOC).\n"
                    "Use |wconnect|n to get back into the game."
                )
                return

            self.msg(account.at_look(target=None, session=session))

        except RuntimeError as exc:
            self.msg(f"|rCould not unpuppet from |c{old_char}|n: {exc}")
            logger.log_sec(
                f"{old_char} fails to exit the game (Account: {account})."
                # f"IP: {session.address})."
            )


# note that this is inheriting from MuxAccountLookCommand,
# and has the .playable property.
class CmdOOCLook(account.MuxAccountLookCommand):
    """
    Syntax: look

    This is an OOC version of the look command. Since an account doesn't have
    an in-game existence, there is no concept of location or "self". If we are
    controlling a character, the IC version of look takes over.
    """

    key = "look"
    aliases = ["l", "ls"]
    locks = "cmd:all()"
    help_category = "General"

    # this is used by the parent
    account_caller = True

    def func(self):
        """implement the ooc look command"""

        if self.session.puppet:
            # if we are puppeting, this is only reached in the case the that puppet
            # has no look command on its own.
            self.msg("You currently have no ability to look around.")
            return

        if _AUTO_PUPPET_ON_LOGIN and _MAX_NR_CHARACTERS == 1 and self.playable:
            # only one exists and is allowed - simplify
            self.msg(
                "You are out-of-character (OOC).\nUse |wic|n to get back into the game."
            )
            return

        # call on-account look helper method
        self.msg(
            self.account.at_look(account=self.playable, session=self.session),
        )


class CmdOptions(account.CmdOption):
    """
    Syntax: options[/switch] [name = value]

    Switches:
      save - Save the current option setting for future logins.
      clear - Clear the saved options.

    This command allows viewing and setting client interface settinggs. Note
    that saved options may not be able to be used if later connecting with
    a client with different capabilities.
    """

    key = "options"
    aliases = ["option"]


class CmdPassword(Command):
    """
    Syntax: password

    Change your password. Make sure to pick a safe one!
    """

    key = "password"
    locks = "cmd:pperm(Player)"
    account_caller = True

    def func(self):
        account = self.account
        oldpass = yield ("Enter your password:")

        if not oldpass:
            self.msg("Password change aborted.")
            return
        if not account.check_password(oldpass):
            self.msg("The specified password is incorrect.")
            return

        newpass = yield ("Enter your new password:")
        if not newpass:
            self.msg("Password change aborted.")
            return
        validated, error = account.validate_password(newpass)
        if not validated:
            errors = [e for suberror in error.messages for e in error.messages]
            string = "\n".join(errors)
            self.msg(string)
            return

        account.set_password(newpass)
        account.save()
        self.msg("Password changed.")
        logger.log_sec(
            f"Password Changed: {account} (Caller: {account}, IP: {self.session.address})."  # noqa: E501
        )


class CmdPlay(Command):
    """
    Syntax: play <character>

    Play (IC) as a given character.
    """

    key = "play"
    locks = "cmd:is_ooc()"
    aliases = ["connect", "ic", "puppet"]
    help_category = "General"

    def func(self):
        """
        Main puppet method
        """
        account = self.account
        session = self.session

        new_character = None
        character_candidates = []

        if not self.args:
            if account.db._main_character:
                # if a main character is set, use that
                character_candidates.append(account.db._main_character)
            else:
                character_candidates = (
                    [account.db._last_puppet] if account.db._last_puppet else []
                )
            if not character_candidates:
                self.msg("Syntax: ic <character>")
                return
        else:
            # argument given

            if account.db._playable_characters:
                # look at the playable_characters list first
                character_candidates.extend(
                    utils.make_iter(
                        account.search(
                            self.args,
                            candidates=account.db._playable_characters,
                            search_object=True,
                            quiet=True,
                        )
                    )
                )

            if account.locks.check_lockstring(account, "perm(Builder)"):
                # builders and higher should be able to puppet more than their
                # playable characters.
                if session.puppet:
                    # start by local search - this helps to avoid the user
                    # getting locked into their playable characters should one
                    # happen to be named the same as another. We replace the suggestion
                    # from playable_characters here - this allows builders to puppet objects  # noqa: E501
                    # with the same name as their playable chars should it be necessary
                    # (by going to the same location).
                    character_candidates = [
                        char
                        for char in session.puppet.search(self.args, quiet=True)
                        if char.access(account, "puppet")
                    ]
                if not character_candidates:
                    # fall back to global search only if Builder+ has no
                    # playable_characters in list and is not standing in a room
                    # with a matching char.
                    character_candidates.extend(
                        [
                            char
                            for char in search.object_search(self.args)
                            if char.access(account, "puppet")
                        ]
                    )

        # handle possible candidates
        if not character_candidates:
            self.msg("That is not a valid character choice.")
            return
        if len(character_candidates) > 1:
            self.msg(
                "Multiple targets with the same name:\n %s"
                % ", ".join(
                    "%s(#%s)" % (obj.key, obj.id) for obj in character_candidates
                )
            )
            return
        else:
            new_character = character_candidates[0]

        # do the puppet puppet
        try:
            account.puppet_object(session, new_character)
            account.db._last_puppet = new_character
            logger.log_sec(
                f"{new_character} enters the game (Account: {account})."
                # f"IP: {self.session.address})."
            )
        except RuntimeError as exc:
            self.msg(f"|rYou cannot become |C{new_character.name}|n: {exc}")
            logger.log_sec(
                f"{new_character} fails to enter the game (Account: {account})."
                # f"IP: {self.session.address})."
            )


class CmdQuit(account.CmdQuit):
    """
    Syntax: quit

    Switch:
      all - disconnect all connected sessions

    Disconnect your current session from the game. Use /all to disconnect all
    sessions.
    """


class CmdSessions(account.CmdSessions):
    """
    Syntax: sessions

    Lists the sessions currently connected to your account.
    """


class CmdSetMain(Command):
    """
    Syntax: setmain [character]

    This command is responsible for setting your main character which will
    establish them as the character that you automatically log into upon
    connection.
    """

    key = "setmain"
    aliases = ["main"]
    locks = "cmd:is_ooc()"
    help_category = "General"
    account_caller = True

    def func(self):
        account = self.account

        if not account.db._playable_characters:
            self.msg("You have no playable characters.")
            return

        if not self.args:
            self.msg(f"Main Character: {account.db._main_character}.")
            return

        if self.args.strip().lower() == "none":
            account.db._main_character = None
            self.msg("Main Character set to None.")
            logger.log_sec(f"Main Character Set: None (Account: {account}).")
            return

        character = utils.make_iter(
            account.search(
                self.args,
                candidates=account.db._playable_characters,
                search_object=True,
                quiet=True,
            )
        )

        if len(character) > 1:
            self.msg(
                "Multiple targets with the same name:\n %s"
                % ", ".join("%s(#%s)" % (obj.key, obj.id) for obj in character)
            )
            return

        character = character[0]
        if character not in account.characters:
            self.msg("You have no such character.")
            return

        account.db._main_character = character
        self.msg(f"Main Character set to: {character}.")
        logger.log_sec(f"Main Character Set: {character} (Account: {account}).")


class CmdWho(Command):
    """
    Syntax: who

    This command lists all players.
    """

    key = "who"
    aliases = ["wh"]
    locks = "cmd:all()"
    help_category = "General"

    def create_header(self, width):
        header_string = f"{self.get_header(width)}\n"
        header_string += f"{self.get_time_display(width)}\n"
        header_string += f"{self.get_admin_display(width)}\n"
        header_string += f"{self.format_admin(['Jake'], width)}\n"
        header_string += f"{self.get_player_display(width)}"

        return header_string

    def get_header(self, width):
        return utils.pad(
            " |145[ {} ]|n ".format(settings.SERVERNAME),
            width=width + 6,
            align="c",
            fillchar="-",
        )

    def get_time_display(self, width):
        current_time = datetime.now().strftime("%H:%M:%S %p, %A, %B %d, %Y")
        return utils.pad(current_time, width=width, align="c", fillchar=" ")

    def get_admin_display(self, width):
        return utils.pad(
            " |r[ Administrators ]|n ", width=width + 4, align="c", fillchar="-"
        )

    def format_admin(self, names, width):
        # Calculate the total length of the names
        total_names_length = sum(len(name) for name in names)

        # Calculate the number of gaps between the names, and add 2 for the margins
        num_gaps = len(names) - 1 + 2

        # Calculate the total available space
        remaining_space = width - total_names_length

        if remaining_space <= 0:
            return " ".join(names)[:width]  # Truncate if it doesn't fit

        # Calculate the gap size, which will also be the margin size
        gap = remaining_space // num_gaps

        # Calculate any extra spaces that can't be evenly distributed
        extra_space = remaining_space % num_gaps

        # Create the formatted string with the left margin
        formatted_string = " " * gap + names[0]
        for name in names[1:]:
            this_gap = gap + (1 if extra_space > 0 else 0)
            formatted_string += " " * this_gap + name
            extra_space -= 1

        # Add the right margin
        formatted_string += " " * gap

        return formatted_string

    def get_player_display(self, width):
        return utils.pad(" [ Players ] ", width=width, align="c", fillchar="-")

    def get_footer(self, width):
        return utils.pad("", width=width, align="c", fillchar="-")

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
            # session.protocol_key,
            isinstance(session.address, tuple)
            and session.address[0]
            or session.address,
        )

    def get_admin_and_table(self, session_list, caller, width):
        admin = []
        table = self.styled_table(
            "|wPlayer",
            "|wRoom",
            "|wOn for",
            "|wIdle",
            # "|wProtocol",
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
                continue

            if not session.logged_in:
                continue

            self.add_row_to_table(table, session, caller)

        return admin, table

    def func(self):
        """
        Get all connected accounts by polling sessions.
        """
        caller = self.caller
        session_list = SESSIONS.get_sessions()
        session_list = sorted(session_list, key=lambda x: x.account.key)
        width = 49 + 5 * ((self.client_width() - 49) // 5)

        if caller.permissions.check("Admin"):
            # privileged info
            admin, table = self.get_admin_and_table(session_list, caller, width)
        else:
            # width = 50 if self.client_width() >= 44 else self.client_width()
            # Unprivileged table
            # table = EvTable(header=False, border=None)
            table = self.styled_table(header=False, border=None, pad_left=2)

            # Add players to list.
            admin = []
            for session in session_list:
                # Separate admin from players
                if session.get_account().permissions.check("Admin"):
                    admin.append(
                        strip_ansi(session.get_account().get_display_name(caller))
                    )
                    continue

                # Skip sessions that are not logged in.
                if not session.logged_in:
                    continue

                # Add player to table.
                session_account = session.get_account()
                table.add_row(session_account.get_display_name(caller))

        naccounts = SESSIONS.account_count()
        is_one = naccounts == 1
        header = self.create_header(width)
        footer = self.get_footer(width)
        string = f"{header}\n{table}\n{footer}\n"
        string += f"{naccounts} player{'s' if not is_one else ''} logged in.".rjust(
            width
        )

        caller.msg(string)
