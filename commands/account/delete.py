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

    def _find_character(self, name):
        """Find a character matching the given name."""
        playable_characters = getattr(
            self.account.db, "_playable_characters", []
        )
        if not playable_characters:
            return None, "You have no playable characters to delete."

        matches = [
            char
            for char in playable_characters
            if char.key.lower() == name.lower()
        ]

        if not matches:
            return None, "You have no such character to delete."
        if len(matches) > 1:
            return (
                None,
                "Aborting - there are multiple characters with the same name. Please contact an admin to delete the correct one.",
            )

        char = matches[0]
        if not char.access(self.account, "delete"):
            return None, "You do not have permission to delete this character."

        return char, None

    def _delete_character(self, character):
        """Delete the given character."""

        def _callback(account, prompt, result):
            if result.lower() not in {"yes", "y"}:
                self.msg("Deletion aborted.")
                return

            key = character.key
            try:
                playable_characters = getattr(
                    account.db, "_playable_characters", []
                )
                account.db._playable_characters = [
                    pc for pc in playable_characters if pc != character
                ]
                character.delete()
                self.msg(f"'|w{key}|n' has been permanently deleted.")
                logger.log_sec(
                    f"Character Deleted: {key} (Account: {account})."
                )
            except Exception as e:
                logger.log_err(f"Error deleting character '{key}': {e}")
                self.msg(
                    "An error occurred while attempting to delete the character."
                )

        prompt = f"|rPermanently delete '|w{character.key}|r'? This action cannot be undone! |w[Y/n]|n"
        get_input(self.account, prompt, _callback)

    def func(self):
        if not self.args:
            self.msg("Syntax: delete <name>")
            return

        character, error = self._find_character(self.args.strip())
        if error:
            self.msg(error)
            return

        self._delete_character(character)
