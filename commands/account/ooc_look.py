"""
Command module containing CmdOOCLook.
"""

from django.conf import settings
from evennia.utils import utils

from commands.command import Command

_AUTO_PUPPET_ON_LOGIN = settings.AUTO_PUPPET_ON_LOGIN
_MAX_NR_CHARACTERS = settings.MAX_NR_CHARACTERS


class CmdOOCLook(Command):
    """
    Command to implement the OOC look functionality.

    Usage:
        look

    This command allows players to look around when they are out-of-character (OOC).
    """

    key = "look"
    aliases = ["l", "ls"]
    locks = "cmd:is_ooc()"
    help_category = "Account"
    account_caller = True

    def parse(self):
        playable = self.account.characters
        # store playable property
        if self.args:
            self.playable = dict(
                (utils.to_str(char.key.lower()), char) for char in playable
            ).get(self.args.lower(), None)
        else:
            self.playable = playable

    def func(self):
        if self.session.puppet:
            self.msg("You currently have no ability to look around.")
            return

        if _AUTO_PUPPET_ON_LOGIN and _MAX_NR_CHARACTERS == 1 and self.playable:
            self.msg(
                "You are out-of-character (OOC).\nUse |wic|n to get back into the game."
            )
            return

        self.msg(
            self.account.at_look(account=self.playable, session=self.session)
        )
