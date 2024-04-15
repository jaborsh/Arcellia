from handlers.rolls import RollHandler

from evennia.utils import dedent
from world.nautilus.quest import NautilusQuest

roll_handler = RollHandler()


def node_start(caller):
    if not (caller.quests.get("Nautilus")):
        caller.quests.add(NautilusQuest)

    caller.ndb._evmenu.quest = caller.quests.get("Nautilus")

    text = dedent(
        """\
        A figure catches your eye - a young enchantress bound by cold iron chains, her presence a stark contrast to the grim surroundings. As she lifts a phantom cigarette to her lips, an action more of habit than need, you notice her eyes are brown and her face is speckled with birthmarks. 
        
        She can't be more than her late twenties. Draped upon her is a silver jumpsuit, cascading down her form like the armor of a queen forged from moonlight and starshine.

        |cThe Enchantress|n says, "Get me out of this cell!"
        """
    )

    options = (
        {"desc": "Are you trapped?", "goto": "node_enchantress_1_1"},
        {"desc": "About that...", "goto": "node_enchantress_2_1"},
        {"desc": "[Leave]", "goto": ""},
    )

    return text, options


def node_enchantress_1_1(caller):
    def _callback(caller):
        caller.msg(
            'The enchantress allows a sliver of solemnity to pierce her erstwhile amused facade. "Because I\'m trapped..." she admits, the words leaving her lips with a weight that seems to draw the very air from the cell. She takes another pull from her ephemeral cigarette, the act now stripped of its previous nonchalance. The faint glimmer of amusement in her eyes fades, replaced by reality.\n'
        )
        return "node_enchantress_hub"

    text = dedent(
        """\
        The enchantress pauses as if the question itself weaves through layers of enchantment to unsettle her thoughts and responds with a tone laden with mild perplexity, "Uh... no?"

        Her reply floats in the air, ironic. Her brows knit together subtly, glancing around the cell that confines her, as though only now considering the reality of her situation. It's clear as the crystalline waters of Arcellia that she is, indeed, trapped; yet her response, drenched in sarcasm, reflects her spirit.
        """
    )

    options = (
        {"desc": "Then why are you here?", "goto": _callback},
        {"desc": "Can you free yourself?", "goto": "node_enchantress_1_2"},
    )

    return text, options


def node_enchantress_1_2(caller):
    def _callback_1(caller):
        caller.msg(
            "This promise reverberates through the cell, carrying with it the weight of committment and the lightness of hope. The enchantress, her gaze still locked with yours, perceives the earnestness.\n\n|CSelect an option:|n"
        )
        return "node_enchantress_hub"

    def _callback_2(caller):
        caller.msg(
            "The enchantress' response is a silent one, yet heavy with meaning. She looks you in the eye, the shadows of her sell seeming to recede for a moment under the weight of her gaze. In that look, there's a mingling of emotions - surprise, perhaps a flicker of amusement, and a depth of gratitude. It's as if your whimsical self-designation strikes a chord within her, resonating with the threads of fate binding you to this singular moment.\n\nShe shows a spark reignited by the unexpected gift of laughter in the midst of darkness. For what are heroes, if not saviors in their own right?\n\n|CSelect an option:|n"
        )
        return "node_enchantress_hub"

    text = dedent(
        """\
        The enchantress, in response, shakes her head slowly, a gesture heavy with resignation and unspoken attempts marred by failure. No words are needed to convey the depth of her plight, for her actions speak volumes of a battle waged against her bindings - a battle that, for now, she cannot win alone.
        """
    )

    options = (
        {"desc": "I'll help you.", "goto": _callback_1},
        {"desc": "Savior is my name.", "goto": _callback_2},
    )

    return text, options


def node_enchantress_2_1(caller):
    text = dedent(
        """\
        The enchantress' eyes narrow, a glimmer of interest lighting up her face amid the dimness of the cell. "Go on," she urges, a hint of impatience threading her voice, like a swift current beneath a calm surface.
        """
    )

    options = (
        {"desc": "What do I get out of saving you?", "goto": "node_enchantress_2_2"},
    )
    return text, options


