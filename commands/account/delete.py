"""
Command module containing CmdDelete.
"""

from evennia.utils import utils
from evennia.utils.evmenu import get_input

from commands.command import Command
from server.conf import logger


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
                pc
                for pc in account.db._playable_characters
                if pc != char_to_delete
            ]
            char_to_delete.delete()
            self.msg(f"Character '|w{key}|n' permanently deleted.")
            logger.log_sec(f"Character Deleted: {key} (Account: {account}).")

        prompt = f"|rThis will permanently delete |n'|w{char_to_delete.key}|n'|r. This cannot be undone!|n Continue? |r[Y/n]|n"
        get_input(account, prompt, _delete_character)
