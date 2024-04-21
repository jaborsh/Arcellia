from handlers.quests import Quest, QuestProgress


class NautilusQuest(Quest):
    key = "Nautilus"
    initial_details = {
        "body_assessment": False,
        "pulled_lever": None,
        "enchantress": False,
        "enchantress_freed": False,
        "enchantress_vomit": False,
    }
    initial_objectives = {
        "escape": {
            "name": "Escape the Nautilus",
            "description": "You've awoken in a strange place. You need to find a way to escape.",
            "hidden": False,
            "status": QuestProgress.UNSTARTED,
        },
        "helm": {
            "name": "Find the Nautilus' Helm",
            "description": "You've met the Enchantress. She's told you to find the Nautilus' Helm and set sail to Elm.",
            "hidden": False,
            "status": QuestProgress.UNSTARTED,
        },
        "freedom": {
            "name": "Sail to Freedom",
            "description": "Sail away to Elm.",
            "hidden": False,
            "status": QuestProgress.UNSTARTED,
        },
    }

    def start(self):
        super().start()
        self.objectives["escape"]["status"] = QuestProgress.IN_PROGRESS
