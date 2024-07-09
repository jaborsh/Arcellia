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

        This is it, kiddo. The big nothing. The grand finale. The ultimate \"Fuck you!\" to existence itself.

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
    def _set_gender(caller, **kwargs):
        caller.traits.add(
            "gender",
            "Gender",
            value=kwargs.get('gender')
        )
        
        return "chargen_race"

    text = dedent(
        """\
        Look who's decided to start existing again. Typical. You just had to go and remember you're someone, didn't you?

        Alright, meat puppet, time to choose your flesh prison. What'll it be? The old Adam's apple and dangly bits combo? Or perhaps you'd prefer the estrogen-fueled emotional whirlwind? Oh, and if you're indecisive, there's always door number three: the androgynous special, perfect for those who like to keep the world guessing.

        |CSo what's it going to be, baby?|n
        """
    )  # noqa: E501

    options = (
        {"key": "", "goto": "chargen_welcome"},
        {
            "key": ("1", "male", "m"),
            "desc": "Male",
            "goto": (_set_gender, {"gender": genders.Gender.MALE}),
        },
        {
            "key": ("2", "female", "f"),
            "desc": "Female",
            "goto": (_set_gender, {"gender": genders.Gender.FEMALE}),
        },
        {
            "key": ("3", "androgynous", "a"),
            "desc": "Androgynous",
            "goto": (_set_gender, {"gender": genders.Gender.ANDROGYNOUS}),
        },
        {"key": "_default", "goto": "chargen_gender"},
    )

    return text, options


def chargen_race(caller, raw_string, **kwargs):
    def _set_race(caller, **kwargs):
        return "chargen_finalize"

    if caller.gender.value == genders.Gender.MALE:
        text = genders.GENDER_INFO_DICT['male']
    elif caller.gender.value == genders.Gender.FEMALE:
        text = genders.GENDER_INFO_DICT['female']
    else:
        text = genders.GENDER_INFO_DICT['androgynous']

    return text, ""


def chargen_finalize(caller, raw_string):
    caller.move_to(
        XYZRoom.objects.get_xyz(xyz=("4", "0", "sunwreck_shores")), quiet=True
    )
    return "", ""
