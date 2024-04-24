from .handler import Handler


class CombatHandler(Handler):
    """
    A class that handles combat-related operations.

    Attributes:
        _data (dict): A dictionary that stores the combat data.

    Methods:
        engage(initiator, target): Engages two entities in combat.
        disengage(entity, **kwargs): Disengages an entity from combat.
        is_engaged(entity, target): Checks if an entity is engaged with a target.
        get_combatants(entity): Returns the set of combatants for a given entity.
        all_combatants(): Returns a list of all entities engaged in combat.
    """

    # def __init__(
    #     self, obj, db_attribute_key, db_attribute_category=None, default_data={}
    # ):
    #     self._combat_active = False
    #     super().__init__(obj, db_attribute_key, db_attribute_category, default_data)

    def engage(self, initiator, target):
        """
        Engages two entities in combat.

        Args:
            initiator: The entity initiating the combat.
            target: The entity being targeted for combat.
        """
        if initiator not in self._data:
            self._data[initiator] = set()

        if target not in self._data:
            self._data[target] = set()

        self._data[initiator].add(target)
        self._data[target].add(initiator)

        # if not self._combat_active:
        #     self._combat_active = True

        self._save()

    def disengage(self, entity, **kwargs):
        """
        Disengages an entity from combat.

        Args:
            entity: The entity to disengage from combat.
            targets (optional): A list of specific targets to disengage from. If not provided, disengages from all targets.
        """
        targets = kwargs.get("targets", None)

        if not targets:
            if entity in self._data:
                for opponent in list(self._data[entity]):
                    self._data[opponent].remove(entity)
                    if not self._data[opponent]:
                        del self._data[opponent]
                del self._data[entity]
        else:
            for target in targets:
                if entity in self._data:
                    self._data[entity].remove(target)
                if target in self._data:
                    self._data[target].remove(entity)
                if not self._data[target]:
                    del self._data[target]
            if not self._data[entity]:
                del self._data[entity]

        self._save()

    def is_engaged(self, entity, target):
        """
        Checks if an entity is engaged with a target.

        Args:
            entity: The entity to check.
            target: The target entity to check against.

        Returns:
            bool: True if the entity is engaged with the target, False otherwise.
        """
        return target in self._data.get(entity, set())

    def get_combatants(self, entity):
        """
        Returns the set of combatants for a given entity.

        Args:
            entity: The entity to get the combatants for.

        Returns:
            set: A set of combatant entities.
        """
        return self._data.get(entity, set())

    def get_ordered_combatants(self):
        return sorted(self._data.keys(), key=lambda entity: entity.dexterity)

    def all_combatants(self):
        """
        Returns a list of all entities engaged in combat.

        Returns:
            list: A list of entities engaged in combat.
        """
        return list(self._data.keys())
