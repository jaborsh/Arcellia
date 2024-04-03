from handlers.quests import Quest


class NautilusQuest(Quest):
    key = "Nautilus"
    details = {
        "body_assessment": False,
        "pulled_lever": None,
        "enchantress": False,
        "enchantress_freed": False,
        "enchantress_vomit": False,
    }
