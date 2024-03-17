from evennia.utils import dedent

from world.characters import backgrounds, genders, races
from world.xyzgrid.xyzroom import XYZRoom

_BACKGROUND_INFO_DICT = backgrounds.BACKGROUND_INFO_DICT

_GENDER_INFO_DICT = genders.GENDER_INFO_DICT

_RACE_INFO_DICT = races.RACE_INFO_DICT

_SUBRACE_INFO_DICT = races.SUBRACE_INFO_DICT


def chargen_welcome(caller):
    def _set_screenreader(caller):
        for session in caller.account.sessions.all():
            session.protocol_flags["SCREENREADER"] = True
            session.update_flags(screenreader=True)
        return "chargen_gender"

    text = dedent(
        """\
        Enveloped in a cocoon of primordial blackness, warmth wraps around the tiny essence of being, a lone conscience no more significant than a grain of malt in an endless expanse of darkness. It floats in this tranquil void, beyond the realms of obligation, where time and duty dissolve into an eternal, serene abyss. Thought and action meld into the nothingness; here one finds peace in the still, comforting promise of an existence unburdened by the need to do, to be, to strive - forevermore in an endless canvas of never ever.

        |CDo you use a screenreader?|n
        """
    )

    options = (
        {"key": "", "goto": "chargen_welcome"},
        {"key": ("y", "yes"), "desc": "Enable Screenreader", "goto": _set_screenreader},
        {"key": ("n", "no"), "desc": " Disable Screenreader", "goto": "chargen_gender"},
        {"key": "_default", "goto": "chargen_welcome"},
    )

    return text, options


def chargen_gender(caller, raw_string, **kwargs):
    def _set_gender(caller):
        selected_gender = kwargs.get("selected_gender", None)
        if selected_gender == "male":
            caller.traits.add(
                "gender",
                "Gender",
                value=genders.Gender.MALE,
            )
        elif selected_gender == "female":
            caller.traits.add("gender", "Gender", value=genders.Gender.FEMALE)
        elif selected_gender == "androgynous":
            caller.traits.add("gender", "Gender", value=genders.Gender.ANDROGYNOUS)
        else:
            return "chargen_welcome"

        return "chargen_race"

    if selected_gender := kwargs.get("selected_gender", None):
        text = _GENDER_INFO_DICT[selected_gender] + "\n\n|CConfirm your Gender|n:"
        options = (
            {"key": "", "goto": "chargen_welcome"},
            {
                "key": ("y", "yes"),
                "desc": f"Confirm {selected_gender.capitalize()}",
                "goto": (_set_gender, {"selected_gender": selected_gender}),
            },
            {
                "key": ("n", "no"),
                "desc": "Return to Gender Selection",
                "goto": ("chargen_gender", {"selected_gender": None}),
            },
        )

    else:
        text = dedent(
            """\
            As immeasurable time drifts by, untouched by the suffocating grasp of struggle, existence remains unfathomably tranquil. But in the midst of this hushed eternity, a whisper of consciousness begins to stir. Somewhere just beyond perception, shrouded in the unseen recesses of this void, a presence makes itself known. It festers, submerged in a vile, caustic broth that seeps into the edges of awareness. This entity envelops the serene conscience, injecting a sense of disquiet into the calm that once reigned.

            All at once, as if gasping for breath from beneath an ocean of nothingness, there is light and form upon the horizon. The chance to become, to be, to exist, dwells solely within your heart.

            |CSelect your Gender|n:
            """
        )  # noqa: E501

        options = (
            {"key": "", "goto": "chargen_welcome"},
            {
                "key": ("1", "male", "m"),
                "desc": "Male",
                "goto": ("chargen_gender", {"selected_gender": "male"}),
            },
            {
                "key": ("2", "female", "f"),
                "desc": "Female",
                "goto": ("chargen_gender", {"selected_gender": "female"}),
            },
            {
                "key": ("3", "androgynous", "a"),
                "desc": "Androgynous",
                "goto": ("chargen_gender", {"selected_gender": "androgynous"}),
            },
            {"key": "_default", "goto": "chargen_gender"},
        )

    return text, options