def node_enchantress_2_2(caller):
    def _callback(caller):
        if roll_handler.check("1d20", dc=10, stat=caller.charisma):
            caller.msg(
                '|g[Charisma Success]|n\n\n"No." Her response is immediate, a single word punctuated by the drawing of silvery smoke. The phantom cigarette, seemingly forgotten, now serves as a consuit for her assurance, a visual testament to her promise. The smoke curls and dances in the dim light of her cell. Her eyes betray no deception.\n\n'
            )
            return "node_enchantress_hub_1_1"
        else:
            caller.msg("|r[Charisma Failure]|n\n")
            return "node_enchantress_hub_1_1"

    text = dedent(
        """\
        Her response is both simple and a challenge: "Unless you're heartless, you will help." This retort gives a pause. No promises of treasure or power, no tales of secret knowledge or alliances. Instead, she appeals to something more intrinsic: a potential compassion she perceives - or hopes to perceive - within you.

        A silence settles, thick as the cold air of the cell. Her brown eyes watch you. In them, you glimpse not just the fate of this enchantress, but a reflection of your own soul, standing at the crossroads between empathy and indifference.
        """
    )

    options = ({"desc": "Will you betray me?", "goto": _callback},)

    return text, options


def node_enchantress_hub(caller):
    text = ""

    options = {
        "desc": "How long have you been here?",
        "goto": "node_enchantress_hub_1_1",
    }

    return text, options


def node_enchantress_hub_1_1(caller):
    def _callback(caller):
        text = "|#C7C10CShe's right. Something wants to come out -- through your mouth. But you can keep it down because your body does not control you.|n\n\n"

        if roll_handler.check("1d20", dc=10, stat=caller.constitution):
            caller.quests.add_details("Nautilus", {"enchantress_vomit": False})
            text += dedent(
                """\
            |g[Constitution Success]|n

            Drawing upon a well of inner constitution, you focus on steadying your breath and calming the tumultuous sensation rolling within. You remind yourself firmly that your body does not control you - you control it. With a deep inhalation that carries the brine of the sea mingled with the aged wood of the boat, you steady your stance. Slowly, the urge recedes, like a wave withdrawing from the shore.
            """
            )
        else:
            caller.quests.add_details("Nautilus", {"enchantress_vomit": True})
            text += dedent(
                """\
                |r[Constitution Failure]|n

                Despite your best efforts to quell the violent uprising within, the revolt proves too potent to suppress. It's a moment of visceral surrender as your body rebels, forcing you to acquiesce to its demands. It makes you put your hand to your mouth and swallow. The experience, as brief as it is chaotic, leaves you feeling vulnerable, yet cleansed in some ineffable way.
                """
            )

        caller.msg(text)

        return "node_enchantress_vomit"

    text = dedent(
        """\
        The enchantress' gaze intensifies, a sudden shift from the veiled mixture of hope and resilience to a clear, unadulterated concern. "Are you all right?" she asks instead.
        """
    )

    options = {"desc": "Continue.", "goto": _callback}

    return text, options


def node_enchantress_vomit(caller):
    if caller.quests.get_detail("Nautilus", "enchantress_vomit"):
        text = dedent(
            """\
            Her concern deepening at the sight of your distress, she watches you closely. "Friend?", she begins, the uncertainty in her voice clear as she braces for what might come next.
            """
        )

    else:
        text = dedent(
            """
            Nothing your struggle to maintain composure, the enchantress' expression shifts to one of solemn understanding. 
            """
        )

    options = {
        "desc": "What are we doing on this ship?",
        "goto": "node_enchantress_hub_1_2",
    }

    return text, options


def node_enchantress_hub_1_2(caller):
    text = dedent(
        """\
        The enchantress meets your question with a thoughtful pause, her gaze drifting momentarily throughout the shadowed confines of her cell, as if the answer might be found in the murkiness that surrounds her. "I couldn't say," she admits, her voice reflecting a mixture of puzzlement and resignation. "In truth... so far, the sailors have sailed and drank. I can't say I've seen you before."

        Her response, candid and tinged with uncertainty, mirrors the enigma that wraps itself around the vessel's purpose and your presence upon it. It's a revelation that, while not illuminating, confirms the oddity of your situation. You're both adrift in a sea of questions with few answers in sight, navigating through the unknown with nothing.
        """
    )

    if roll_handler.check("1d20", dc=11, stat=caller.intelligence):
        text += "\n|CYou have no doubt about the drinking, but do you strike yourself as a tight-lipped drunk? Surely, in an atmopshere loosened by drink, words must have flowed as freely as the spirits themselves. She must have heard something: a slip of the tongue, a whispered rumor, or even a shouted declaration."

    options = {"desc": "[TEMP] Continue.", "goto": "node_enchantress_intro"}

    return text, options


