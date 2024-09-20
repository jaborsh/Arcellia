from evennia.utils import dedent
from evennia.utils.utils import inherits_from

from utils.text import _INFLECT
from world.characters import (
    genders,
    races,
)


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
        {
            "key": ("y", "yes"),
            "desc": "Enable Screenreader",
            "goto": _set_screenreader,
        },
        {
            "key": ("n", "no"),
            "desc": " Disable Screenreader",
            "goto": "chargen_gender",
        },
        {"key": "_default", "goto": "chargen_welcome"},
    )

    return text, options


def chargen_gender(caller, raw_string, **kwargs):
    def _set_gender(caller, **kwargs):
        caller.traits.add("gender", "Gender", value=kwargs.get("gender"))
        return "chargen_race"

    text = dedent(
        """\
        Look who's decided to crawl out of the void and play dress-up. Couldn't resist the siren call of existence, could you? Had to go and remember you're a someone.
        
        Fine, you glutton for punishment. Time to pick your flesh prison. What'll it be, sweetcheeks? The old Adam's apple and dangly bits combo? Maybe you'd prefer the estrogen-fueled emotional whirlwind complete with society's impossible expectations? If you're a true connoisseur of mischief, there's always door number three: androgynity. It's the gender equivalent of a shapeshifting illusion, a living question mark that scoffs at the binary.

        |CSo what's it going to be, baby?|n
        """
    )

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
    if caller.gender.value == genders.Gender.MALE:
        text = genders.GENDER_INFO_DICT["male"]
    elif caller.gender.value == genders.Gender.FEMALE:
        text = genders.GENDER_INFO_DICT["female"]
    else:
        text = genders.GENDER_INFO_DICT["androgynous"]

    options = (
        {"key": "", "goto": "chargen_race"},
        {
            "key": ("1", "human"),
            "desc": "Human",
            "goto": (
                "chargen_race_confirmation",
                {"race": races.RaceRegistry.get("human")},
            ),
        },
        {
            "key": ("2", "elf"),
            "desc": "Elf",
            "goto": (
                "chargen_race_confirmation",
                {"race": races.RaceRegistry.get("elf")},
            ),
        },
        {
            "key": ("3", "drow"),
            "desc": "Drow",
            "goto": (
                "chargen_race_confirmation",
                {"race": races.RaceRegistry.get("drow")},
            ),
        },
        {
            "key": ("4", "halfling"),
            "desc": "Halfling",
            "goto": (
                "chargen_race_confirmation",
                {"race": races.RaceRegistry.get("halfling")},
            ),
        },
        {
            "key": ("5", "dwarf"),
            "desc": "Dwarf",
            "goto": (
                "chargen_race_confirmation",
                {"race": races.RaceRegistry.get("dwarf")},
            ),
        },
        {
            "key": ("6", "gnome"),
            "desc": "Gnome",
            "goto": (
                "chargen_race_confirmation",
                {"race": races.RaceRegistry.get("gnome")},
            ),
        },
        {"key": "_default", "goto": "chargen_race"},
    )

    return text, options


def chargen_race_confirmation(caller, raw_string, **kwargs):
    def _set_race(caller, **kwargs):
        race = kwargs.get("race")
        caller.traits.add("race", "Race", value=race)
        caller.race.value.initialize_race_equipment(caller)
        caller.race.value.initialize_race_features(caller)
        return "chargen_finalize"

    race = kwargs.get("race")
    text = (
        races.RACE_INFO_DICT[race.key.lower()] + "\n"
        f"|CWill you be {_INFLECT.a(race.key.lower())}|n?\n"
    )

    options = (
        {"key": "", "goto": "chargen_race"},
        {"key": ("y", "yes"), "desc": "Yes", "goto": (_set_race, kwargs)},
        {"key": ("n", "no"), "desc": "No", "goto": "chargen_race"},
        {"key": "_default", "goto": "chargen_race"},
    )

    return text, options


def chargen_finalize(caller, raw_string):
    start = caller.search(
        "#2", global_search=True, use_dbref=True
    )  # XYZRoom.objects.get_xyz(xyz=("4", "0", "sunwreck_shores"))
    caller.location = start
    caller.init_flasks()

    for eq in caller.contents:
        if inherits_from(eq, "typeclasses.equipment.equipment.Equipment"):
            caller.equipment.wear(eq)

    return "", ""
