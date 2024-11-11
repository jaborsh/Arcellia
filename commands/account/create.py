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

    # 1. Primary Command Method
    def func(self):
        """Execute the command to create a new character."""
        if not self.args:
            self.msg("Syntax: create <name>")
            return

        key = self.args.strip().capitalize()[:16]
        validation_result = self._validate_character(key)

        if not validation_result:
            return

        self._display_name_rules()
        prompt = f"\nDid you enter '|w{key}|n' correctly and does this name comply with the rules? |r[Y/n]|n"
        get_input(self.account, prompt, self._handle_creation(key))

    # 2. Validation Methods
    def _validate_character(self, key):
        """Validate character creation requirements."""
        if not key.isalpha():
            self.msg("|rYour character's name may only contain letters.|n")
            return False

        if self._is_at_character_limit():
            return False

        if ObjectDB.objects.filter(
            db_typeclass_path=settings.BASE_CHARACTER_TYPECLASS,
            db_key__iexact=key,
        ).exists():
            self.msg(f"|rA character named '|w{key}|r' already exists.|n")
            return False

        return True

    def _is_at_character_limit(self):
        """Check if account has reached character limit."""
        if (
            _MAX_NR_CHARACTERS is not None
            and not self.account.is_superuser
            and not self.account.check_permstring("Developer")
            and len(self.account.db._playable_characters) >= _MAX_NR_CHARACTERS
        ):
            plural = "" if _MAX_NR_CHARACTERS == 1 else "s"
            self.msg(
                f"You may only have a maximum of {_MAX_NR_CHARACTERS} character{plural}."
            )
            return True
        return False

    def _display_name_rules(self):
        """Display the rules for character names."""
        rules_string = (
            "The following rules apply to names:\n\n"
            "1. |gNames should be distinct from iconic media characters.|n\n"
            "2. |gNames should suit the game's theme and setting.|n\n"
            "3. |gNames should be understandable and pronounceable.|n"
        )
        self.msg(rules_string)

    # 3. Creation Process Methods
    def _handle_creation(self, key):
        """Handle character creation callback."""

        def inner(caller, callback_prompt, result):
            if result.lower() not in ["yes", "y"]:
                self.msg("Creation aborted.")
                return

            new_character = self._create_character_obj(key)
            if not new_character:
                return

            self._enter_game(new_character)

        return inner

    def _create_character_obj(self, key):
        """Create the character object with basic settings."""
        start_location = ObjectDB.objects.get_id(settings.START_LOCATION)
        default_home = ObjectDB.objects.get_id(settings.DEFAULT_HOME)

        new_character = create.create_object(
            settings.BASE_CHARACTER_TYPECLASS,
            key=key,
            location=start_location,
            home=default_home,
            permissions=settings.PERMISSION_ACCOUNT_DEFAULT,
        )

        new_character.locks.add(
            f"puppet:id({new_character.id}) or pid({self.account.id}) or perm(Developer) or pperm(Developer);"
            f"delete:id({self.account.id}) or perm(Admin)"
        )
        new_character.db.desc = "This is a character."
        self.account.db._playable_characters.append(new_character)

        logger.log_sec(
            f"Character Created: {new_character} (Account: {self.account}, IP: {self.session.address})."
        )
        return new_character

    def _enter_game(self, new_character):
        """Handle character game entry and menu setup."""
        try:
            self.account.puppet_object(self.session, new_character)
            self.account.db._last_puppet = new_character
            logger.log_sec(
                f"{new_character} enters the game (Account: {self.account})."
            )

            AMenu(
                new_character,
                "world.chargen.menu",
                startnode="chargen_welcome",
                auto_look=True,
                auto_help=True,
                cmd_on_exit=None,
                persistent=True,
            )
        except RuntimeError as error:
            self.msg(f"|rYou cannot become |C{new_character.name}|n: {error}")
            logger.log_sec(
                f"{new_character} fails to enter the game (Account: {self.account})."
            )
