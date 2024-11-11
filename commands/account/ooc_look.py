"""
Command module for OOC (Out of Character) looking functionality.
Allows players to view their characters and environment while not actively playing.
"""

from django.conf import settings

from commands.command import Command

_AUTO_PUPPET_ON_LOGIN = settings.AUTO_PUPPET_ON_LOGIN
_MAX_NR_CHARACTERS = settings.MAX_NR_CHARACTERS


class CmdOOCLook(Command):
    """
    Look around in Out-of-Character mode.

    Usage:
        look

    Without arguments, shows all available characters.
    With a character name, shows details for that specific character.
    """

    key = "look"
    aliases = ["l", "ls"]
    locks = "cmd:is_ooc()"
    help_category = "Account"
    account_caller = True

    def parse(self):
        """Parse the command input for target character selection."""
        chars = self.account.characters

        if not self.args:
            self.target_character = chars
            return

        char_dict = {char.key.lower(): char for char in chars}
        self.target_character = char_dict.get(self.args.lower())

    def func(self):
        """Execute the OOC look command."""
        if self.session.puppet:
            self.msg("You currently have no ability to look around.")
            return

        # Handle auto-puppet single character case
        if (
            _AUTO_PUPPET_ON_LOGIN
            and _MAX_NR_CHARACTERS == 1
            and self.target_character
        ):
            self.msg(
                "You are out-of-character (OOC).\n"
                "Use |wic|n to get back into the game."
            )
            return

        # Perform the actual look
        look_output = self.account.at_look(
            account=self.target_character, session=self.session
        )
        self.msg(look_output)
