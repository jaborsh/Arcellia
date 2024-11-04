from world.characters.guilds.guild import Guild


class Adventurer(Guild):
    key = "adventurer"

    def test(self):
        return "Hi"

    def spawn_initial_gear(self, character):
        """
        Spawns basic adventuring gear for new guild members.

        Args:
            character: The character to receive the gear
        """
        # Create basic gear set
        gear = [
            {"key": "leather armor", "typeclass": "typeclasses.objects.Armor"},
            {"key": "dagger", "typeclass": "typeclasses.objects.Weapon"},
            {"key": "backpack", "typeclass": "typeclasses.objects.Container"},
            {"key": "torch", "typeclass": "typeclasses.objects.Light"},
            {"key": "waterskin", "typeclass": "typeclasses.objects.Item"},
        ]

        # Spawn and give each item to character
        for item in gear:
            obj = character.location.spawn(**item)
            obj.move_to(character, quiet=True)
