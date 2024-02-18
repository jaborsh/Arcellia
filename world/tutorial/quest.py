from handlers.quests import Quest


class TutorialQuest(Quest):
    key = "Tutorial"
    details = {
        "body_assessment": False,
        "enchantress": False,
        "enchantress_freed": False,
        "enchantress_vomit": False,
    }
