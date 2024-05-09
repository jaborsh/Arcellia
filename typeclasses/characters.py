"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from django.conf import settings
from handlers import quests

from evennia.objects.objects import DefaultCharacter
from evennia.utils.utils import (
    lazy_property,
    variable_from_module,
)

from .entities import Entity
from .objects import ObjectParent

_AT_SEARCH_RESULT = variable_from_module(*settings.SEARCH_AT_RESULT.rsplit(".", 1))


class Character(Entity, ObjectParent, DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_post_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the prelogout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    prelogout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.locks.add("msg:all()")

    @lazy_property
    def quests(self):
        return quests.QuestHandler(self, db_attribute_key="quests")

    @property
    def background(self):
        return self.traits.get("background")

    # Combat
    def execute_combat_turn(self):
        if not self.ndb.combat_action:
            self.msg("You attack.")
            return

        # Perform combat action
        pass