# Post-Freedom
def node_enchantress_intro(caller):
    def _callback1(caller):
        caller.msg(
            'The enchantress regards you with a look that is both apologetic and discerning, as if assessing the weight of her next words before they breach her lips. "I didn\'t mean to overwhelm you with information," she finally says, her voice soft yet firm, like a gentle tide caressing the shore but persistent enough to shape the land over time. "You seem a bit... lost.\n"'
        )
        return "node_enchantress_intro"

    if not caller.quests.get_detail("Nautilus", "enchantress_freed"):
        caller.quests.add_details("Nautilus", {"enchantress_freed": True})
        text = dedent(
            """
            The air between you thickens with your assertion, a flicker of resolve igniting within you despite the sea of uncertainty you're adrift in. The words spill from your lips. The enchantress, still as a statue, regards you with a newfound intensity. Her eyes, previously clouded with resignation, now shimmer with a glint of something akin to respect.

            She leans closer, her voice lowering to a conspiratorial whisper. "There are demons here," she confides, her gaze locking onto yours. "One of the sailors has been performing rituals for a week now. The others thought nothing of it and ignored him." Her words hang in the air, heavy with implication.

            The enchantress watches you, her expression somber yet laced with a subtle urging. It's clear she believes your arrival is no mere twist of fate. Silence stretches between you, broken only by the distant, mournful cry of the sea.
            """
        )

        if roll_handler.check("1d20", dc=11, stat=caller.charisma):
            text += (
                "\n|mShe speaks matter-of-factly, but there's a sadness in her voice.|n"
            )
    else:
        text = ""

    options = [
        {
            "desc": "And why didn't you just tell me about the rituals?",
            "goto": _callback1,
        },
        {
            "desc": "I don't remember anything that's happened on the ship.",
            "goto": "node_enchantress_intro_1_1",
        },
    ]

    if roll_handler.check("1d20", dc=14, stat=caller.charisma):
        options.append(
            {
                "desc": "|m[Let her know you want her. Physically.]|n",
                "goto": "node_enchantress_intro_2_1",
            }
        )

    options.append(
        {"desc": "I should get going now. [Leave]", "goto": "node_quit"},
    )

    return text, options


def node_enchantress_intro_1_1(caller):
    def _callback1(caller):
        caller.msg(
            'The atmosphere shifts subtly, tension threading through the air like a whisper on the wind. Your affirmation, succinct and ripe with an underturrent of determination, meets her ear, sparking an ambiguous response.\n\n"Is it?" The enchantress responds, her eyebrow arched in a gesture that mingles skepticism with intrigue. The cigarette perched between her fingers sizzles, a faint sound that nevertheless slices through the tension. The crackle of burning tobacco seems to punctuate her doubt.'
        )

        if roll_handler.check("1d20", dc=10, stat=caller.charisma):
            caller.msg(
                "\n|mShe looks tired, her beauty waning faster than it ought to at her age.|n"
            )

        return "node_enchantress_intro"

    def _callback2(caller):
        caller.msg(
            'The journey through understanding one\'s place on a ship haunted by shadows and secrets is nothing if not a labyrinth of choices and revelations.\n\n"Have you been drinking?" The enchantress counters, a flicker of amusement - perhaps disbelief - dancing behind her eyes. The sizzle of her cigarette once again punctuates the moment, a familiar yet dissonant backdrop to the unfolding discourse.\n'
        )

        return "node_enchantress_intro"

    text = dedent(
        """\
        The enchantress meets your gaze once more, her eyes reflecting a depth of understanding that transcends mere empathy. "I can see that," she responds, her tone devoid of judgment, steeped instead in a quiet acknowledgement of your shared plight. Her affirmation is a gentle touch upon a wound.

        With her response, the enchantress implicitly invites you to accept the void within, not as an abyss to be feared, but as a canvas yet to be filled. 
        """
    )

    options = (
        {"desc": "Good.", "goto": _callback1},
        {"desc": "Do you know why?", "goto": _callback2},
    )

    return text, options


