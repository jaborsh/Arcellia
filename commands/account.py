import time
from datetime import datetime

from django.conf import settings
from evennia.commands.default.account import MuxAccountLookCommand
from evennia.objects.models import ObjectDB
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import create, logger, utils
from evennia.utils.ansi import strip_ansi
from evennia.utils.evmenu import get_input
from utils.formatting import wrap

from commands.command import Command

_MAX_NR_CHARACTERS = settings.MAX_NR_CHARACTERS
_AUTO_PUPPET_ON_LOGIN = settings.AUTO_PUPPET_ON_LOGIN


class CmdCreate(Command):
    """
    Usage: create <name>

    Create a new character. Names will automatically capitalize. Follow the
    provided rules when creating a new character.
    """

    key = "create"
    locks = "cmd:pperm(Player)"
    help_category = "General"
    account_caller = True

    def func(self):
        account = self.account
        session = self.session
        if not self.args:
            self.msg("Usage: create <name>")
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
                    f"You may only have a maximum of {_MAX_NR_CHARACTERS} character{plural}."
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
                f"(Caller: {account}, IP: {session.address})."
            )

            # start puppeting the character
            try:
                account.puppet_object(session, new_character)
                account.db._last_puppet = new_character
                logger.log_sec(
                    f"Puppet Success: (Caller: {account}, Target: {new_character}, IP:"
                    f" {session.address})."
                )
            except RuntimeError as error:
                self.msg(f"|rYou cannot become |C{new_character.name}|n: {error}")
                logger.log_sec(
                    f"Puppet Failed: %s (Caller: {account}, Target: {new_character}, IP:"
                    f" {session.address})."
                )

        prompt = f"Did you enter '|w{key}|n' correctly and does this name comply with the rules? |r[Y/n]|n"
        get_input(account, prompt, _callback)


class CmdDelete(Command):
    """
    Usage: delete <name>

    Permanently delete one of your characters. This cannot be undone!
    """

    key = "delete"
    locks = "cmd:pperm(Player)"
    help_category = "General"
    account_caller = True

    def func(self):
        account = self.account
        session = self.session

        if not self.args:
            self.msg("Usage: delete <name>")
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
                "Aborting - there are two characters with the same name. Ask an admin to delete the right one."
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
                f"Character Deleted: {key} (Caller: {account}, IP: {session.address})."
            )
            del caller.ndb._char_to_delete

        match = match[0]
        account.ndb._char_to_delete = match

        # Return if caller has no permission to delete this
        if not match.access(account, "delete"):
            self.msg("You do not have permission to delete this character.")
            return

        prompt = f"|rThis will permanently delete |n'|w{match.key}|n'|r. This cannot be undone!|n Continue? |r[Y/n]|n"
        get_input(account, prompt, _callback)


# note that this is inheriting from MuxAccountLookCommand,
# and has the .playable property.
class CmdOOCLook(MuxAccountLookCommand):
    """
    Usage: look

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


class CmdWho(Command):
    """
    Usage: who

    This command lists all players.
    """

    key = "who"
    locks = "cmd:all()"
    help_category = "General"

    def create_header(self, width):
        header_string = f"{self.get_header(width)}\n"
        header_string += f"{self.get_time_display(width)}\n"
        header_string += f"{self.get_admin_display(width)}\n"
        header_string += (
            f"{self.format_admin('Jake - Developer', 'Jeanie - Writer', width)}\n"
        )
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

    def format_admin(self, name1, name2, width):
        total_names_length = len(name1) + len(name2)

        # Calculate the remaining space after placing the names
        remaining_space = width - total_names_length

        # Calculate the spaces for left, middle and right
        left_right_space = remaining_space // 3
        middle_space = remaining_space - (2 * left_right_space)

        formatted_string = " " * left_right_space + name1 + " " * middle_space + name2

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
