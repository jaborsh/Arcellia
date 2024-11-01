"""
Command module containing CmdSetMain.
"""

from commands.command import Command
from server.conf import logger


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
            character_list = ", ".join(
                f"{obj.key}(#{obj.id})" for obj in character
            )
            self.msg(f"Multiple targets with the same name:\n {character_list}")
            return

        character = character[0]
        if character not in account.characters:
            self.msg("You have no such character.")
            return

        account.db._main_character = character
        self.msg(f"Main Character set to: {character}.")
        logger.log_sec(f"Main Character Set: {character} (Account: {account}).")
