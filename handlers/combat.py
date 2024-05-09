from collections import deque
from enum import Enum, auto

from .handler import Handler


class TurnState(Enum):
    WAITING = auto()
    DONE = auto()


class CombatHandler(Handler):
    def __init__(self, obj, db_attribute_key, db_attribute_category=None):
        """Initialize combat handler with reference to the parent object."""
        super().__init__(obj, db_attribute_key, db_attribute_category, default_data={})
        self.combatants = self._data
        self.turn_queue = deque()

    def _update_turn_queue(self):
        """Update the turn order based on combatant dexterity and state."""
        sorted_combatants = sorted(
            self.combatants.keys(),
            key=lambda combatant: (
                self.combatants[combatant]["state"] == TurnState.WAITING,
                -combatant.stats.get("dexterity").value,
            ),
        )

        self.turn_queue = deque(sorted_combatants)

    def add_combatant(self, combatant, enemies):
        """Add a new combatant to the handler if not already present.

        Args:
            combatant: An instance representing a character or creature.
        """
        if combatant not in self.combatants:
            self.combatants[combatant] = {"enemies": set(), "state": TurnState.WAITING}

        self.add_enemy_relationship(combatant, enemies)
        self._update_turn_queue()
        self._save()

    def add_enemy_relationship(self, combatant, enemies):
        if not isinstance(enemies, (list, set)):
            enemies = [enemies]

        for enemy in enemies:
            self.combatants[combatant]["enemies"].add(enemy)

            if enemy not in self.combatants:
                self.combatants[enemy] = {"enemies": set(), "state": TurnState.WAITING}

            self.combatants[enemy]["enemies"].add(combatant)

    def remove_combatant(self, combatant):
        """Remove a combatant from the handler.

        Args:
            combatant: An instance representing a character or creature.
        """
        if combatant in self.combatants:
            del self.combatants[combatant]
            if combatant in self.turn_queue:
                self.turn_queue.remove(combatant)

            # Create a list of keys to safely remove elements during iteration
            for other_combatant in list(self.combatants):
                self.combatants[other_combatant]["enemies"].discard(combatant)
                if not self.combatants[other_combatant]["enemies"]:
                    del self.combatants[other_combatant]

        self._update_turn_queue()
        self._save()

    def start_round(self):
        """Start a new round of combat."""
        for combatant in self.combatants:
            self.combatants[combatant]["state"] = TurnState.WAITING

        self._update_turn_queue()
        self._save()

        while self.turn_queue:
            combatant = self.turn_queue.popleft()
            self.execute_turn(combatant)

        self.end_round()

    def execute_turn(self, combatant):
        print(f"{combatant.key} attacks!")
        self.combatants[combatant]["state"] = TurnState.DONE

    def end_round(self):
        """End the current round of combat."""
        print("The round has ended.")

    def end_combat(self):
        pass
