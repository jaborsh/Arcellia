"""
Command module containing CmdCreate.
"""

from django.conf import settings
from evennia.objects.models import ObjectDB
from evennia.utils import create
from evennia.utils.evmenu import get_input

from commands.command import Command
from menus.amenu import AMenu
from server.conf import logger

_MAX_NR_CHARACTERS = settings.MAX_NR_CHARACTERS


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
                logger.log_sec(
                    f"{new_character} enters the game (Account: {account})."
                )
            except RuntimeError as error:
                self.msg(
                    f"|rYou cannot become |C{new_character.name}|n: {error}"
                )
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
