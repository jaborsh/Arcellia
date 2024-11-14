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
from evennia.utils import create
from evennia.utils.utils import (
    lazy_property,
    variable_from_module,
)

from handlers import quests
from handlers.clothing.clothing import ClothingHandler
from prototypes import flasks
from world.characters.guilds.registry import GuildEnums, guild_registry

from .entities import Entity
from .objects import Object

_AT_SEARCH_RESULT = variable_from_module(
    *settings.SEARCH_AT_RESULT.rsplit(".", 1)
)

# Constants
BASE_STAT_VALUE = 100
STAT_INCREMENT = 10
HUMAN_VERSATILITY_MULTIPLIER = 1.25


class Character(Entity, Object, DefaultCharacter):
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

    VALID_STATS = {"health", "mana", "stamina"}

    def at_object_creation(self):
        """Initialize character attributes and properties."""
        super().at_object_creation()
        self.locks.add("msg:all()")
        self._init_guild()

    def basetype_setup(self):
        """
        Setup character-specific security.

        You should normally not need to overload this, but if you do,
        make sure to reproduce at least the two last commands in this
        method (unless you want to fundamentally change how a
        Character object works).
        """
        super().basetype_setup()
        # add the default cmdset
        self.cmdset.add_default(settings.CMDSET_CHARACTER, persistent=True)

    def _init_guild(self):
        """Initialize character's guild membership."""
        self.traits.add(
            "guilds",
            "Guilds",
            value={GuildEnums.ADVENTURER: guild_registry.get("adventurer")},
        )

    def init_flasks(self):
        """Initialize character's health and mana flasks."""
        for flask_type in (flasks.HEALTH_FLASK, flasks.MANA_FLASK):
            flask = spawner.spawn(flask_type)[0]
            flask.home = self
            flask.move_to(self, quiet=True)

    @lazy_property
    def clothing(self):
        return ClothingHandler(self)

    @property
    def guilds(self):
        """Character's guild memberships."""
        return self.traits.get("guilds")

    @lazy_property
    def quests(self):
        """Quest handler for the character."""
        return quests.QuestHandler(self, db_attribute_key="quests")

    def at_die(self):
        """Handle character death by creating a soul and transferring experience."""
        super().at_die()
        soul = create.create_object(
            "typeclasses.souls.Soul",
            key="soul",
            location=self.location,
        )
        soul.experience.current = self.experience.current
        soul.owner.value = self
        self.experience.current = 0

    def get_numbered_name(self, count, looker=None, **kwargs):
        return self.appearance.get_numbered_name(
            count, looker, no_article=True, **kwargs
        )
