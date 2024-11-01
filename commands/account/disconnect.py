"""
Command module containing CmdDisconnect.
"""

from django.conf import settings

from commands.command import Command
from server.conf import logger

_AUTO_PUPPET_ON_LOGIN = settings.AUTO_PUPPET_ON_LOGIN
_MAX_NR_CHARACTERS = settings.MAX_NR_CHARACTERS


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

    def func(self):
        """Implement function"""
        account = self.account
        session = self.session
        old_char = account.get_puppet(session)

        if not old_char:
            self.msg("You are already OOC.")
            return

        account.db._last_puppet = old_char

        try:
            account.unpuppet_object(session)
            self.msg("\n|GYou go OOC.|n\n")
            logger.log_sec(f"{old_char} exits the game (Account: {account}).")

            if (
                _AUTO_PUPPET_ON_LOGIN
                and _MAX_NR_CHARACTERS == 1
                and self.playable
            ):
                self.msg(
                    "You are out-of-character (OOC).\n"
                    "Use |wconnect|n to get back into the game."
                )
            else:
                self.msg(account.at_look(target=None, session=session))

        except RuntimeError as exc:
            self.msg(f"|rCould not unpuppet from |c{old_char}|n: {exc}")
            logger.log_sec(
                f"{old_char} fails to exit the game (Account: {account})."
            )
