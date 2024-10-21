from evennia.utils import dedent

from handlers.quests import QuestProgress
from handlers.rolls import RollHandler
from world.quests.emberlyn.emberlyn_start_quest import ArrivalObjective

roll_handler = RollHandler()


def node_start(caller):
    text = dedent(
        """
        She lifts her hand and in that motion the air around her seems to shimmer. A single wisp of smoke coils upward, though no pipe or ember lies in her grasp. The smoke dances, swirling unnaturally before curling back around her fingers. Her lips part in a languid smile.
        
        \"You've come a long way,\" her voice is soft, almost drowned by the sound of the waves, yet it reaches you clear as a bell.
        
        The smoke drifts lazily between you, forming fleeting shapes - a bird, a blade, a key - before dissolving back into the sea air. She waits for you to begin, though she seems as if she already knows what you will say.
        """
    )

    if roll_handler.check("1d20", dc=10):
        text += dedent(
            """
            |#FFA500Something tugs at the edges of your perception, something most might miss. A subtle shift in the light as the veil moves reveals the rich brown of her eyes, earthy and warm beneath the mysterious air she weaves around herself. There is youth there too - she cannot be much older than her twenties.|n
            """
        )

    options = (
        {"desc": "Where am I?", "goto": "node_aeum_1_1"},
        {"desc": "[Leave]", "goto": "node_quit"},
    )

    return text, options


def node_aeum_1_1(caller):
    def _callback_seeking(caller):
        caller.msg(
            dedent(
                """
                The woman nods slowly, as though your answer was not only expected but inevitable. The smoke around her fingers curls tighter, condensing into a single thin line that spirals upward before dissolving into the breeze.
                
                \"Seeking... Yes,\" she murmurs, her voice dipping into something softer. \"Everyone comes to this shore seeking something. A truth they've lost... a hope they've long forgotten.\"
                """
            )
        )
        return "node_aeum_hub"

    def _callback_running(caller):
        caller.msg(
            dedent(
                """
                At your words, the woman's smile widens, though her eyes remain unreadable beneath the veil. The smoke around her fingers flickers and fans out, stretching in all directions before vanishing into the salty air.
                
                \"Running,\" she repeats, the word rolling off her tongue like a stone skipping across the water. \"Many come here with the weight of the world chasing them. But the sea? The sea forgets. It swallows everything eventually - memories, mistakes, even names.\"
                """
            )
        )
        return "node_aeum_hub"

    text = dedent(
        """
        She tilts her head slightly, the veil shifting just enough to reveal a faint gleam in her eyes. The smoke curls once more around her fingers, as if considering your question with her.
        
        \"Where are you?\" she repeats softly. She gestures lazily to the expanse of the beach, the ocean stretching endlessly beyond it. \"You're where the world forgets itself.\"
            
        The smoke twists, though the lines blur and fade. \"But where you truly are,\" she continues, her tone turning conspiratorial, \"that depends on you, doesn't it? Some come here seeking. Others, running. And you?\" Her gaze sharpens behind her hood.
            
        \"Which are you?\"
        """
    )

    options = (
        {"desc": "Seeking.", "goto": _callback_seeking},
        {"desc": "Running.", "goto": _callback_running},
        {"desc": "[Leave]", "goto": "node_quit"},
    )

    return text, options


def node_aeum_hub(caller):
    options = (
        {"desc": "What am I doing here?", "goto": "node_aeum_2_1"},
        {"desc": "[Leave]", "goto": "node_quit"},
    )
    return "Smoke idly curls from her fingertips.", options


def node_aeum_2_1(caller):
    text = dedent(
        """
        At your question, the woman's expression softens, though the hood hides most of her face. The smoke swirling around her falters a moment, as if caught in some unseen current. Her fingers trace slow patterns in the air, and her voice, when it comes, is thick with something unspoken - sadness, perhaps, or a weariness that runs deeper.
                
        \"That is a question with many answers, none of which you'll find in the sand beneath your feet. Fate brought you to Emberlyn, as it brings all who tread this shore. There are forces stirring in the world, shadows stretching far beyond this place. |CYou are part of something greater now|n. Something that looms, unseen, yet inevitable.\"
        """
    )

    options = (
        {"desc": "What do you mean?", "goto": "node_aeum_2_2"},
        {"desc": "[Leave]", "goto": "node_quit"},
    )

    return text, options


def node_aeum_2_2(caller):
    text = dedent(
        """
        The woman lets out a soft, breathy chuckle, though there's no humor in it. The smoke between her fingers twist tighter, like a thread wound too tight, before she lets it unravel again into the air.
        
        \"Life... it has a way of turning harder, doesn't it? The tides get rougher, the winds colder. We lose things along the way - people, places, pieces of ourselves.\" Her eyes seem to look past you, into the distance, or perhaps into the past.
        
        "And yet," she continues, "we go on. Step by step, we keep walking, even when the road crumbles beneath us. That's what it means to live, isn't it? To endure. To carry the weight of what's broken even when it feels too heavy."
        """
    )

    options = (
        {"desc": "Yeah, we go on, alright.", "goto": "node_aeum_2_3_1"},
        {
            "desc": "In that case, doesn't life get hard *because* we go on?",
            "goto": "node_aeum_2_3_2",
        },
        {
            "desc": "Maybe we should stop going on, then.",
            "goto": "node_aeum_2_3_3",
        },
    )

    return text, options


