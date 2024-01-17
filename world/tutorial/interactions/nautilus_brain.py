from evennia.utils import dedent


def node_start(caller):
    text = dedent(
        """\
        You stand before a grotesque spectacle. A figure, seated, head cleft open, reveals a pulsating, alien brain, an aberration where human thought should reside. The scene is macabre yet strangely compelling.|/
        """
    )

    options = (
        {"desc": "Attempt an Extraction", "goto": "node_extraction"},
        {"desc": "Communicate with the Brain", "goto": "node_communicate"},
        {"desc": "Destroy the Aberration", "goto": "node_destroy"},
        {"desc": "Leave", "goto": "node_quit"},
    )

    return text, options


def node_extraction(caller, raw_string, **kwargs):
    text = dedent(
        """\
        With steady hands and a heart steeled against the macabre task, you set about the delicate extraction. Guided by intuition more than knowledge, you navigate the complex anatomy.

        The aberration, now free, quivers in gratitude. A telepathic whisper fills your mind, "|CThank you, savior.|n" The entity follows you, its presence eerie but not unwelcome.
        """
    )

    return text, {}


def node_communicate(caller, raw_string, **kwargs):
    text = dedent(
        """\
        You focus, reaching out with words. The air thickens as a telepathic connection forms, the entity's thoughts mingling with yours.

        It shares its plight, a tale of captivity and longing for freedom. Pleading for aid, it promises assistance in your journey should you liberate it.
        """
    )

    options = (
        {"desc": "Attempt an Extraction", "goto": "node_extraction"},
        {"desc": "Destroy the Aberration", "goto": "node_destroy"},
        {"desc": "Leave", "goto": "node_quit"},
    )

    return text, options


def node_destroy(caller, raw_string, **kwargs):
    text = dedent(
        """\
        Determined that this aberration should not exist, you prepare to strike the fatal blow.

        With a swift, decisive action, the entity is no more.
        """
    )

    return text, {}


def node_quit(caller, raw_string, **kwargs):
    return "", ""