def chargen_race(caller, raw_string, **kwargs):
    def _set_race(caller, **kwargs):
        race = kwargs.get("selected_race", None)
        subrace = kwargs.get("selected_subrace", None)

        if not race:
            caller.msg("An error occurred. Contact an administrator.")
            return "chargen_welcome"

        if subrace:
            race_type = f"{subrace} {race}"
        else:
            race_type = f"{race}"

        race_type = races.RaceRegistry.get(race_type)

        if not race_type:
            caller.msg("An error occurred. Contact an administrator.")
            return "chargen_welcome"

        caller.traits.add("race", "Race", value=race_type)
        return "chargen_background"

    selected_race = kwargs.get("selected_race", None)
    selected_subrace = kwargs.get("selected_subrace", "")

    if selected_subrace:
        text = _SUBRACE_INFO_DICT[selected_race][selected_subrace] + "\n"
    elif selected_race:
        text = _RACE_INFO_DICT[selected_race] + "\n"
    else:
        text = dedent(
            """
            A notion unfurls within the stillness, one you might rather remain oblivious to. Consider the reason behind this self-imposed exile into nothingness. Perhaps there's a part of you, marinated in the excesses of your own actions, that recoils from such revelations. In eagerness, perhaps, you deluged yourself in oblivion, tipping the balance beyond a simple seasoning to a state of overwhelming saturation.

            Imagine, if you dare, a colossal sphere where malevolence brews. On this orb, simian creatures of nefarious intent wage an incessant war, a tableau of chaos underpinned by brutality. You are among them - no mere observer, but an active participant. This sphere is your arena, your world; the others, your kindred and adversaries.

            They clash with savage fervor over scraps and dominance, a dance as old as time itself, couched in a rhetoric that seems all too familiar - a hollow phrase adopted from the ether to give a shade of meaning to the struggle. Take with you the grim axiom from this metaphorical panorama: in the contest for survival amongst your own, it is conquer or be conquered, to prevail in might or be reduced to insignificance.

            |CSelect your Race|n:
            """  # noqa: E501
        )

    if not selected_race:
        options = []
        i = 0
        for race in _RACE_INFO_DICT.keys():
            i += 1
            options.append(
                {
                    "key": (str(i), race),
                    "desc": race.capitalize(),
                    "goto": ("chargen_race", {"selected_race": race}),
                }
            )

    elif (
        selected_race
        and not selected_subrace
        and _SUBRACE_INFO_DICT.get(selected_race, None)
    ):
        text += "\n|CSelect your Subrace|n:\n"
        options = []
        i = 0
        for subrace in _SUBRACE_INFO_DICT[selected_race].keys():
            i += 1
            options.append(
                {
                    "key": (str(i), subrace),
                    "desc": subrace.capitalize(),
                    "goto": (
                        "chargen_race",
                        {"selected_race": selected_race, "selected_subrace": subrace},
                    ),
                }
            )

    elif (selected_race and selected_subrace) or (
        selected_race and not _SUBRACE_INFO_DICT.get(selected_race, None)
    ):
        text += "\n|CConfirm your Race|n:\n"
        options = (
            {
                "key": "y",
                "desc": f"Confirm {selected_subrace} {selected_race}",
                "goto": (
                    _set_race,
                    {
                        "selected_race": selected_race,
                        "selected_subrace": selected_subrace,
                    },
                ),
            },
            {
                "key": "n",
                "desc": "Return",
                "goto": ("chargen_race", {"selected_race": None}),
            },
        )

    return text, options


def chargen_background(caller, raw_string, **kwargs):
    def _set_background(caller, **kwargs):
        background = kwargs.get("selected_background", None)
        background = backgrounds.BackgroundRegistry.get(background)

        if not background:
            caller.msg("An error occurred. Contact an administrator.")
            return "chargen_welcome"

        caller.traits.add("background", "Background", value=background)
        return "chargen_appearance"

    selected_background = kwargs.get("selected_background", None)
    if selected_background:
        text = (
            _BACKGROUND_INFO_DICT[selected_background]
            + "\n\n|CConfirm your Background|n:"
        )
        options = (
            {
                "key": "y",
                "desc": f"Confirm {selected_background}",
                "goto": (_set_background, {"selected_background": selected_background}),
            },
            {
                "key": "n",
                "desc": "Return",
                "goto": ("chargen_background", {"selected_background": None}),
            },
        )

    else:
        text = dedent(
            """
            Drawn inexorably as if fated, your awareness adheres to a most disquieting realization, much like the unfortunate insect ensnared by a viscous trap. The fleshly construct you inhabit, a machine wrought of limbs, burdened with the intrinsic nature of life begins its laborious reawakening. This vessel, animated by a tumultuous spirit, yearns for the expanse of a world where purpose is the currency of existence, where desire is ever-present.

            Suddenly, a searing lance of light pierces the tranquility that shrouds your mind, an invasive force intent on prying your eyes from their restful closure. Accompanying this intrusion is a sound, a sonorous peal that resonates with the very essence of perdition. It heralds an awakening, a clarion so powerful, it is as if the very gates of hell themselves were orchestrating your return to the waking world.

            |CSelect your Background|n:
            """
        )

        options = []
        i = 0
        for background in _BACKGROUND_INFO_DICT.keys():
            i += 1
            options.append(
                {
                    "key": (str(i), background),
                    "desc": background.capitalize(),
                    "goto": ("chargen_background", {"selected_background": background}),
                }
            )

    return text, options


