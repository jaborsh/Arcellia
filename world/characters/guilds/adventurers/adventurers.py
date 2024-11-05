from evennia.prototypes import spawner

from world.characters.guilds.adventurers.adventurer_gear import (
    STARTING_BATTLE_AXE,
)
from world.characters.guilds.guild import Guild


class Adventurer(Guild):
    key = "adventurer"

    def spawn_initial_gear(self, character):
        """
        Spawns basic adventuring gear for new guild members.

        Args:
            character: The character to receive the gear
        """

        axe = spawner.spawn(STARTING_BATTLE_AXE)[0]
        axe.location = character
        character.equipment.wear(axe)