def node_enchantress_intro_2_1(caller):
    def _callback_success(caller):
        caller.msg(
            '|#9B1B30Perched on the precipice of the unknown, where the veil between life and shadow grows thin, your thoughts, sparked by desperation and the surreal calm of impending doom, spill forth unguarded.\n\nThe enchantress, her presence a constant amidst the chaos, regards you with a depth of understanding. "You seek comfort," she acknowledges, her voice soft, carrying the warmth of empathy as a balm to the soul. "It\'s only natural."|n\n'
        )
        return "node_enchantress_intro"

    if roll_handler.check("1d20", dc=14, stat=caller.charisma):
        text = dedent(
            """\
            |g[Charisma Success]|n

            |#9B1B30"Why are you doing this?" The enchantress' question pierces the heavy air, her words sharp, yet not devoid of curiosity. Her gaze seeks not just an answer but an understanding of the motives that drive you, here, in the confines of a ship cloaked in shadow. Not to mention the dead bodies.|n
            """
        )

        options = (
            {
                "desc": "We're at death's door. And still... Does the longing ever stop?",
                "goto": _callback_success,
            },
        )
    else:
        text = dedent(
            """\
            |r[Charisma Failure]|n

            |#9B1B30The words have already left your mouth, a decision made, actions set into motion like dominos cascading towards inevitable conclusions. Yet, as they hang suspended in the time between speaking and hearing, there's a palpable tension.|n
            """
        )

        options = {
            "desc": "I want to have fuck with you.",
            "goto": "node_enchantress_seduce_failure_1",
        }

    return text, options


def node_enchantress_seduce_failure_1(caller):
    def _callback(caller):
        caller.msg(
            "|#9B1B30Her eyes sparkle with unrestrained hilarity. \"No... That's not what you said. You said...\" Her words teeter on the edge of cohesion, but she's unable to finish, the waves of laughter rolling over her once more, consuming her in their jovial tide.|n\n"
        )
        return "node_enchantress_seduce_failure_2"

    text = dedent(
        """\
        |#9B1B30She erupts in laughter, a melodic sound that seems to wash away the shadow of melancholy that had settled upon her features. The fatigue that once painted her expression is swept aside, replaced by amusement and a flicker of light-heartedness rare in such dire straits.|n
        """
    )

    options = (
        {"desc": "I said I want to have sex with you.", "goto": _callback},
        {"desc": "Nevermind.", "goto": "node_enchantress_seduce_failure_2"},
    )

    return text, options


def node_enchantress_seduce_failure_2(caller):
    text = dedent(
        """\
        |#9B1B30With the enchantress' laughter echoes in the air like a melody. "Pretty please. One more time..." she implores, her request wrapped in lingering amusement.|n
        """
    )

    options = [
        {
            "desc": "Find someone else to laugh at.",
            "goto": "node_enchantress_seduce_failure_3",
        },
    ]

    if roll_handler.check("1d20", dc=11, stat=caller.charisma):
        options.append(
            {
                "desc": "|xCan't back down now. Say what you said again. Proudly.",
                "goto": "node_enchantress_seduce_authority",
            }
        )

    return text, options


def node_enchantress_seduce_failure_3(caller):
    text = dedent(
        """\
        |#9B1B30The laughter that had lit up her face like a beacon in the night fades as she understands the impact of her mirth. "I'm sorry," she responds, her tone earnest, devoid of the wit that had pervaded moments before. She puts out her ephemeral cigarette, an uncharacteristically gentle act.|n
        """
    )

    options = ()

    return text, options


def node_enchantress_seduce_authority(caller):
    text = dedent(
        """\
        In an outburst fueled by a mix of vexation, desperation, and perhaps the surreal nature of your circumstances, you escalate the exchange. |#9B1B30"I said I want to have fuck with you!"|n The words burst forth, unfiltered and raw, defiance mingling.

        Taken aback by the intensity and the choice of words, the enchantress finds herself caught between shock and amusement. |#9B1B30"You're god damn right you did,"|n she manages to say, tears of laughter reemerging stronger than before. "What kind of person even are you?" she wonders aloud.
        """
    )

    options = (
        {
            "desc": "The Bringer of the Apocalypse.",
            "goto": "node_enchantress_seduce_apocalypse",
        },
        {
            "desc": "A Superstar. I can no longer deny it.",
            "goto": "node_enchantress_seduce_superstar",
        },
        {
            "desc": "I'm sorry. I don't know. You're pretty. I'm sorry.",
            "goto": "node_enchantress_seduce_sorry",
        },
    )

    return text, options


