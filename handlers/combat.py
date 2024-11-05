from collections import deque
from typing import Any, Dict, List, Optional, Set, Union

from evennia.utils.utils import delay

from .handler import Handler


class CombatHandler(Handler):
    """Handle combat-related data and mechanics for an object.

    This handler manages combatants, their enemies, and combat flow including
    turn processing and damage calculations.

    Attributes:
        is_fighting (bool): Whether combat is currently active
        queue (deque): Queue of combatants waiting for their turn
        _data (dict): Internal storage for combat data
    """

    SCALING_DIVISOR = 100.0
    SCALING_STATS = ["strength", "dexterity", "intelligence", "faith", "arcane"]

    def __init__(
        self,
        obj: Any,
        db_attribute_key: str = "combat",
        db_attribute_category: Optional[str] = None,
        default_data: Optional[Dict] = None,
    ) -> None:
        """Initialize the combat handler.

        Args:
            obj: The object this handler is attached to
            db_attribute_key: Database attribute key for storage
            db_attribute_category: Optional category for the db attribute
            default_data: Optional initial data dictionary
        """
        default_data = default_data or {"combatants": {}}
        self.is_fighting = False
        self.queue: deque = deque()

        super().__init__(
            obj, db_attribute_key, db_attribute_category, default_data
        )

    # Combat State Management
    def is_combat_active(self) -> bool:
        """Check if combat should continue.

        Returns:
            True if any combatants still have enemies
        """
        return any(self.get_enemies(c) for c in self._data["combatants"])

    def start_combat(self) -> None:
        """Initialize combat if there are valid combatants."""
        if not self._data["combatants"] or self.is_fighting:
            return

        self.is_fighting = True
        self.queue = deque(self._data["combatants"].keys())
        self.process_next_turn()

    def end_combat(self) -> None:
        """Reset combat state."""
        self.is_fighting = False
        self.queue.clear()

    # Combatant Management
    def _valid_combatant(self, combatant: Any) -> bool:
        """Check if a combatant is still valid for combat.

        Args:
            combatant: The combatant to validate

        Returns:
            bool: True if the combatant is valid for combat
        """
        if not hasattr(combatant, "location") or combatant.location != self.obj:
            self.remove_combatant(combatant)
            return False
        if hasattr(combatant, "is_alive") and not combatant.is_alive():
            self.remove_combatant(combatant)
            return False
        return True

    def add_combatant(
        self, combatant: Any, enemies: Union[Any, List[Any]]
    ) -> None:
        """Add a combatant and their enemies to combat.

        Args:
            combatant: The combatant to add
            enemies: Single enemy or list of enemies
        """
        if not enemies:
            return

        if not isinstance(enemies, list):
            enemies = [enemies]

        self._data["combatants"].setdefault(combatant, set())
        new_enemies = set(enemies)
        self._data["combatants"][combatant].update(new_enemies)

        for enemy in new_enemies:
            self._data["combatants"].setdefault(enemy, set())
            self._data["combatants"][enemy].add(combatant)

        if not self.is_fighting:
            self.start_combat()
        else:
            self.queue.append(combatant)

    def remove_combatant(self, combatant: Any) -> None:
        """Remove a combatant from combat.

        Args:
            combatant: The combatant to remove
        """
        if combatant in self._data["combatants"]:
            for enemy in self._data["combatants"][combatant]:
                if enemy in self._data["combatants"]:
                    self._data["combatants"][enemy].discard(combatant)
                    if not self._data["combatants"][enemy]:
                        del self._data["combatants"][enemy]

            del self._data["combatants"][combatant]

        if not self._data["combatants"]:
            self.end_combat()

    # Combat Actions
    def process_next_turn(self) -> None:
        """Process the next turn in the combat sequence."""
        if not self.is_fighting:
            return

        if not self.queue:
            if self.is_combat_active():
                self.queue = deque(self._data["combatants"].keys())
            else:
                self.end_combat()
                return

        combatant = self.queue.popleft()

        if not (
            self._valid_combatant(combatant) and self.get_enemies(combatant)
        ):
            self.process_next_turn()
            return

        self.perform_attack(combatant)
        if self._valid_combatant(combatant) and self.get_enemies(combatant):
            self.queue.append(combatant)

        delay(1, self.process_next_turn)

    def perform_attack(self, combatant: Any) -> None:
        """Execute an attack action for a combatant.

        Args:
            combatant: The attacking combatant
        """
        enemies = self.get_enemies(combatant)
        if not enemies:
            return

        target = next(iter(enemies))
        damage = self._calculate_damage(combatant, target)

        target.at_damage(damage)
        if not target.is_alive():
            self.remove_combatant(target)

    def _calculate_weapon_damage(
        self, weapon: Any, attacker: Any, is_secondary: bool = False
    ) -> float:
        """Calculate damage for a single weapon including stat scaling.

        Args:
            weapon: The weapon being used
            attacker: The attacking combatant
            is_secondary: Whether this is a secondary weapon

        Returns:
            float: Base damage plus stat scaling bonuses
        """
        # Apply secondary weapon penalty if applicable
        base_damage = weapon.damage * (0.5 if is_secondary else 1.0)

        try:
            # Calculate stat scaling bonuses
            stat_bonuses = round(
                sum(
                    attacker.stats[stat].value
                    * weapon.scaling[stat].value
                    / self.SCALING_DIVISOR
                    for stat in self.SCALING_STATS
                    if stat in weapon.scaling.all()
                    and stat in attacker.stats.all()
                )
            )
        except Exception as e:
            attacker.msg(f"Error: {e}")
            stat_bonuses = 0

        return base_damage + stat_bonuses

    def _calculate_damage(self, attacker: Any, target: Any) -> float:
        """Calculate total attack damage based on equipped weapons.

        Args:
            attacker: The attacking combatant
            target: The target of the attack

        Returns:
            float: The calculated damage amount
        """
        weapons = attacker.equipment.weapons
        if not weapons:
            return 1.0

        total_damage = 0.0

        # Primary weapon damage
        primary_weapon = weapons[0]
        total_damage += self._calculate_weapon_damage(primary_weapon, attacker)
        self._send_attack_message(
            primary_weapon.attributes.get("attack_desc", "You attack."),
            attacker,
            target,
        )

        # Secondary weapon damage, if equipped
        if len(weapons) > 1:
            secondary_weapon = weapons[1]
            total_damage += self._calculate_weapon_damage(
                secondary_weapon, attacker, is_secondary=True
            )
            self._send_attack_message(
                secondary_weapon.attributes.get("attack_desc", "You attack."),
                attacker,
                target,
            )

        return round(total_damage)

    def _send_attack_message(
        self, message: str, attacker: Any, target: Any
    ) -> None:
        """Send attack message to the room.

        Args:
            message: The attack message to send
            attacker: The attacking combatant
            target: The target of the attack
        """
        self.obj.msg_contents(
            message,
            from_obj=attacker,
            mapping={"caller": attacker, "target": target},
        )

    # Utility Methods
    def get_enemies(self, combatant: Any) -> Set[Any]:
        """Get the set of enemies for a combatant.

        Args:
            combatant: The combatant to get enemies for

        Returns:
            Set of enemies for the combatant
        """
        return self._data["combatants"].get(combatant, set())

    def all_combatants(self) -> List[Any]:
        """Get all current combatants.

        Returns:
            List of all combatants
        """
        return list(self._data["combatants"].keys())
