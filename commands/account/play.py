"""
Command module containing CmdPlay and CharacterManager.
"""

from evennia.utils import search, utils

from commands.command import Command


class CharacterManager:
    """Handles character-related operations for the play command."""

    def __init__(self, account, session):
        self.account = account
        self.session = session

    def find_playable_characters(self, query):
        candidates = []

        if self.account.db._playable_characters:
            candidates.extend(
                utils.make_iter(
                    self.account.search(
                        query,
                        candidates=self.account.db._playable_characters,
                        search_object=True,
                        quiet=True,
                    )
                )
            )

        if self.account.locks.check_lockstring(self.account, "perm(Builder)"):
            candidates.extend(self._find_builder_characters(query))

        return candidates

    def _find_builder_characters(self, query):
        if self.session.puppet:
            return [
                char
                for char in self.session.puppet.search(query, quiet=True)
                if char.access(self.account, "puppet")
            ]
        return [
            char
            for char in search.object_search(query)
            if char.access(self.account, "puppet")
        ]

    def get_default_character(self):
        if self.account.db._main_character:
            return self.account.db._main_character
        if self.account.db._last_puppet:
            return self.account.db._last_puppet
        if self.account.db._playable_characters:
            return self.account.db._playable_characters[0]
        return None


class CmdPlay(Command):
    """
    Switch to playing as a different character.

    Usage:
      play <character>
    """

    key = "play"
    locks = "cmd:is_ooc()"
    aliases = ["connect", "ic", "puppet"]
    help_category = "Account"

    def func(self):
        manager = CharacterManager(self.account, self.session)
        query = self.args.strip() if self.args else ""

        character = self._get_character_choice(manager, query)
        if not character:
            return

        self._switch_character(character)

    def _get_character_choice(self, manager, query):
        if not query:
            character = manager.get_default_character()
            if not character:
                self.msg("Syntax: play <character>")
                return None
            return character

        candidates = manager.find_playable_characters(query)
        if not candidates:
            self.msg("That is not a valid character choice.")
            return None

        return candidates[0]

    def _switch_character(self, character):
        try:
            self.account.puppet_object(self.session, character)
            self.account.db._last_puppet = character
        except RuntimeError as exc:
            self.msg(f"|rYou cannot become |C{character.name}|n: {exc}")
