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
from world.characters import stats
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

    def at_level(self, stat):
        if stat not in self.stats.all():
            return

        self.stats.get(stat).base += 1
        if stat == "vigor":
            self.stats.add(
                "health",
                "Health",
                trait_type="gauge",
                base=stats.HEALTH_LEVELS[self.vigor.base],
                min=0,
                max=stats.HEALTH_LEVELS[self.vigor.base],
            )
            self.health.current = self.health.max
        elif stat == "mind":
            self.stats.add(
                "mana",
                "Mana",
                trait_type="gauge",
                base=stats.MANA_LEVELS[self.mind.base],
                min=0,
                max=stats.MANA_LEVELS[self.mind.base],
            )
            self.mana.current = self.mana.max
        elif stat == "endurance":
            self.stats.add(
                "stamina",
                "Stamina",
                trait_type="gauge",
                base=stats.STAMINA_LEVELS[self.endurance.base],
                min=0,
                max=stats.STAMINA_LEVELS[self.endurance.base],
            )
            self.stamina.current = self.stamina.max

            curr_weight = self.weight.current
            self.stats.add(
                "weight",
                "Weight",
                trait_type="counter",
                base=0,
                min=0,
                max=stats.WEIGHT_LEVELS[self.endurance.base]
                * (
                    1.0
                    if not self.feats.has(racial_feats.HumanVersatility)
                    else 1.25
                ),
            )
            self.weight.current = curr_weight
