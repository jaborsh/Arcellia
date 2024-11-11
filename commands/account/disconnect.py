"""
Command module containing CmdDisconnect.
"""

from django.conf import settings

from commands.command import Command
from server.conf import logger


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

    # Class-level configuration
    AUTO_PUPPET_ON_LOGIN = getattr(settings, "AUTO_PUPPET_ON_LOGIN", False)
    MAX_NR_CHARACTERS = getattr(settings, "MAX_NR_CHARACTERS", 1)

    def func(self):
        """Execute the disconnect command."""
        if not self._validate_character():
            return

        self._store_last_puppet()
        if self._attempt_unpuppet():
            self._show_disconnect_message()

    def _validate_character(self):
        """Check if the account has a character to disconnect from."""
        if not self.account.get_puppet(self.session):
            self.msg("You are already OOC.")
            return False
        return True

    def _store_last_puppet(self):
        """Store the current character as the last puppet."""
        self.old_char = self.account.get_puppet(self.session)
        self.account.db._last_puppet = self.old_char

    def _attempt_unpuppet(self):
        """Attempt to unpuppet the current character."""
        try:
            self.account.unpuppet_object(self.session)
            logger.log_sec(
                f"{self.old_char} exits the game (Account: {self.account})."
            )
            return True
        except RuntimeError as exc:
            self._handle_error(exc, "Could not unpuppet from")
        except Exception as exc:
            self._handle_error(exc, "An unexpected error occurred:")
        return False

    def _handle_error(self, exc, prefix):
        """Handle and log errors during unpuppeting."""
        self.msg(f"|r{prefix} |c{self.old_char}|n: {exc}")
        logger.log_err(
            f"{self.old_char} failed to exit the game (Account: {self.account}). Error: {exc}"
        )

    def _show_disconnect_message(self):
        """Display appropriate disconnect messages to the user."""
        self.msg("\n|GYou go OOC.|n\n")

        if (
            self.AUTO_PUPPET_ON_LOGIN
            and self.MAX_NR_CHARACTERS == 1
            and getattr(self, "playable", False)
        ):
            self.msg(
                "You are out-of-character (OOC).\n"
                "Use |wconnect|n to get back into the game."
            )
        else:
            room_description = self.account.at_look(
                target=None, session=self.session
            )
            self.msg(room_description)
