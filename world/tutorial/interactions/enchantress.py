from evennia.utils import dedent
from world.tutorial.quest import TutorialQuest


def node_start(caller):
    if not (caller.quests.get("Tutorial")):
        caller.quests.add(TutorialQuest)

    caller.ndb._evmenu.quest = caller.quests.get("Tutorial")

    text = dedent(
        """\

        """
    )

    options = {}

    return text, options
