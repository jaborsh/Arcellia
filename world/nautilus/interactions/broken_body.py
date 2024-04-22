from handlers.quests import QuestProgress
from handlers.rolls import RollHandler

from evennia.utils import dedent
from world.nautilus.quest import NautilusObjective

roll_handler = RollHandler()


def node_start(caller):
    quest = caller.quests.get("Nautilus")

    text = dedent(
        """\
        The navigator, easily identified by the tattered remnants of a seafarer's uniform, possesses hands forever stilled, their grip weaked around a set of charts, their lines and symbols no longer prescribed paths but rather a map of lost potential.
        """
    )

    options = [{"desc": "Investigate the Corpse", "goto": "node_investigate"}]

    if (
        quest.get_objective_status(NautilusObjective.ASSESS_BODY)
        == QuestProgress.UNSTARTED
    ):
        options.append({"desc": "Assess the Damage", "goto": "node_assessment"})

    options.append({"desc": "Leave", "goto": "node_quit"})

    return text, options


def node_investigate(caller, **kwargs):
    quest = caller.quests.get("Nautilus")

    text = dedent(
        """\
        The scene before you burns with a haunting clarity despite the haze that shrouds your vision, as if mists of the mind seek to shield you from the starkness of reality. In the midst of shadows and half-light, the figure of a man presents itself, its mortal journey concluded. Within those sightless eyes a narrative seems to linger: a tale suspended in the glass of death's own gaze.|/|/A shiver winds its way down your spine. The heart aches, whether from the chill that grips the air or from the specter of a story left untold, and you find yourself beckoned by those dead eyes to peer into the abyss and comprehend the truths that lie within their ever-still watch.
        """
    )

    options = []

    if (
        quest.get_objective_status(NautilusObjective.ASSESS_BODY)
        == QuestProgress.UNSTARTED
    ):
        options.append({"desc": "Assess the Damage", "goto": "node_assessment"})

    options.append({"desc": "Leave", "goto": "node_quit"})

    return text, options


def node_assessment(caller):
    caller.quests.set_objective(
        "Nautilus", NautilusObjective.ASSESS_BODY, "status", QuestProgress.COMPLETED
    )

    if roll_handler.check("1d20", dc=10, stat=caller.intelligence):
        text = dedent(
            """\
            |G[Intelligence Success]|n
            
            With a breath of intuition, you discern a tale of violence born from within these very walls. An intruder from a world beyond in a tempest of rage or fear that had its genesis here. The positioning of the lifeless navigator further speaks to this gruesome revelation, a placement not at random, but the end fresult of an act dictated by raw, unforgiving physics of brutality. His slump against the stern tells of an intensity that could very well have been the sentinel of his demise - a force striking with such fervor that even the vessel's sturdy build yielded to its fury.
            """
        )

        options = (
            {
                "desc": "Did I kill them? (look at your hands.)",
                "goto": "node_assessment_2",
            },
        )
    else:
        text = dedent(
            """
            |r[Intelligence Failure]|n
            
            What do you mean *assess the damage*? How would you do that? What are you even trying to do?
            """
        )

        options = {"desc": "Leave", "goto": "node_quit"}
    return text, options


def node_assessment_2(caller):
    text = dedent(
        """
        As the question knots itself within your thoughts, you instinctively raise your hands before your eyes. The act is one of seeking, perhaps for a damning confirmation or relieving absolution. In the half-light, your right hand reveals a web of bruises, delicate and dark like the shadowed underbrush of a forbidden forest. They weave across your skin in patterns both random and intricately natural.

        Yet upon closer inspection, their edges possess none of the tender rage of new wounds. They are remnants of post trials, not of this grim narrative that unfolds before you.
        """
    )

    options = ({"desc": "What did this then?", "goto": "node_assessment_3"},)

    return text, options


def node_assessment_3(caller):
    text = dedent(
        """
        A critical eye casts over the grim scene, taking in every detail with forensic precision. The absence of detritus near the fallen man, the lack of splintered remains one might expect to find had there been a forceful withdrawal, suggests a certain cleanliness to the violent act. A silence hangs over the probable method of dispatch, as if the very air hesitates to confirm your suspicions.

        The remnants of the scene intimate at a conclusion delivered swiftly from a distance - the hallmark of a projectile's lethal kiss. Not a blade or blunt instrument wielded by hand, which would have left a telltale trace of its passage back to the aggressor. A spell, perhaps.
        """
    )

    options = ({"desc": "Leave", "goto": "node_quit"},)

    return text, options


def node_quit(caller, raw_string, **kwargs):
    caller.msg("You step away from the body.")
    return "", {}
