from enum import Enum

from class_registry import ClassRegistry

from world.characters.guilds import adventurers

guild_registry = ClassRegistry()
guild_registry._register(adventurers.Adventurer.key, adventurers.Adventurer)


class GuildEnums(Enum):
    ADVENTURER = "adventurer"