def chargen_appearance(caller, raw_string, **kwargs):
    text = dedent(
        """
        Suspended above a basin twisted and marred by neglect, a mirror holds court. From the damaged faucet, a jet of scalding water erupts, casting a shroud of steam across the glass, obscuring clarity. There, in the fogged reflection, only the barest hint of a figure can be discerned, a specter of self without detail or form. A startling epiphany cascades over you in that ill-defined moment; your own visage is a mystery, lost beneath the gentle veil of mist.

        |CSelect an Appearance Option|n:
        """
    )

    options = (
        {"key": "", "goto": "chargen_appearance"},
        {
            "key": ("1", "detailed", "d"),
            "desc": "Create a Customized Description",
            "goto": "chargen_appearance_detailed",
        },
        {
            "key": ("2", "template", "t"),
            "desc": "Select Template Descriptors",
            "goto": "chargen_appearance_template",
        },
        {"key": "_default", "goto": "chargen_appearance"},
    )

    return text, options


def chargen_appearance_detailed(caller, raw_string, **kwargs):
    def _set_appearance(caller, raw_string, **kwargs):
        caller.db.desc = raw_string.strip()
        return ("chargen_appearance_detailed", {"appearance": caller.db.desc})

    if appearance := kwargs.get("appearance", None):
        text = f"\n{appearance}\n\n|CConfirm your Appearance|n:"
        options = (
            {"key": "y", "desc": "Confirm Appearance", "goto": "chargen_finalize"},
            {
                "key": "n",
                "desc": "Return",
                "goto": ("chargen_appearance_detailed", {"appearance": None}),
            },
        )
    else:
        text = dedent(
            """
            The time has come: a defining instant that invites no delay, and fosters no escape. What lies beyond that soft and swirling vapor is a truth that must be faced. With a breath that is both anticipatory and anxious, the facade you're about to unveil comes with the peril of true self-revelation. Therein lies the precipice of identity - you stand poised to meet the eyes of the being you inhabit, to witness the countenance that is undeniably yours, irrespective of reverberations they might cause within the core of who you are.

            |CWrite your Description|n:
            """
        )
        options = (
            {"key": "", "goto": "chargen_appearance_detailed"},
            {"key": "_default", "goto": _set_appearance},
        )

    return text, options


