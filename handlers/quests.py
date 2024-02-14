from evennia.utils import dbserialize


class QuestHandler:
    def __init__(self, obj):
        self.obj = obj
        self.do_save = False
        self._load()

    def _load(self):
        self.storage = self.obj.attributes.get("quests", category="quests", default={})

    def _save(self):
        self.obj.attributes.add("quests", self.storage, category="quests")
        self._load()
        self.do_save = False

    def add(self, quest):
        """
        Add a new quest

        Args:
            quest (EvAdventureQuest): The quest class to start.

        """
        self.storage[quest.key] = quest(self.obj)
        self._save()

    def get(self, quest):
        """
        Get the quest stored on character, if any.

        Args:
            quest (str): The name of the quest to check for.

        Returns:
            EvAdventureQuest or None: The quest stored, or None if
                Character is not on this quest.

        """
        return self.storage.get(quest)

    def has(self, quest):
        """
        Check if a given quest is registered with the Character.

        Args:
            quest (str): The name of the quest to check for.

        Returns:
            bool: If the character is following this quest or not.

        """
        return bool(self.storage.get(quest))

    def remove(self, quest):
        """
        Remove a quest. If not complete, it will be abandoned.

        Args:
            quest (str): The quest to remove.

        """
        quest = self.storage.pop(quest, None)
        if not quest.is_completed:
            # make sure to cleanup
            quest.abandon()
        self._save()

    def check_progress(self, quest, *args, **kwargs):
        """
        Check progress of a given quest or all quests.

        Args:
            quest (str, optional): If given, check the progress of this quest (if we have it),
                otherwise check progress on all quests.
            *args, **kwargs: Will be passed into each quest's `progress` call.

        """
        if quest in self.storage:
            quests = [self.storage[quest]]
        else:
            quests = self.storage.values()

        for quest in quests:
            quest.progress(*args, **kwargs)

        if self.do_save:
            self._save()


class Quest:
    """ """

    key = "quest"
    desc = "This is the base quest class"
    start_stage = 0

    abandoned_text = "This quest is abandoned!"
    finished_text = "This quest is completed!"

    def __init__(self, quester, start_stage=0):
        if " " in self.key:
            raise TypeError("The quest name must not have spaces in it.")

        self.current_stage = start_stage or self.start_stage
        self.quester = quester
        self.abandoned = False
        self.finished = False

    def __serialize_dbobjs__(self):
        self.quester = dbserialize.dbserialize(self.quester)

    def __deserialize_dbobjs__(self):
        if isinstance(self.quester, bytes):
            self.quester = dbserialize.dbunserialize(self.quester)

    @property
    def questhandler(self):
        return self.quester.quests

    @property
    def stage(self):
        return self.current_stage

    @stage.setter
    def stage(self, stage):
        self.current_stage = stage
        self.questhandler.do_save = True
        self.questhandler._save()

    def progress(self, *args, **kwargs):
        if not (self.finished or self.abandoned):
            getattr(self, f"stage_{self.current_stage}")(*args, **kwargs)

    def abandon(self):
        self.abandoned = True
        self.cleanup()

    def complete(self):
        self.finished = True
        self.cleanup()

    def cleanup(self):
        """
        This is called both when completing the quest, or when it is abandoned prematurely.
        Make sure to cleanup any quest-related data stored when following the quest.
        """
        pass

    def help(self):
        """
        This is used to get help (or a reminder) of what needs to be done to complete the current
        quest-step.

        Returns:
            str: The help text for the current step.

        """
        if self.is_completed:
            return self.completed_text

        help_resource = (
            getattr(self, f"help_{self.current_step}", None)
            or "You need to {self.current_step} ..."
        )
        if callable(help_resource):
            # the help_<current_step> can be a method to call
            return help_resource()
        else:
            # normally it's just a string
            return str(help_resource)
