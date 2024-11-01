"""
Command module containing CmdSetMain.
"""

from evennia import Command
from evennia.utils import logger


class CmdSetMain(Command):
    """
    Set your main character

    Usage:
      setmain <character>

    This will set the character you stay connected to by default when you log in. Use 'setmain none'
    to unset your main character. Note that setting a main character will also set your account name
    to match the character's name.
    """

    key = "setmain"
    aliases = ["main"]
    locks = "cmd:is_ooc()"
    help_category = "Account"
    account_caller = True

    def func(self):
        """
        Set the main character
        """
        account = self.account
        args = self.args.strip()
        playable_characters = account.db._playable_characters

        if not playable_characters:
            self.msg("You have no playable characters.")
            return

        if not args:
            main_character = account.db._main_character
            if main_character:
                self.msg(f"Your main character is: {main_character}.")
            else:
                self.msg("You have no main character set.")
            return

        if args.lower() == "none":
            account.db._main_character = None
            self.msg("Your main character has been unset.")
            logger.log_sec(f"Main character unset by {account}.")
            return

        char = account.search(
            args,
            candidates=playable_characters,
            search_object=True,
            quiet=True,
        )

        if not char:
            self.msg("That is not a valid character.")
            return

        if len(char) > 1:
            char_list = ", ".join(f"{obj.key}(#{obj.id})" for obj in char)
            self.msg(f"Multiple characters with the same name:\n {char_list}")
            return

        char = char[0]
        account.db._main_character = char
        account.db.username = char.db.name
        self.msg(f"Your main character has been set to: {char}.")
        logger.log_sec(f"Main character set to {char} by {account}.")
