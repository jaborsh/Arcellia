"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from django.conf import settings
from evennia.objects.objects import DefaultCharacter
from evennia.prototypes import spawner
from evennia.utils.utils import (
    lazy_property,
    variable_from_module,
)

from handlers import quests
from prototypes import flasks
from world.features import racial as racial_feats

from .entities import Entity
from .objects import ObjectParent

_AT_SEARCH_RESULT = variable_from_module(
    *settings.SEARCH_AT_RESULT.rsplit(".", 1)
)


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

    def init_flasks(self):
        health_flask = spawner.spawn(flasks.HEALTH_FLASK)[0]
        mana_flask = spawner.spawn(flasks.MANA_FLASK)[0]
        health_flask.home = self
        mana_flask.home = self
        health_flask.move_to(self, quiet=True)
        mana_flask.move_to(self, quiet=True)

    @lazy_property
    def quests(self):
        return quests.QuestHandler(self, db_attribute_key="quests")

    def at_level(self, attribute):
        if attribute not in ("health", "mana", "stamina"):
            return

        self.level.current += 1

        if attribute == "health":
            self.stats.add(
                "health",
                "Health",
                trait_type="counter",
                base=100,
                min=0,
                max=self.health.max + 10,
            )
        elif attribute == "mana":
            self.stats.add(
                "mana",
                "Mana",
                trait_type="counter",
                base=100,
                min=0,
                max=self.mana.max + 10,
            )
        elif attribute == "stamina":
            self.stats.add(
                "stamina",
                "Stamina",
                trait_type="counter",
                base=100,
                min=0,
                max=self.stamina.max + 10,
            )

            curr_weight = self.weight.current
            max_weight = (
                self.weight.max
                if not self.feats.has(racial_feats.HumanVersatility)
                else self.weight.max / 1.25
            )
            (
                self.stats.add(
                    "weight",
                    "Weight",
                    trait_type="counter",
                    base=0,
                    min=0,
                    max=(max_weight + 10)
                    * (
                        1.0
                        if not self.feats.has(racial_feats.HumanVersatility)
                        else 1.25
                    ),
                ),
            )
            self.weight.current = curr_weight
        else:
            return

        self.stats.get(attribute).value = self.stats.get(attribute).max
