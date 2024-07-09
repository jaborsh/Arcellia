import re
from enum import Enum
from evennia.utils import dedent

_GENDER_PRONOUN_MAP = {
    "male": {"s": "he", "o": "him", "p": "his", "a": "his"},
    "female": {"s": "she", "o": "her", "p": "her", "a": "hers"},
    "neutral": {"s": "it", "o": "it", "p": "its", "a": "its"},
    "androgynous": {"s": "they", "o": "them", "p": "their", "a": "theirs"},
}

_RE_GENDER_PRONOUN = re.compile(r"(?<!\|)\|(?!\|)[sSoOpPaA]")

GENDER_INFO_DICT = {
    "male": dedent(
        """
        Decided to be a dangler, did you? Congratulations on your newfound ability to mansplain and manspread. Now, let's see what kind of suit you want to parade around in.

        Will it be the boring old human model? Or perhaps you fancy yourself an elf, all pointy-eared and holier-than-thou? Maybe you're more of a stout little dwarf, with a beard full of ale foam and a chip on your shoulder? How about a gnome, small enough to hide from your problems but not your insecurities? Halfling, perhaps; perfect for second breakfasts and hairy feet fetishists? And let's not forget the orc option - nothing says \"I have anger issues\" quite like green skin and protruding tusks.

        |CChoose wisely, meat sack.|n
        """
    ),
    "female": dedent(
        """
        Ah, embracing the fairer sex. Get ready for a lifetime of being interrupted and explained to about your own experiences. Now, let's pick out your costume.

        Fancy being a run-of-the-mill human? Or maybe an elf, so you can look down your nose at everyone for millennia? How about a dwarf; short, stout, and perpetually angry? Or a gnome; tiny, tinkering, and probably with a voice that could shatter class? A halfling has all the joys of being mistaken for a child with none of the innocence. Don't forget the nymph option - because nothing says \"Take me seriously!\" like being a living, breathing fantasy.

        |CPick your poison, sister.|n
        """
    ),
    "androgynous": dedent(
        """
        Ooh, playing it coy! Not picking a side? How very... indecisive of you. Well, let's see what kind of ambiguous meat suit you'd like to slip into.

        Will it be the utterly unremarkable human? Perhaps the elf, for when you want to be androgynous for several thousand years? Maybe the dwarf catches your fancy - compact, sturdy, and with a beard that's the envy of all genders.

        How about a gnome? Small in stature but big on confusing everyone around you. Or a halfling, for when you want to be mistaken for a child of indeterminate gender. There's always the nymph option - nothing says \"gender is societal\" quite like being a living embodiment of nature's whimsy.

        Don't forget the orc - because sometimes you just want to rage against the gender binary while also raging against everything else.

        Choose your vessel, you beautiful enigma.
        """
    )
}


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    ANDROGYNOUS = "androgynous"
    NEUTRAL = "neutral"


GENDER_MAP = {
    "male": Gender.MALE,
    "female": Gender.FEMALE,
    "androgynous": Gender.ANDROGYNOUS,
    "neutral": Gender.NEUTRAL,
}