def chargen_appearance_template(caller, raw_string, **kwargs):
    def _set_appearance(caller, **kwargs):
        desc = dedent(
            """
            {identity}, standing with {height} stature, embodies the life they've lived through the form of their {body} physique. Their {skin} skin, a canvas of their heritage, captures and plays with the light, be it the golden touch of the sun or the moon's soft glow. {eye_type} eyes, rich in {eye_color}, reveal the depths of their experiences. Hair, in varying shades of {hair_color}, crowns their head, a well-proportioned {nose} nose finds harmony with a {mouth} mouth, together sketching the visage of character.
            """.format(
                identity=(
                    f"{caller.race.value.race} {caller.gender.value.value}"
                    if caller.gender.value.value != "androgynous"
                    else f"{caller.gender.value.value} {caller.race.value.race}"
                ),
                height=kwargs.get("height"),
                body=kwargs.get("body"),
                skin=kwargs.get("skin_type"),
                eye_type=kwargs.get("eye_type").capitalize(),
                eye_color=kwargs.get("eye_color"),
                hair_color=kwargs.get("hair_color"),
                nose=kwargs.get("nose_type"),
                mouth=kwargs.get("mouth_type"),
            ).lstrip()
        )

        desc = (
            "A " + desc
            if desc[0].lower() not in ["a", "e", "i", "o", "u"]
            else "An " + desc
        )

        caller.db.desc = desc.strip()
        return "chargen_finalize"

    text = dedent(
        """
        A figure stares back from the other side of the obscured mirror, its features hidden beneath the mist's caress. It exists there as an enigma, a stranger composed of familiar lines and curves, yet wholly unrecognizable. A shiver of alienation creeps along your spine - the realization dawns upon you that the entity reflected in the glass, this 'thing' that should be as known to you as the very beat of your heart, remains anonymous. It is as if you are gazing upon an intimate unknown, a specter of self that is both intimately close and unsettlingly foreign.

        |CSelect an Appearance Option|n:
        """
    )

    height = kwargs.get("height", "")
    body = kwargs.get("body", "")
    eye_color = kwargs.get("eye_color", "")
    hair_color = kwargs.get("hair_color", "")
    skin_type = kwargs.get("skin_type", "")
    eye_type = kwargs.get("eye_type", "")
    nose_type = kwargs.get("nose_type", "")
    mouth_type = kwargs.get("mouth_type", "")

    options = (
        {"key": "", "goto": "chargen_appearance"},
        {
            "key": ("1", "height"),
            "desc": f"Height ({height})",
            "goto": ("appearance_height", kwargs),
        },
        {
            "key": ("2", "body", "body type"),
            "desc": f"Body Type ({body})",
            "goto": ("appearance_body", kwargs),
        },
        {
            "key": ("3", "eye color", "ec"),
            "desc": f"Eye Color ({eye_color})",
            "goto": ("appearance_eye_color", kwargs),
        },
        {
            "key": ("4", "hair color", "hc"),
            "desc": f"Hair Color ({hair_color})",
            "goto": ("appearance_hair_color", kwargs),
        },
        {
            "key": ("5", "skin type", "st"),
            "desc": f"Skin Type ({skin_type})",
            "goto": ("appearance_skin_type", kwargs),
        },
        {
            "key": ("6", "eye type", "et"),
            "desc": f"Eye Type ({eye_type})",
            "goto": ("appearance_eye_type", kwargs),
        },
        {
            "key": ("7", "nose type", "nt"),
            "desc": f"Nose Type ({nose_type})",
            "goto": ("appearance_nose_type", kwargs),
        },
        {
            "key": ("8", "mouth type", "mt"),
            "desc": f"Mouth Type ({mouth_type})",
            "goto": ("appearance_mouth_type", kwargs),
        },
    )

    if len(kwargs) == 9:
        options += (
            {
                "key": ("9", "f", "finalize"),
                "desc": "|CFinalize Appearance|n",
                "goto": (_set_appearance, kwargs),
            },
        )

    return text, options


