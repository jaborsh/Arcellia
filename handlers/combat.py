from collections import deque

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
        if default_data is None:
            default_data = {"combatants": {}, "action_queue": []}
        super().__init__(obj, db_attribute_key, db_attribute_category, default_data)

        self.action_queue = deque(self._data.get("action_queue", []))

    def add_combat(self, combatant, enemies=None):
        """
        Adds a combatant and their enemies to the combatants dictionary.

        If the combatant does not exist, they are added. Enemies are then added to their enemy list.

        Parameters:
            combatant (str): The combatant to be added.
            enemies (object or list): The enemies to be added to the combatant's list of enemies. Can be a single enemy or a list of enemies.
        """

        if not enemies:
            return

        if not isinstance(enemies, list):
            enemies = [enemies]

        self._data["combatants"].setdefault(combatant, [])

        # Add only new enemies to avoid duplicates
        existing_enemies = set(self._data["combatants"][combatant])
        new_enemies = set(enemies) - existing_enemies

        if new_enemies:
            self._data["combatants"][combatant].extend(new_enemies)

            for enemy in new_enemies:
                self._data["combatants"].setdefault(enemy, [])
                if combatant not in self._data["combatants"][enemy]:
                    self._data["combatants"][enemy].append(combatant)

        self._save()

    def remove_combatant(self, combatant):
        """
        Removes a combatant from the combatants list and from other combatants' enemy lists.

        Parameters:
            combatant (str): The combatant to be removed.
        """
        if combatant in self._data["combatants"]:
            del self._data["combatants"][combatant]

            # Remove combatant from all enemy lists
            for k in list(self._data["combatants"].keys()):
                v = self._data["combatants"][k]
                if combatant in v:
                    self._data["combatants"][k] = [e for e in v if e != combatant]

                if not self._data["combatants"][k]:
                    del self._data["combatants"][k]
                    self.remove_actions(k)

            self.remove_actions(combatant)
            self._save()

    def get_enemies(self, combatant):
        """
        Returns the list of enemies for a given combatant.

        Parameters:
            combatant (str): The combatant whose enemies are requested.

        Returns:
            list: A list of enemies for the specified combatant.
        """
        return self._data["combatants"].get(combatant, [])

    def all_combatants(self):
        """
        Returns all combatants in the combatants dictionary.

        Returns:
            list: A list of all combatants.
        """
        return list(self._data["combatants"].keys())

    def add_action(self, combatant, action):
        """
        Adds an action to the action queue for a specific combatant.

        Parameters:
            combatant (str): The combatant performing the action.
            action (str): The action to be added to the queue.
        """
        self.action_queue.append((combatant, action))
        self._data["action_queue"] = list(self.action_queue)
        self._save()

    def get_next_action(self):
        """
        Retrieves and removes the next action from the action queue.

        Returns:
            tuple: The next action in the queue (combatant, action).
        """
        if self.action_queue:
            next_action = self.action_queue.popleft()
            self._data["action_queue"] = list(self.action_queue)
            self._save()
            return next_action
        return None

    def remove_actions(self, combatant):
        """
        Removes all actions for the specified combatant from the action queue.

        Parameters:
            combatant (str): The combatant whose actions should be removed.
        """
        self.action_queue = deque(
            [(c, action) for c, action in self.action_queue if c != combatant]
        )
        self._data["action_queue"] = list(self.action_queue)
        self._save()

    def clear_actions(self):
        """
        Clears the entire action queue.
        """
        self.action_queue.clear()
        self._data["action_queue"] = []
        self._save()


class EntityCombatHandler(Handler):
    """
    A class to manage entity-specific combat data, interacting with the main CombatHandler.

    Inherits from:
        Handler: The general-purpose data handler.

    Attributes:
        combat_handler (CombatHandler): Reference to the main CombatHandler that manages combat data.
    """

    def __init__(
        self,
        obj,
        db_attribute_key="combat",
        db_attribute_category=None,
        default_data={},
    ):
        """
        Initializes the EntityCombatHandler.

        Parameters:
            obj (object): The player object for which combat data is being handled.
            db_attribute_key (str): The key under which player combat data is stored.
            db_attribute_category (str, optional): The category of the attribute in the object's attributes dictionary.
            default_data (dict, optional): Default data to use for initialization, if none exists.
        """
        super().__init__(obj, db_attribute_key, db_attribute_category, default_data)

    # a reference to the room's CombatHandler
    @property
    def combat_handler(self):
        return self.obj.location.combat