def node_aeum_2_3_1(caller):
    text = dedent(
        """
        The woman shifts slightly and her head tilts, and for a moment, the smoke between her fingers stills. Her voice is quiet, almost a murmur:
        
        "Do we?" she asks, the faintest doubt creeping into her tone. "I wonder... Some do. Some keep walking, even when the way is lost. But others..." Her voice trails off, the sentence left unfinished, hanging in the air like the last tendril of smoke before it dissipates.
        """
    )

    options = (
        {"desc": "So, what's happening?", "goto": "node_aeum_2_4"},
        {"desc": "[Leave]", "goto": "node_quit"},
    )

    return text, options


def node_aeum_2_3_2(caller):
    text = dedent(
        """
        The woman's lips curve slightly beneath the veil, a fleeting smile touched with a hint of sad understanding. The smoke curls once more around her fingers, forming a brief, delicate spiral.
        
        "Perhaps you are right," she says, her tone thoughtful. "Each step, each breath, we carry the weight forward, and it presses down until the road itself begins to give away beneath us." She pauses, letting the words linger before continuing.
        
        "But even whyen the road breaks... there's always something - or someone - to slow the fall. Heroes. Those who patch the cracks, even for a little while. The pace changes. The world shifts. Sometimes, for a moment, we find firmer ground." She looks at you, the smile gone.
        """
    )

    options = (
        {"desc": "So, what's happening?", "goto": "node_aeum_2_4"},
        {"desc": "[Leave]", "goto": "node_quit"},
    )

    return text, options


def node_aeum_2_3_3(caller):
    text = dedent(
        """
        The woman regards you for a long, quiet moment, her hood rippling softly in the breeze. When she speaks, her voice is low, touched with empathy and a knowing sadness.
        
        "That thought... it's crossed more minds than you'd think," she replies gently. "And perhaps this isn't the first time it's crossed yours." The smoke in her hand coils, tightening briefly, before loosening into a soft, slow drift. "But whether we stop or go on... the world doesn't wait. It moves, with or without us."
        
        She says nothing more.
        """
    )

    options = (
        {"desc": "So, what's happening?", "goto": "node_aeum_2_4"},
        {"desc": "[Leave]", "goto": "node_quit"},
    )

    return text, options


def node_aeum_2_4(caller):
    text = dedent(
        """
        The woman's eyes seem to darken. Her voice is soft, as though speaking too loudly might shatter something fragile in the air between you.
        
        "Imagine a song - a slow, sorrowful tune. One that starts soft, barely noticeable at first. But it keeps playing. Over and over, like a broken instrument, and after a while, you can't help but hear it, feel it, deep in your bones."
        
        Her fingers trace a slow pattern in the air, the smoke following, twisting into shapes like notes hanging on invisible strings. "At first, some try to sing along," she continues. "They shout over it, hoping their voices will drown out the sadness. But the song... it doesn't stop. It never stops. Eventually, all you're left with is the hum of it. Echoing in everything. In everyone."
        
        She pauses, letting the weight of her words settle. "And now... it's louder than ever. The world feels it. Every breath. Every step. The song lingers, and it's not just sad anymore - it's tired."
        
        For a moment, the air feels heavier, as though the melody she speaks of is pressing down, unseen but unmistakable.
        """
    )

    options = (
        {"desc": "What is the world feeling?", "goto": "node_aeum_2_5_1"},
        {"desc": "I've heard enough.", "goto": "node_aeum_2_6"},
    )

    return text, options


def node_aeum_2_5_1(caller):
    text = dedent(
        """
        The woman lowers her gaze.
        
        "The world... it feels as though none of it matters anymore. Like the things we once held so tightly have slipped through our fingers." She pauses, her words hanging in the air like the faintest echo of a fading melody. "And that we're alone now. All of us, trying to listen to a song that barely exists anymore."
        
        She sighs, the weight of it palpable. "It's quiet, you see. So quiet you almost can't hear it at all. But it's there, whispering. And what it says... it's hard to understand. But if you listen close enough, it tells you the truth: the road beneath us is crumbling, little by little. Piece by piece."
        
        Her gaze lifts, as if searching for something beyond the horizon. "And once the road's gone... well, that's the part no one wants to hear."
        """
    )

    options = (
        {
            "desc": "What happens when the music stops?",
            "goto": "node_aeum_2_5_2",
        },
        {"desc": "I've heard enough.", "goto": "node_aeum_2_6"},
    )

    return text, options


def node_aeum_2_5_2(caller):
    text = dedent(
        """
        The woman's fingers pause, the last wisp of smoke fading into nothing. She meets your gaze, her voice low and steady.
        
        "When the music stops... so does Arcellia."
        """
    )

    options = ({"desc": "What do we do?", "goto": "node_aeum_2_6"},)

    return text, options


def node_aeum_2_6(caller):
    caller.msg(
        dedent(
            f"""
            "You go," she says simply. "Prepare for what's coming. The town of Emberlyn lies to the north, just beyond the gate. If you're to do anything, I suggest you start there."
            
            Smoke coils once more around her fingers, twisting in a slow, deliberate spiral. "Goodbye, {caller.display_name}. I have a feeling we'll meet again."
            """
        )
    )

    caller.quests.set_objective(
        "Arrival",
        ArrivalObjective.MEET_AEUM,
        "status",
        QuestProgress.COMPLETED,
    )

    return "", {}


def node_quit(caller):
    return "", {}
