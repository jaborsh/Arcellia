from handlers.quests import Quest


class TutorialQuest(Quest):
    key = "Tutorial"
    details = {
        "body_assessment": False,
    }

    # Stage 0 - Initialization
    # Stage 1 - Investigated the Body
