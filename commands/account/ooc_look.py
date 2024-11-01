"""
Command module containing CmdOOCLook.
"""

from django.conf import settings

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

    def parse(self) -> None:
        """
        Parse the command input to determine the target character for the OOC look.
        """
        # Retrieve all playable characters associated with the account
        playable_characters = self.account.characters

        if self.args:
            # Create a dictionary mapping lowercase character names to character objects
            character_dict = {
                char.key.lower(): char for char in playable_characters
            }
            # Set the target character based on user input, if it exists
            self.target_character = character_dict.get(self.args.lower())
        else:
            # If no specific character is mentioned, set to all playable characters
            self.target_character = playable_characters

    def func(self) -> None:
        """
        Execute the OOC look command, displaying the appropriate information to the user.
        """
        # Check if the user is currently puppeting a character
        if self.session.puppet:
            self.msg("You currently have no ability to look around.")
            return

        # Handle the case where AUTO_PUPPET_ON_LOGIN is enabled and only one character exists
        if (
            _AUTO_PUPPET_ON_LOGIN
            and _MAX_NR_CHARACTERS == 1
            and self.target_character
        ):
            self.msg(
                "You are out-of-character (OOC).\nUse |wic|n to get back into the game."
            )
            return

        # Attempt to perform the OOC look by invoking the account's at_look method
        look_output = self.account.at_look(
            account=self.target_character, session=self.session
        )
        self.msg(look_output)
