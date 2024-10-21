from enum import Enum, auto

from handlers.quests import Quest, QuestProgress


class ArrivalObjective(Enum):
    MEET_AEUM = auto()
    READ_BOOK = auto()
    REACH_EMBERLYN = auto()


class ArrivalQuest(Quest):
    key = "Arrival"

    initial_objectives = {
        ArrivalObjective.MEET_AEUM: {
            "name": "A Veil on the Beach",
            "description": "The waves of Emberlyn Beach crash softly against the shore, carrying with them a chill that pricks the skin. Amongst the driftwood and salt-streaked rocks, a woman stands, her figure draped in a veil as though spun from the sea's own mist. Her presence is a whisper amidst the ocean's roar, beckoning for discovery, yet offering no clear invitation. She awaits.",
            "hidden": False,
            "status": QuestProgress.UNSTARTED,
        },
        ArrivalObjective.READ_BOOK: {
            "name": "Shanties in the Sand",
            "description": "Somewhere among the driftwood and the forgotten debris of Emberlyn Beach, a book lies half-buried in the sand, its pages weathered and worn by the sea's touch.",
            "hidden": False,
            "status": QuestProgress.UNSTARTED,
        },
    }

    def start(self):
        super().start()
        self.objectives[ArrivalObjective.MEET_AEUM]["status"] = (
            QuestProgress.IN_PROGRESS
        )
        self.objectives[ArrivalObjective.READ_BOOK]["status"] = (
            QuestProgress.IN_PROGRESS
        )
