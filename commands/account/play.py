"""
Command module containing CmdPlay.
"""

from evennia.utils import search, utils

from commands.command import Command


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

    def _search_characters(self, query):
        """
        Search for playable characters based on the given query.

        Args:
            query (str): The search query provided by the player.

        Returns:
            list: A list of playable character objects matching the query.
        """
        account = self.account
        character_candidates = []

        if account.db._playable_characters:
            character_candidates.extend(
                utils.make_iter(
                    account.search(
                        query,
                        candidates=account.db._playable_characters,
                        search_object=True,
                        quiet=True,
                    )
                )
            )

        if account.locks.check_lockstring(account, "perm(Builder)"):
            if self.session.puppet:
                character_candidates.extend(
                    [
                        char
                        for char in self.session.puppet.search(
                            query, quiet=True
                        )
                        if char.access(account, "puppet")
                    ]
                )
            else:
                character_candidates.extend(
                    [
                        char
                        for char in search.object_search(query)
                        if char.access(account, "puppet")
                    ]
                )

        return character_candidates

    def _get_default_character(self):
        """
        Get the default character for the player, if any.

        Returns:
            Object or None: The main or last puppet character, if any.
        """
        account = self.account

        if account.db._main_character:
            return account.db._main_character
        elif account.db._last_puppet:
            return account.db._last_puppet
        elif account.db._playable_characters:
            return account.db._playable_characters[0]

        return None

    def _switch_to_character(self, character):
        """
        Switch the player's session to control the given character.

        Args:
            character (Object): The character to switch to.
        """
        account = self.account
        session = self.session

        try:
            account.puppet_object(session, character)
            account.db._last_puppet = character
        except RuntimeError as exc:
            self.msg(f"|rYou cannot become |C{character.name}|n: {exc}")

    def func(self):
        """
        Execute the play command.

        This method is called when the player executes the play command.
        It retrieves the player's account and session, checks the arguments,
        gets the character candidates, and performs the necessary actions
        to switch to the chosen character.
        """
        character_query = self.args

        if not character_query:
            default_character = self._get_default_character()
            if not default_character:
                self.msg("Syntax: play <character>")
                return
            character_candidates = [default_character]
        else:
            character_candidates = self._search_characters(character_query)

        if not character_candidates:
            self.msg("That is not a valid character choice.")
            return

        new_character = character_candidates[0]
        self._switch_to_character(new_character)