def node_enchantress_seduce_apocalypse(caller):
    def _apocalypse1(caller):
        caller.msg(
            'Under the dim, flickering light, the dialogue between the two of you traces the path of a peculiar dance - each step, a word; each turn, an exchanged glance. The air is thick with the scent of impending doom and the lingering trace of her cigarette smoke.\n\n|r"Mere minutes? I should go prepare then. Thank you, this has been delightful,"|n she responds, her composure unshaken. With a grace that seems out of place in the face of oblivion, she extinguishes her cigarette, the glow at its tip fading like the last light before darkness. Then, without further ado, she disappears.'
        )
        return "node_quit"

    def _apocalypse2(caller):
        caller.msg(
            'Under the dim, flickering light, the dialogue between the two of you traces the path of a peculiar dance - each step, a word; each turn, an exchanged glance. The air is thick with the scent of impending doom and the lingering trace of her cigarette smoke.\n\n|r"All right, then. Looks like I should go prepare. And thank you, this has been delightful,"|n she replies, her tone laced with serenity. With a final glance that seems to capture the essence of your shared moment, she extinguishes her cigarette and vanishes, leaving behind a silence and the seas.'
        )
        return "node_quit"

    text = dedent(
        """\
        Amidst the cryptic ambiance of the Nautilus, each word spoken acts as a pebble tossed into the still waters of the unknown.

        |r"Has the time come already?" the enchantress replies, her voice a blend of curiosity and sarcasm, as if the notion of the apocalypse is a familiar fate yet she seeks confirmation of its arrival.|n
        """
    )

    options = (
        {
            "desc": "We are mere minutes away from the total collapse of reality.",
            "goto": _apocalypse1,
        },
        {
            "desc": "The end can't be more than three days away.",
            "goto": _apocalypse2,
        },
        {
            "desc": "We've still some years to go.",
            "goto": _apocalypse2,
        },
    )

    return text, options


def node_enchantress_seduce_superstar(caller):
    def _superstar(caller):
        caller.msg(
            '|#FFD700"I have certainly been entertained. Thank you. Whatever you are, you should stick to it,"|n she replies, her words wrapping around you like a cloak. As she extinguishes her phantom cigarette, the finality of the act seems to punctuate her departure, her form melding with the enveloping shadows as she fades from your presence.'
        )

        return "node_quit"

    text = dedent(
        """\
        Amidst the cryptic ambiance of the Nautilus, each word spoken acts as a pebble tossed into the still waters of the unknown.

        |#FFD700"Okay, that's cool. Can I maybe ask you to elaborate on your superstardom a tiny bit?" the enchantress inquires, her words tinged with a mirthful curiosity.|n
        """
    )

    options = (
        {"desc": "It means I'm a bloated drunk.", "goto": _superstar},
        {
            "desc": "I'm the hero of this story. It's a theory I'm developing",
            "goto": _superstar,
        },
    )

    return text, options


def node_enchantress_seduce_sorry(caller):
    text = dedent(
        """\
        Amidst the cryptic ambiance of the Nautilus, each word spoken acts as a pebble tossed into the still waters of the unknown.

        |#A9CCE3You stammer, the confession spilling from you in a torrent of emotion, a tangled skein of apology, admiration, and the all-encompassing confusion that defines your odyssey.

        "Don't be. It was funny," she reassures, her response soothing.|n
        """
    )

    if roll_handler.check("1d20", dc=11, stat=caller.wisdom):
        text += "\n\n|CShe appears to genuinely want you to understand it's okay.|n"

    text += '\n"|#A9CCE3There are other things in life -- more meaningful, more fitting for you. This..." She gestures towards herself, draped in silver, "Is not one of them."|n\n\n As she extinguishes her cigarette, the glow at its tip fading like the last light before darkness, she disappears.'

    options = {"desc": "[Leave]", "goto": "node_quit"}

    return text, options


def node_quit(caller):
    return "", {}
