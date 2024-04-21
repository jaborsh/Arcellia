from copy import copy
from enum import Enum

from evennia.utils import dbserialize

from handlers.handler import Handler


class QuestProgress(Enum):
    """
    Enum for quest completion status.

    Attributes:
    - UNSTARTED: The quest has not been started yet.
    - IN_PROGRESS: The quest is currently in progress.
    - COMPLETED: The quest has been completed.
    - FAILED: The quest has failed.
    """

    UNSTARTED = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    FAILED = 3


class QuestHandler(Handler):
    """
    Handler for managing quests on a game object. Supports adding, updating,
    and checking the status of quests. Quests include details about the quest
    and its current stage.

    Quest data is saved persistently, ensuring it survives game reboots.
    Methods:
    - add_quest(quest_cls): Adds a new quest with the given quest class.
    - add_detail(quest_name, detail, value): Adds a new detail to a quest.
    - add_details(quest_name, new_details): Adds multiple details to a quest.
    - get_detail(quest_name, detail): Retrieves a specific detail from a quest.
    - get_details(quest_name): Retrieves all details of a quest.
    - get_objective(quest_name, objective, key): Retrieves the value of an
        objective's key.
    - set_objective(quest_name, objective, key, value): Sets the value of an
        objective's key.
    - get_objectives(quest_name): Retrieves all objectives of a quest.
    - update_objectives(quest_name, new_objectives): Updates the objectives of
        a quest.
    - get_status(quest_name): Retrieves the status of a quest.
    - set_status(quest_name, new_status): Sets the status of a quest.
    - remove_quest(quest_name): Removes a quest from the handler.
    - clear_quests(): Removes all quests.
    """

    def all(self):
        return self._data

    def add(self, quest_cls):
        """
        Adds a new quest to the QuestHandler.

        This method creates a new instance of the specified quest class and adds it to the QuestHandler's data dictionary. The quest is added with its key as the dictionary key and the quest object as the corresponding value.

        Parameters:
            quest_cls (class): The class of the quest to be added. The class must have a constructor that takes a single argument, which is the game object the QuestHandler is attached to.

        Returns:
            None
        """
        quest = quest_cls(self.obj)
        self._data[quest.key] = quest

    def add_detail(self, quest, detail, value):
        if quest := self._data.get(quest, None):
            if quest.status == QuestProgress.UNSTARTED:
                quest.status = QuestProgress.IN_PROGRESS

            quest.add_detail(detail, value)
            self._save()

    def add_details(self, quest, new_details):
        """
        Adds new details to a specific quest.

        This method adds new details to a specific quest in the QuestHandler's data dictionary. It retrieves the quest object based on the provided quest name and updates its details with the new_details dictionary. The updated details are then saved using the _save() method.

        Parameters:
            quest (str): The name of the quest to add details to.
            new_details (dict): A dictionary containing the new details to be added to the quest.

        Returns:
            None
        """
        if quest := self._data.get(quest, None):
            if quest.status == QuestProgress.UNSTARTED:
                quest.status = QuestProgress.IN_PROGRESS

            quest.add_details(new_details)
            self._save()

    def get_detail(self, quest, detail):
        """
        Retrieves a specific detail from a specific quest.

        This method retrieves a specific detail from a specific quest in the QuestHandler's data dictionary. It first checks if the quest exists in the data dictionary. If the quest exists, it retrieves the corresponding Quest object and then retrieves the specific detail from the Quest object's details dictionary based on the provided detail name. If the quest or the detail does not exist, it returns None.

        Parameters:
            quest (str): The name of the quest to retrieve the detail from.
            detail (str): The name of the detail to retrieve.

        Returns:
            Any or None: The value of the specific detail from the specified quest, or None if the quest or the detail does not exist.
        """
        quest = self._data.get(quest, None)
        return quest.details.get(detail) if quest else None

    def get_details(self, quest):
        """
        Retrieves the details of a specific quest.

        This method retrieves the details of a specific quest from the QuestHandler's data dictionary. It first checks if the quest exists in the data dictionary. If the quest exists, it retrieves the corresponding Quest object and then calls the 'get_details' method of the Quest object to retrieve the details. If the quest does not exist, it returns None.

        Parameters:
            quest (str): The name of the quest to retrieve the details from.

        Returns:
            dict or None: A dictionary containing the details of the specified quest, or None if the quest does not exist.
        """
        quest = self._data.get(quest, None)
        return quest.get_details() if quest else None

    def get_objective(self, quest, objective):
        """
        Retrieves the objective for a given quest.

        Args:
            quest (str): The name of the quest.
            objective (str): The name of the objective.
            key (str): The key associated with the objective.

        Returns:
            The objective associated with the given quest, objective, and key.
            Returns None if the quest is not found.

        """
        quest = self._data.get(quest)
        return quest.get_objective(objective) if quest else None

    def set_objective(self, quest, objective, key, value):
        """
        Sets the objective of a quest.

        Args:
            quest (str): The name of the quest.
            objective (str): The objective to set.
            key (str): The key of the objective.
            value (str): The value to set for the objective.

        Returns:
            None

        """
        if quest := self._data.get(quest, None):
            if quest.status == QuestProgress.UNSTARTED:
                quest.status = QuestProgress.IN_PROGRESS

            quest.set_objective(objective, key, value)

            if quest.is_complete():
                quest.complete()

            self._save()

    def get_objectives(self, quest):
        """
        Retrieve the objectives for a given quest.

        Args:
            quest (str): The name of the quest.

        Returns:
            list or None: A list of objectives for the quest, or None if the quest does not exist.
        """
        quest = self._data.get(quest, None)
        return quest.get_objectives() if quest else None

    def update_objectives(self, quest, new_objectives):
        """
        Update the objectives of a quest.

        Args:
            quest (str): The name of the quest.
            new_objectives (list): The new objectives for the quest.

        Returns:
            None
        """
        if quest := self._data.get(quest, None):
            if quest.status == QuestProgress.UNSTARTED:
                quest.status = QuestProgress.IN_PROGRESS

            quest.update_objectives(new_objectives)

            if quest.is_complete():
                quest.complete()

            self._save()

    def get_status(self, quest):
        """
        Retrieve the status of a quest.

        Args:
            quest (str): The name or identifier of the quest.

        Returns:
            str or None: The status of the quest, or None if the quest does not exist.

        """
        quest = self._data.get(quest, None)
        return quest.get_status() if quest else None

    def set_status(self, quest, new_status):
        """
        Set the status of a quest.

        Args:
            quest (str): The name of the quest.
            new_status (str): The new status to set for the quest.

        Returns:
            None
        """
        if quest := self._data.get(quest, None):
            quest.set_status(new_status)
            self._save()

    def remove(self, quest):
        """
        Removes a quest from the QuestHandler.

        This method removes a specific quest from the QuestHandler's data dictionary. It first checks if the quest exists in the data dictionary. If the quest exists, it deletes the corresponding key-value pair from the dictionary using the 'del' keyword. The updated quest data is then saved using the _save() method.

        Parameters:
            quest (str): The name of the quest to be removed.

        Returns:
            None
        """
        if quest := self._data.get(quest, None):
            del self._data[quest.key]
            self._save()

    def clear(self):
        """
        Clears all quests stored in the QuestHandler.

        This method removes all quests from the QuestHandler's data dictionary. It clears the dictionary using the 'clear' method of the dictionary object. After calling this method, the QuestHandler will have no quests stored.

        Parameters:
            None

        Returns:
            None
        """
        self._data.clear()


