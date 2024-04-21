from handlers.quests import Quest


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
            "name": "Find a way to escape the Nautilus",
            "description": "You've awoken in a strange place. You need to find a way to escape.",
            "hidden": False,
            "completed": False,
        },
        "helm": {
            "name": "Find the Nautilus' Helm",
            "description": "You've met the Enchantress. She's told you to find the Nautilus' Helm and sail to safety.",
            "hidden": True,
            "completed": False,
        },
        "freedom": {
            "name": "Sail to Freedom",
            "description": "You've escaped the Nautilus.",
            "hidden": True,
            "completed": False,
        },
        "finished": {
            "name": "Quest Complete",
            "description": "You've completed the Nautilus quest.",
            "hidden": True,
            "completed": False,
        },
    }
