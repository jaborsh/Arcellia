"""
Command module containing CmdDelete.
"""

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

    def func(self) -> None:
        account = self.account

        if not self.args:
            self.msg("Syntax: delete <name>")
            return

        # Safely access playable characters, defaulting to an empty list if not set
        playable_characters = getattr(account.db, "_playable_characters", [])
        if not playable_characters:
            self.msg("You have no playable characters to delete.")
            return

        char_name = self.args.strip().lower()
        # Find matching characters with case-insensitive comparison
        match = [
            char
            for char in playable_characters
            if char.key.lower() == char_name
        ]

        if not match:
            self.msg("You have no such character to delete.")
            return

        if len(match) > 1:
            self.msg(
                "Aborting - there are multiple characters with the same name. "
                "Please contact an admin to delete the correct one."
            )
            return

        char_to_delete = match[0]

        # Check if the account has permission to delete the character
        if not char_to_delete.access(account, "delete"):
            self.msg("You do not have permission to delete this character.")
            return

        def _delete_character(account, prompt, result):
            # Confirm deletion based on user input
            if result.lower() not in {"yes", "y"}:
                self.msg("Deletion aborted.")
                return

            key = char_to_delete.key
            try:
                # Remove the character from playable characters
                account.db._playable_characters = [
                    pc for pc in playable_characters if pc != char_to_delete
                ]
                # Delete the character object
                char_to_delete.delete()
                self.msg(f"Character '|w{key}|n' has been permanently deleted.")
                # Log the deletion for auditing purposes
                logger.log_sec(
                    f"Character Deleted: {key} (Account: {account})."
                )
            except Exception as e:
                # Log any unexpected errors during deletion
                logger.log_err(f"Error deleting character '{key}': {e}")
                self.msg(
                    "An error occurred while attempting to delete the character."
                )

        prompt = (
            f"|rThis will permanently delete '|w{char_to_delete.key}|r'. "
            f"This action cannot be undone!|n Continue? |r[Y/n]|n"
        )
        get_input(account, prompt, _delete_character)