class Quest:
    """
    Represents an individual quest with a key, details, and current stage.

    Properties:
    - key (str): The name of the quest.
    - details (dict): A dictionary containing details of the quest, such as description, objectives, etc.
    - stage (str): The current stage of the quest, used to track progression.

    Methods:
    - update_stage(new_stage): Updates the quest's current stage.
    - is_complete(): Checks if the quest is complete based on its stage.
    - get_details(): Returns the quest's details.
    """

    key = "quest"
    initial_details = {}
    initial_objectives = {}
    initial_status = QuestProgress.UNSTARTED

    def __init__(self, quester):
        """
        Initializes a new Quest object.

        This method is called when a new Quest object is created. It sets the initial values for the quester, details, and stage attributes of the Quest object.

        Parameters:
            quester: The quester associated with the quest.
            details (dict): A dictionary containing details of the quest, such as description, objectives, etc. (default: {})
            initial_stage (int): The initial stage of the quest (default: 0)

        Returns:
            None
        """

        if " " in self.key:
            raise TypeError("The quest name must not have spaces in it.")

        self.quester = quester
        self.details = copy(self.initial_details)
        self.objectives = copy(self.initial_objectives)
        self.status = copy(self.initial_status)

    def __serialize_dbobjs__(self):
        """
        Serializes the `quester` attribute using the `dbserialize` function.

        This method is responsible for serializing the `quester` attribute of the object.
        It uses the `dbserialize` function to convert the `quester` attribute into a format
        that can be stored in a database.

        Returns:
            None

        """
        self.quester = dbserialize.dbserialize(self.quester)

    def __deserialize_dbobjs__(self):
        """
        Deserialize the quester object if it is of type bytes.

        This method checks if the `quester` attribute is an instance of `bytes`.
        If it is, it uses the `dbserialize.dbunserialize` function to deserialize
        the `quester` object.

        Returns:
            None

        """
        if isinstance(self.quester, bytes):
            self.quester = dbserialize.dbunserialize(self.quester)

    def add_detail(self, new_detail, value):
        """
        Adds a new detail to the quest.

        Parameters:
            new_detail (str): The name of the new detail to add.
            value (Any): The value of the new detail.

        Returns:
            None
        """
        self.details[new_detail] = value

    def add_details(self, new_details):
        """
        Adds new details to a specific quest.

        Parameters:
            new_details (dict): A dictionary containing the new details to be added to the quest.

        Returns:
            None
        """
        self.details.update(new_details)

    def get_detail(self, detail):
        """
        Retrieves a specific detail from a specific quest.

        Parameters:
            detail (str): The name of the detail to retrieve.

        Returns:
            Any or None: The value of the specific detail from the specified quest, or None if the quest or the detail does not exist.
        """
        return self.details.get(detail)

    def get_details(self):
        """
        Returns the details of the quest.

        Returns:
            str: The details of the quest.
        """
        return self.details

    def get_objective(self, objective):
        """
        Retrieve the value associated with the given key for the specified objective.

        Args:
            objective (str): The name of the objective.
            key: The key associated with the value to retrieve.

        Returns:
            The value associated with the given key for the specified objective.

        """
        return self.objectives.get(objective)

    def set_objective(self, objective, key, value):
        """
        Set the value of a specific key for an objective.

        Args:
            objective (str): The name of the objective.
            key (str): The key to set the value for.
            value: The value to set.

        Returns:
            None
        """
        self.objectives[objective][key] = value

    def get_objectives(self):
        """
        Returns the objectives associated with this quest.

        Returns:
            dict: A list of objectives.
        """

        return self.objectives

    def update_objectives(self, new_objectives):
        """
        Update the objectives of the quest.

        Args:
            new_objectives (dict): A dictionary containing the new objectives to be updated.

        Returns:
            None
        """
        self.objectives.update(new_objectives)

    def get_status(self):
        """
        Returns the status of the quest.

        Returns:
            Enum: The status of the quest.
        """
        return self.status

    def set_status(self, new_status):
        """
        Set the status of the quest.

        Args:
            new_status (Enum): The new status to set for the quest.

        Returns:
            None
        """
        self.status = new_status

    def is_complete(self):
        """
        Check if all objectives in the quest are completed.

        Returns:
            bool: True if all objectives are completed, False otherwise.
        """

        objectives = self.get_objectives()

        if not all(objectives[objective]["completed"] for objective in objectives):
            return False

        self.complete()
        return True

    def complete(self):
        """
        Marks the quest as completed.

        This method updates the status of the quest to 'COMPLETED'.
        """
        self.status = QuestProgress.COMPLETED
