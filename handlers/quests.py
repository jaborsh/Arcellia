from evennia.utils import dbserialize


class QuestHandler:
    """
    Handler for managing quests on a game object. Supports adding, updating,
    and checking the status of quests. Quests include details about the quest
    and its current stage.

    Quest data is saved persistently, ensuring it survives game reboots.

    Methods:
    - add(quest_name, details): Adds a new quest with the given details.
    - update_stage(quest_name, new_stage): Updates the stage of a quest.
    - is_quest_active(quest_name): Checks if a quest is currently active.
    - get_quest_details(quest_name): Retrieves details for a specific quest.
    - remove_quest(quest_name): Removes a quest from the handler.
    - clear_quests(): Removes all quests.
    """

    __slots__ = ("data", "db_attribute", "obj")

    def __init__(self, obj, db_attribute="quests"):
        """
        Initializes the QuestHandler attached to a game object.

        Args:
            obj: The game object this handler is attached to.
            db_attribute (str): The database attribute used for storing quest data.
        """

        if not obj.attributes.get(db_attribute, None):
            obj.attributes.add(db_attribute, {})

        self.data = obj.attributes.get(db_attribute)
        self.obj = obj
        self.db_attribute = db_attribute

    def _load(self):
        """
        Loads the quest data from the game object's attributes.

        This method retrieves the quest data from the game object's attributes using the specified database attribute. If the attribute does not exist, it initializes it with an empty dictionary. The loaded quest data is then stored in the 'data' attribute of the QuestHandler instance.

        This method is called internally by the QuestHandler class and does not need to be called directly by the user.

        Parameters:
            None

        Returns:
            None
        """
        self.data = self.obj.attributes.get(self.db_attribute, default={})

    def _save(self):
        """
        Saves the quest data to the game object's attributes.

        This method saves the quest data stored in the 'data' attribute of the QuestHandler instance to the game object's attributes using the specified database attribute. It updates the attribute with the current quest data. The saved quest data will persist even after game reboots.

        This method is called internally by the QuestHandler class and does not need to be called directly by the user.

        Parameters:
            None

        Returns:
            None
        """
        self.obj.attributes.add(self.db_attribute, self.data)
        self._load()

    def all(self):
        """
        Returns all quests stored in the QuestHandler.

        This method retrieves and returns all quests stored in the QuestHandler. It returns a dictionary containing the quest names as keys and the corresponding Quest objects as values.

        Parameters:
            None

        Returns:
            dict: A dictionary containing all quests stored in the QuestHandler. The keys are the quest names and the values are the corresponding Quest objects.
        """
        return self.data

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
        self.data[quest.key] = quest

    def get(self, quest):
        """
        Retrieves a specific quest from the QuestHandler.

        This method retrieves a specific quest from the QuestHandler's data dictionary based on the provided quest name. It returns the corresponding Quest object if the quest exists, or None if the quest does not exist.

        Parameters:
            quest (str): The name of the quest to retrieve.

        Returns:
            Quest or None: The Quest object corresponding to the provided quest name, or None if the quest does not exist.
        """
        return self.data.get(quest)

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
        if self.data.get(quest, None):
            self.data[quest].add_details(new_details)
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
        quest = self.data.get(quest, None)
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
        quest = self.data.get(quest, None)
        return quest.get_details() if quest else None

    def get_stage(self, quest):
        """
        Retrieves the current stage of a specific quest.

        This method retrieves the current stage of a specific quest from the QuestHandler's data dictionary. It first checks if the quest exists in the data dictionary. If the quest exists, it retrieves the corresponding Quest object and then calls the 'get_stage' method of the Quest object to retrieve the current stage. If the quest does not exist, it returns None.

        Parameters:
            quest (str): The name of the quest to retrieve the stage from.

        Returns:
            str or None: The current stage of the specified quest, or None if the quest does not exist.
        """
        quest = self.data.get(quest, None)
        return quest.get_stage() if quest else None

    def set_stage(self, quest, new_stage):
        """
        Sets the stage of a specific quest.

        This method sets the current stage of a specific quest in the QuestHandler's data dictionary. It first checks if the quest exists in the data dictionary. If the quest exists, it retrieves the corresponding Quest object and then calls the 'set_stage' method of the Quest object to update the stage. The updated stage is then saved using the _save() method.

        Parameters:
            quest (str): The name of the quest to set the stage for.
            new_stage (str): The new stage to set for the quest.

        Returns:
            None
        """
        if self.data.get(quest, None):
            self.data[quest].set_stage(new_stage)
            self._save()

    def remove_quest(self, quest):
        """
        Removes a quest from the QuestHandler.

        This method removes a specific quest from the QuestHandler's data dictionary. It first checks if the quest exists in the data dictionary. If the quest exists, it deletes the corresponding key-value pair from the dictionary using the 'del' keyword. The updated quest data is then saved using the _save() method.

        Parameters:
            quest (str): The name of the quest to be removed.

        Returns:
            None
        """
        if quest in self.data:
            del self.data[quest]
            self._save()

    def clear_quests(self):
        """
        Clears all quests stored in the QuestHandler.

        This method removes all quests from the QuestHandler's data dictionary. It clears the dictionary using the 'clear' method of the dictionary object. After calling this method, the QuestHandler will have no quests stored.

        Parameters:
            None

        Returns:
            None
        """
        self.data.clear()


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
    details = {}
    stage = 0

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

    def __serialize_dbobjs__(self):
        self.quester = dbserialize.dbserialize(self.quester)

    def __deserialize_dbobjs__(self):
        if isinstance(self.quester, bytes):
            self.quester = dbserialize.dbunserialize(self.quester)

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
        return self.details

    def get_stage(self):
        """
        Retrieves the current stage of a specific quest.

        This method retrieves the current stage of a specific quest. It returns the value of the quest's stage attribute.

        Parameters:
            None

        Returns:
            str: The current stage of the specified quest.
        """
        return self.stage

    def set_stage(self, new_stage):
        """
        Sets the stage of a specific quest.

        This method updates the current stage of a specific quest. It takes a new_stage parameter, which represents the new stage to set for the quest. The method sets the quest's stage attribute to the new_stage value.

        Parameters:
            new_stage (str): The new stage to set for the quest.

        Returns:
            None
        """
        self.stage = new_stage
