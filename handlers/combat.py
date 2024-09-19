from collections import deque

from evennia.utils.utils import delay

from .handler import Handler


class CombatHandler(Handler):
    """
    A class to handle combat-related data for an object, particularly managing combatants and their enemies.

    Inherits from:
        Handler: A general-purpose data handler.

    Attributes:
        combatants (dict): A dictionary where the key is a combatant, and the value is a list of their enemies.
    """

    def __init__(
        self,
        obj,
        db_attribute_key="combat",
        db_attribute_category=None,
        default_data=None,
    ):
        """
        Initializes the CombatHandler object.

        Parameters:
            obj (object): The object for which combat data is being handled.
            db_attribute_key (str): The key under which combat data is stored.
            db_attribute_category (str, optional): The category of the attribute in the object's attributes dictionary.
            default_data (dict, optional): Default data to use for initialization, if none exists.
        """
        default_data = default_data or {"combatants": {}}
        self.is_fighting = False
        self.queue = deque()

        super().__init__(
            obj, db_attribute_key, db_attribute_category, default_data
        )

    def _valid_combatant(self, combatant):
        """
        Checks if a combatant is valid (e.g., still present in the location).

        Parameters:
            combatant: The combatant to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        if combatant.location != self.obj:
            self.remove_combatant(combatant)
            return False

        return True

    def add_combatant(self, combatant, enemies=None):
        """
        Adds a combatant and their enemies to the combatants dictionary.

        Parameters:
            combatant: The combatant to be added.
            enemies (object or list): The enemies to be added to the combatant's set of enemies.
                                      Can be a single enemy or a list of enemies.
        """
        if not enemies:
            return

        if not isinstance(enemies, list):
            enemies = [enemies]

        # Initialize combatant's enemy set if it doesn't exist
        self._data["combatants"].setdefault(combatant, set())

        # Add enemies to combatant's enemy set
        new_enemies = set(enemies)
        self._data["combatants"][combatant].update(new_enemies)

        # For each new enemy, ensure they have the combatant in their enemy set
        for enemy in new_enemies:
            self._data["combatants"].setdefault(enemy, set())
            self._data["combatants"][enemy].add(combatant)

        if not self.is_fighting:
            self.start_combat()

    def remove_combatant(self, combatant):
        """
        Removes a combatant from the combatants list and from other combatants' enemy sets.

        Parameters:
            combatant: The combatant to be removed.
        """
        if combatant in self._data["combatants"]:
            # Remove combatant from their enemies' enemy sets
            for enemy in self._data["combatants"][combatant]:
                if enemy in self._data["combatants"]:
                    self._data["combatants"][enemy].discard(combatant)
                    if not self._data["combatants"][enemy]:
                        del self._data["combatants"][enemy]

            # Remove combatant from combatants
            del self._data["combatants"][combatant]

        if not self._data["combatants"]:
            self.end_combat()

    def get_enemies(self, combatant):
        """
        Returns the set of enemies for a given combatant.

        Parameters:
            combatant: The combatant whose enemies are requested.

        Returns:
            set: A set of enemies for the specified combatant.
        """
        return self._data["combatants"].get(combatant, set())

    def all_combatants(self):
        """
        Returns all combatants in the combatants dictionary.

        Returns:
            list: A list of all combatants.
        """
        return list(self._data["combatants"].keys())

    def start_combat(self):
        """
        Initiates combat if there are combatants and combat is not already in progress.
        """
        if not self._data["combatants"] or self.is_fighting:
            return

        self.is_fighting = True
        self.queue = deque(self._data["combatants"].keys())
        self.process_next_turn()

    def process_next_turn(self):
        """
        Processes the next turn in combat.
        """
        if not self.is_fighting:
            return

        if not self.queue:
            # Start a new round or end combat
            if self.is_combat_active():
                self.queue = deque(self._data["combatants"].keys())
            else:
                self.end_combat()
                return

        combatant = self.queue.popleft()

        if not (
            self._valid_combatant(combatant) and self.get_enemies(combatant)
        ):
            # Skip to next combatant
            self.process_next_turn()
            return

        self.perform_attack(combatant)
        # Re-add combatant to queue if they still have enemies
        if self.get_enemies(combatant):
            self.queue.append(combatant)

        # Schedule the next turn after a delay
        delay(1, self.process_next_turn)

    def perform_attack(self, combatant):
        """
        Performs an attack for the given combatant.
        """
        enemies = self.get_enemies(combatant)
        if not enemies:
            return

        target = next(iter(enemies))  # Select an enemy to attack
        # Calculate damage from the combatant's weapons
        if len(combatant.equipment.weapons) == 0:
            damage = 1  # Default damage if no weapons
        elif len(combatant.equipment.weapons) >= 1:
            primary_weapon = combatant.equipment.weapons[0]
            damage = primary_weapon.damage
            self.obj.msg_contents(
                primary_weapon.db.primary_attack,
                from_obj=combatant,
                mapping={"caller": combatant, "target": target},
            )
            if len(combatant.equipment.weapons) > 1:
                secondary_weapon = combatant.equipment.weapons[1]
                damage += secondary_weapon.damage * 0.5
                self.obj.msg_contents(
                    secondary_weapon.db.secondary_attack,
                    from_obj=combatant,
                    mapping={"caller": combatant, "target": target},
                )

        target.at_damage(damage)
        if not target.is_alive():
            self.remove_combatant(target)

    def is_combat_active(self) -> bool:
        """
        Checks if combat is still active (combatants have enemies).

        Returns:
            bool: True if combat should continue, False otherwise.
        """
        return any(self.get_enemies(c) for c in self._data["combatants"])

    def end_combat(self):
        """
        Ends the combat by resetting the state.
        """
        self.is_fighting = False
        self.queue.clear()
