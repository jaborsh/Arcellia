"""
Command module containing CmdDisconnect.
"""

from django.conf import settings

from commands.command import Command
from server.conf import logger

_AUTO_PUPPET_ON_LOGIN = getattr(settings, "AUTO_PUPPET_ON_LOGIN", False)
_MAX_NR_CHARACTERS = getattr(settings, "MAX_NR_CHARACTERS", 1)


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

    def func(self) -> None:
        """Disconnect the player's character from the game, making them OOC."""
        account = self.account
        session = self.session
        old_char = account.get_puppet(session)

        if not old_char:
            self.msg("You are already OOC.")
            return

        # Store the last puppet for potential reconnection
        account.db._last_puppet = old_char

        try:
            # Attempt to unpuppet the current character
            account.unpuppet_object(session)
            self.msg("\n|GYou go OOC.|n\n")
            logger.log_sec(f"{old_char} exits the game (Account: {account}).")

            # Determine the next steps based on settings and character count
            if (
                _AUTO_PUPPET_ON_LOGIN
                and _MAX_NR_CHARACTERS == 1
                and getattr(self, "playable", False)
            ):
                self.msg(
                    "You are out-of-character (OOC).\n"
                    "Use |wconnect|n to get back into the game."
                )
            else:
                # Display the current room's description to the user
                room_description = account.at_look(target=None, session=session)
                self.msg(room_description)

        except RuntimeError as exc:
            # Handle specific runtime errors related to unpuppeting
            self.msg(f"|rCould not unpuppet from |c{old_char}|n: {exc}")
            logger.log_err(
                f"{old_char} failed to exit the game (Account: {account}). Error: {exc}"
            )
        except Exception as exc:
            # Catch all other exceptions to prevent crashes and log them
            self.msg(f"|rAn unexpected error occurred: {exc}|n")
            logger.log_err(
                f"Unexpected error when {old_char} attempted to exit the game (Account: {account}). Error: {exc}"
            )
