"""
Command module containing CmdPlay.
"""

from evennia.utils import search, utils

from commands.command import Command
from server.conf import logger


class CmdPlay(Command):
    """
    Command to play as a character.

    Usage:
      play <character>

    This command allows a player to switch to playing as a different character.
    The player can specify the character they want to play as, and if the character
    is valid and accessible to the player, they will be able to switch to that character.
    """

    key = "play"
    locks = "cmd:is_ooc()"
    aliases = ["connect", "ic", "puppet"]
    help_category = "Account"

    def get_character_candidates(self, account, args):
        """
        Get a list of character candidates based on the given arguments.

        Args:
            account (Account): The player's account.
            args (str): The arguments provided by the player.

        Returns:
            list: A list of character candidates.

        This method determines the character candidates based on the given arguments.
        If no arguments are provided, it checks if the player has a main character or
        a last puppet character. If arguments are provided, it searches for playable
        characters that match the arguments. If the player has builder permissions, it
        also searches for characters that can be puppeted by the player.
        """
        character_candidates = []

        if not args:
            if account.db._main_character:
                character_candidates.append(account.db._main_character)
            elif account.db._last_puppet:
                character_candidates.append(account.db._last_puppet)
        else:
            if account.db._playable_characters:
                character_candidates.extend(
                    utils.make_iter(
                        account.search(
                            args,
                            candidates=account.db._playable_characters,
                            search_object=True,
                            quiet=True,
                        )
                    )
                )

            if account.locks.check_lockstring(account, "perm(Builder)"):
                if self.session.puppet:
                    character_candidates = [
                        char
                        for char in self.session.puppet.search(args, quiet=True)
                        if char.access(account, "puppet")
                    ]
                else:
                    character_candidates.extend(
                        [
                            char
                            for char in search.object_search(args)
                            if char.access(account, "puppet")
                        ]
                    )

        return character_candidates

    def func(self):
        """
        Execute the play command.

        This method is called when the player executes the play command.
        It retrieves the player's account and session, checks the arguments,
        gets the character candidates, and performs the necessary actions
        to switch to the chosen character.
        """
        account = self.account
        session = self.session

        if (
            not self.args
            and not account.db._main_character
            and not account.db._last_puppet
        ):
            self.msg("Syntax: play <character>")
            return
        elif not self.args and account.db._main_character:
            character_candidates = self.get_character_candidates(
                account, account.db._main_character.key
            )
        elif not self.args and account.db._last_puppet:
            character_candidates = self.get_character_candidates(
                account, account.db._last_puppet.key
            )
        else:
            character_candidates = self.get_character_candidates(
                account, self.args
            )
            if not character_candidates:
                self.msg("That is not a valid character choice.")
                return

        new_character = character_candidates[0]

        try:
            account.puppet_object(session, new_character)
            account.db._last_puppet = new_character
            logger.log_sec(
                f"{new_character} enters the game (Account: {account})."
            )
        except RuntimeError as exc:
            self.msg(f"|rYou cannot become |C{new_character.name}|n: {exc}")
            logger.log_sec(
                f"{new_character} fails to enter the game (Account: {account})."
            )
