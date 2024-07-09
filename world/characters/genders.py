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
        Decided to be a dangler, did you? Brave choice, considering the baggage that comes with it. Now let's pick your flavor of bipedal misery:

        Will you be a plain old human, doomed to mediocrity and male-pattern baldness? Or perhaps an elf, eternally pretty but with the personality of a particularly dull tree? Maybe you're the edgy type - how about a dark elf, brooding in the shadows? Halfling, perhaps; perfect for second breakfasts and hairy feet fetishists. You might fancy the dwarven life: beard-grooming and ale-guzzling. If you're feeling particularly masochistic, gnomes are always mistaken for garden decor.

        |CChoose wisely, meat sack|n:
        """
    ),
    "female": dedent(
        """
        Ah, embracing the fairer sex. Get ready for a lifetime of being interrupted and explained to about your own experiences. Now, let's pick out your costume.
        
        Fancy being a human, forever chasing impossible beauty standards? An elf doomed to be the object of every nerd's fantasy? Dark elf more your speed, with a chip on your shoulder bigger than your bust size? A halfling has all the joys of being mistaken for a child with none of the innocence. Dwarves break all the stereotypes and can grow a magnificent beard. And gnomes are the perfect height for being overlooked and underestimated.

        |CPick your poison, sister|n:
        """
    ),
    "androgynous": dedent(
        """
        Ooh, playing it coy! Refusing to be pinned down by society's binary nonsense. Fine, let's pick your flavor of ambiguity.
        
        How about human, forever explaining your pronouns? Elves are androgynous enough to make even the trees question their gender. Dark elf could be fun - nothing says "I contain multitudes" quite like permanent resting bitch face. Halfling's an option if you want to keep everyone guessing about your age, too. Dwarf could be interesting - not everyone with a beard is a man. Or go full gnome and really embrace the "what the hell are you?" lifestyle; nothing says "gender is a construct" quite like being mistaken for lawn ornaments. 

        |CChoose your vessel|n:
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
