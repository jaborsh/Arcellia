from enum import Enum

from handlers.quests import Quest, QuestProgress


class NautilusDetail(Enum):
    PLAYER_VOMIT = "player vomit"


class NautilusObjective(Enum):
    ESCAPE = "escape"
    ASSESS_BODY = "assess body"
    FREE_ENCHANTRESS = "free enchantress"
    SEDUCE_ENCHANTRESS = "seduce enchantress"
    REACH_HELM = "reach helm"
    SAIL_TO_ELM = "sail to elm"


class NautilusQuest(Quest):
    key = "Nautilus"
    initial_details = {
        NautilusDetail.PLAYER_VOMIT: False,
    }

    initial_objectives = {
        NautilusObjective.ESCAPE: {
            "name": "Escape the Nautilus",
            "description": "You've awoken in a strange place. You need to find a way to escape.",
            "hidden": False,
            "status": QuestProgress.UNSTARTED,
        },
        NautilusObjective.ASSESS_BODY: {
            "name": "Assess the Body",
            "description": "You've found a dead body. You should investigate it.",
            "hidden": True,
            "status": QuestProgress.UNSTARTED,
        },
        NautilusObjective.FREE_ENCHANTRESS: {
            "name": "Free the Enchantress",
            "description": "You've found the Enchantress. She's trapped in a cage. You should free her.",
            "hidden": False,
            "status": QuestProgress.UNSTARTED,
        },
        NautilusObjective.SEDUCE_ENCHANTRESS: {
            "name": "Seduce the Enchantress",
            "description": "Seduce the Enchantress?",
            "hidden": True,
            "status": QuestProgress.UNSTARTED,
        },
        NautilusObjective.REACH_HELM: {
            "name": "Reach the Nautilus' Helm",
            "description": "You've met the Enchantress. She's told you to find the Nautilus' Helm and set sail to Elm.",
            "hidden": False,
            "status": QuestProgress.UNSTARTED,
        },
        NautilusObjective.SAIL_TO_ELM: {
            "name": "Sail to Freedom",
            "description": "Sail away to Elm.",
            "hidden": False,
            "status": QuestProgress.UNSTARTED,
        },
    }

    def start(self):
        super().start()
        self.objectives[NautilusObjective.ESCAPE]["status"] = QuestProgress.IN_PROGRESS
