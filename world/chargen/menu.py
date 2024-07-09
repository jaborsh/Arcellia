from evennia.prototypes import spawner
from evennia.utils import dedent

from world.characters import (
    appearances,
    backgrounds,
    classes,
    genders,
    races,
    score,
)
from world.xyzgrid.xyzroom import XYZRoom

_BACKGROUND_INFO_DICT = backgrounds.BACKGROUND_INFO_DICT

_CLASS_INFO_DICT = classes.CLASS_INFO_DICT

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
        Ah, sweet oblivion! Here you are, floating in the vast nothingness of pre-existence. It's a cozy little void, isn't it? Warm, dark, and utterly devoid of all that pesky |y*meaning*|n people lug about.

        An endless expanse of primordial soup, thicker than molasses and blacker than black. Your excuse for a soul is nothing more than a speck, a mote, an infinitesimal crumb of half-formed thought bobbing around in this cosmic stew.

        This is it, kiddo. The big nothing. The grand finale. The ultimate \"Screw you!\" to existence itself.

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
            Look who's decided to start existing again. Typical. You just had to go and remember you're someone, didn't you?

            Alright, meat puppet, time to choose your flesh prison. What'll it be? The old Adam's apple and dangly bits combo? Or perhaps you'd prefer the estrogen-fueled emotional whirlwind? Oh, and if you're indecisive, there's always door number three: the androgynous special, perfect for those who like to keep the world guessing.

            So what's it going to be, baby? Male, female, or that sweet spot in between? Remember, whichever meat suit you choose, it comes fully equipped with the capacity for pain, regret, and the occasional bodily function.

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
        return "chargen_finalize"

    selected_race = kwargs.get("selected_race", None)
    selected_subrace = kwargs.get("selected_subrace", "")

    if selected_subrace:
        text = _SUBRACE_INFO_DICT[selected_race][selected_subrace] + "\n"
    elif selected_race:
        text = _RACE_INFO_DICT[selected_race] + "\n"
    else:
        male_text = dedent(
            """
            Decided to be a dangler, did you? Congratulations on your newfound ability to mansplain and manspread. Now, let's see what kind of suit you want to parade around in.

            Will it be the boring old human model? Or perhaps you fancy yourself an elf, all pointy-eared and holier-than-thou? Maybe you're more of a stout little dwarf, with a beard full of ale foam and a chip on your shoulder? How about a gnome, small enough to hide from your problems but not your insecurities? Halfling, perhaps; perfect for second breakfasts and hairy feet fetishists? And let's not forget the orc option - nothing says \"I have anger issues\" quite like green skin and protruding tusks.

            Choose wisely, meat sack.

            |CSelect your Race|n:
            """  # noqa: E501
        )

        female_text = dedent(
            """
            Ah, embracing the fairer sex. Get ready for a lifetime of being interrupted and explained to about your own experiences. Now, let's pick out your costume.

            Fancy being a run-of-the-mill human? Or maybe an elf, so you can look down your nose at everyone for millennia? How about a dwarf; short, stout, and perpetually angry? Or a gnome; tiny, tinkering, and probably with a voice that could shatter class? A halfling has all the joys of being mistaken for a child with none of the innocence. Don't forget the nymph option - because nothing says \"Take me seriously!\" like being a living, breathing fantasy.

            Pick your poison, sister.
            """
        )

        andro_text = dedent(
            """
            Ooh, playing it coy! Not picking a side? How very... indecisive of you. Well, let's see what kind of ambiguous meat suit you'd like to slip into.

            Will it be the utterly unremarkable human? Perhaps the elf, for when you want to be androgynous for several thousand years? Maybe the dwarf catches your fancy - compact, sturdy, and with a beard that's the envy of all genders.

            How about a gnome? Small in stature but big on confusing everyone around you. Or a halfling, for when you want to be mistaken for a child of indeterminate gender. There's always the nymph option - nothing says \"gender is societal\" quite like being a living embodiment of nature's whimsy.

            Don't forget the orc - because sometimes you just want to rage against the gender binary while also raging against everything else.

            Choose your vessel, you beautiful enigma.
            """
        )

        if caller.gender == genders.Gender.MALE:
            text = male_text
        elif caller.gender == genders.Gender.FEMALE:
            text = female_text
        else:
            text = andro_text

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


def chargen_finalize(caller, raw_string):
    caller.move_to(
        XYZRoom.objects.get_xyz(xyz=("0", "4", "sunwreck_shores")), quiet=True
    )
    return "", ""