def appearance_height(caller, raw_string, **kwargs):
    text = "|CSelect your Height|n:\n"
    options = (
        {"key": "", "goto": "appearance_height"},
        {
            "key": ("1", "short", "sh"),
            "desc": "Short",
            "goto": ("chargen_appearance_template", kwargs | {"height": "short"}),
        },
        {
            "key": ("2", "average", "av"),
            "desc": "Average",
            "goto": ("chargen_appearance_template", kwargs | {"height": "average"}),
        },
        {
            "key": ("3", "tall", "t"),
            "desc": "Tall",
            "goto": ("chargen_appearance_template", kwargs | {"height": "tall"}),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def appearance_body(caller, raw_string, **kwargs):
    text = "|CSelect your Body Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_body"},
        {
            "key": ("1", "petite", "p"),
            "desc": "Petite",
            "goto": ("chargen_appearance_template", kwargs | {"body": "petite"}),
        },
        {
            "key": ("2", "slender", "s"),
            "desc": "Slender",
            "goto": ("chargen_appearance_template", kwargs | {"body": "slender"}),
        },
        {
            "key": ("3", "average", "av"),
            "desc": "Average",
            "goto": ("chargen_appearance_template", kwargs | {"body": "average"}),
        },
        {
            "key": ("4", "athletic", "at"),
            "desc": "Athletic",
            "goto": ("chargen_appearance_template", kwargs | {"body": "athletic"}),
        },
        {
            "key": ("5", "robust", "r"),
            "desc": "Robust",
            "goto": ("chargen_appearance_template", kwargs | {"body": "robust"}),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def appearance_eye_color(caller, raw_string, **kwargs):
    text = "|CSelect your Eye Color|n:\n"
    options = (
        {"key": "", "goto": "appearance_eye_color"},
        {
            "key": ("1", "amber", "a"),
            "desc": "Amber",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "amber"}),
        },
        {
            "key": ("2", "blue", "b"),
            "desc": "Blue",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "blue"}),
        },
        {
            "key": ("3", "brown", "br"),
            "desc": "Brown",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "brown"}),
        },
        {
            "key": ("4", "green", "g"),
            "desc": "Green",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "green"}),
        },
        {
            "key": ("5", "grey", "gr"),
            "desc": "Grey",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "grey"}),
        },
        {
            "key": ("6", "hazel", "h"),
            "desc": "Hazel",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "hazel"}),
        },
        {
            "key": ("7", "black", "bl"),
            "desc": "Black",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "black"}),
        },
        {
            "key": ("8", "copper", "c"),
            "desc": "Copper",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "copper"}),
        },
        {
            "key": ("9", "crimson", "cr"),
            "desc": "Crimson",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "crimson"}),
        },
        {
            "key": ("10", "emerald", "e"),
            "desc": "Emerald",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "emerald"}),
        },
        {
            "key": ("11", "gold", "go"),
            "desc": "Gold",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "gold"}),
        },
        {
            "key": ("12", "opal", "o"),
            "desc": "Opal",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "opal"}),
        },
        {
            "key": ("13", "onyx", "on"),
            "desc": "Onyx",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "onyx"}),
        },
        {
            "key": ("14", "red", "r"),
            "desc": "Red",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "red"}),
        },
        {
            "key": ("15", "sapphire", "sa"),
            "desc": "Sapphire",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "sapphire"}),
        },
        {
            "key": ("16", "silver", "si"),
            "desc": "Silver",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "silver"}),
        },
        {
            "key": ("17", "violet", "v"),
            "desc": "Violet",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "violet"}),
        },
        {
            "key": ("18", "white", "w"),
            "desc": "White",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "white"}),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def appearance_hair_color(caller, raw_string, **kwargs):
    text = "|CSelect your Hair Color|n:\n"
    options = (
        {"key": "", "goto": "appearance_hair_color"},
        {
            "key": ("1", "auburn", "a"),
            "desc": "Auburn",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "auburn"}),
        },
        {
            "key": ("2", "black", "bl"),
            "desc": "Black",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "black"}),
        },
        {
            "key": ("3", "blonde", "b"),
            "desc": "Blonde",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "blonde"}),
        },
        {
            "key": ("4", "brown", "br"),
            "desc": "Brown",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "brown"}),
        },
        {
            "key": ("5", "grey", "gr"),
            "desc": "Grey",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "grey"}),
        },
        {
            "key": ("6", "red", "r"),
            "desc": "Red",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "red"}),
        },
        {
            "key": ("7", "white", "w"),
            "desc": "White",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "white"}),
        },
        {
            "key": ("8", "blue", "bl"),
            "desc": "Blue",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "blue"}),
        },
        {
            "key": ("9", "green", "g"),
            "desc": "Green",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "green"}),
        },
        {
            "key": ("10", "pink", "p"),
            "desc": "Pink",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "pink"}),
        },
        {
            "key": ("11", "purple", "pu"),
            "desc": "Purple",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "purple"}),
        },
        {
            "key": ("12", "silver", "si"),
            "desc": "Silver",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "silver"}),
        },
        {
            "key": ("13", "teal", "t"),
            "desc": "Teal",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "teal"}),
        },
        {
            "key": ("14", "yellow", "y"),
            "desc": "Yellow",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "yellow"}),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def appearance_skin_type(caller, raw_string, **kwargs):
    text = "|CSelect your Skin Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_skin_type"},
        {
            "key": ("1", "freckled", "f"),
            "desc": "Freckled",
            "goto": ("chargen_appearance_template", kwargs | {"skin_type": "freckled"}),
        },
        {
            "key": ("2", "scarred", "sc"),
            "desc": "Scarred",
            "goto": ("chargen_appearance_template", kwargs | {"skin_type": "scarred"}),
        },
        {
            "key": ("3", "wrinkled", "w"),
            "desc": "Wrinkled",
            "goto": ("chargen_appearance_template", kwargs | {"skin_type": "wrinkled"}),
        },
        {
            "key": ("4", "unblemished", "u"),
            "desc": "Unblemished",
            "goto": (
                "chargen_appearance_template",
                kwargs | {"skin_type": "unblemished"},
            ),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def appearance_eye_type(caller, raw_string, **kwargs):
    text = "|CSelect your Eye Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_eye_type"},
        {
            "key": ("1", "almond", "a"),
            "desc": "Almond",
            "goto": ("chargen_appearance_template", kwargs | {"eye_type": "almond"}),
        },
        {
            "key": ("2", "hooded", "h"),
            "desc": "Hooded",
            "goto": ("chargen_appearance_template", kwargs | {"eye_type": "hooded"}),
        },
        {
            "key": ("3", "round", "r"),
            "desc": "Round",
            "goto": ("chargen_appearance_template", kwargs | {"eye_type": "round"}),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def appearance_nose_type(caller, raw_string, **kwargs):
    text = "|CSelect your Nose Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_nose_type"},
        {
            "key": ("1", "aquiline", "a"),
            "desc": "Aquiline",
            "goto": ("chargen_appearance_template", kwargs | {"nose_type": "aquiline"}),
        },
        {
            "key": ("2", "button", "b"),
            "desc": "Button",
            "goto": ("chargen_appearance_template", kwargs | {"nose_type": "button"}),
        },
        {
            "key": ("3", "flat", "f"),
            "desc": "Flat",
            "goto": ("chargen_appearance_template", kwargs | {"nose_type": "flat"}),
        },
        {
            "key": ("4", "wide", "w"),
            "desc": "Wide",
            "goto": ("chargen_appearance_template", kwargs | {"nose_type": "wide"}),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def appearance_mouth_type(caller, raw_string, **kwargs):
    text = "|CSelect your Mouth Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_mouth_type"},
        {
            "key": ("1", "full", "f"),
            "desc": "Full",
            "goto": ("chargen_appearance_template", kwargs | {"mouth_type": "full"}),
        },
        {
            "key": ("2", "small", "s"),
            "desc": "Small",
            "goto": ("chargen_appearance_template", kwargs | {"mouth_type": "small"}),
        },
        {
            "key": ("3", "thin", "t"),
            "desc": "Thin",
            "goto": ("chargen_appearance_template", kwargs | {"mouth_type": "thin"}),
        },
        {
            "key": ("4", "wide", "w"),
            "desc": "Wide",
            "goto": ("chargen_appearance_template", kwargs | {"mouth_type": "wide"}),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def appearance_jaw_type(caller, raw_string, **kwargs):
    text = "|CSelect your Jaw Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_jaw_type"},
        {
            "key": ("1", "pointed", "p"),
            "desc": "Pointed",
            "goto": ("chargen_appearance_template", kwargs | {"jaw_type": "pointed"}),
        },
        {
            "key": ("2", "round", "r"),
            "desc": "Round",
            "goto": ("chargen_appearance_template", kwargs | {"jaw_type": "round"}),
        },
        {
            "key": ("3", "square", "s"),
            "desc": "Square",
            "goto": ("chargen_appearance_template", kwargs | {"jaw_type": "square"}),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def appearance_eyebrow_type(caller, raw_string, **kwargs):
    text = "|CSelect your Eyebrow Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_eyebrow_type"},
        {
            "key": ("1", "arched", "a"),
            "desc": "Arched",
            "goto": (
                "chargen_appearance_template",
                kwargs | {"eyebrow_type": "arched"},
            ),
        },
        {
            "key": ("2", "straight", "s"),
            "desc": "Straight",
            "goto": (
                "chargen_appearance_template",
                kwargs | {"eyebrow_type": "straight"},
            ),
        },
        {
            "key": ("3", "thick", "t"),
            "desc": "Thick",
            "goto": ("chargen_appearance_template", kwargs | {"eyebrow_type": "thick"}),
        },
        {
            "key": ("4", "thin", "th"),
            "desc": "Thin",
            "goto": ("chargen_appearance_template", kwargs | {"eyebrow_type": "thin"}),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def chargen_finalize(caller, raw_string):
    caller.move_to(XYZRoom.objects.get_xyz(xyz=("1", "1", "nautilus")), quiet=True)
    return "", ""
