import re
from enum import Enum

_GENDER_PRONOUN_MAP = {
    "male": {"s": "he", "o": "him", "p": "his", "a": "his"},
    "female": {"s": "she", "o": "her", "p": "her", "a": "hers"},
    "neutral": {"s": "it", "o": "it", "p": "its", "a": "its"},
    "androgynous": {"s": "they", "o": "them", "p": "their", "a": "theirs"},
}

_RE_GENDER_PRONOUN = re.compile(r"(?<!\|)\|(?!\|)[sSoOpPaA]")

GENDER_INFO_DICT = {
    "male": "Men in Arcellia come in many shapes and sizes, from many races and many backgrounds. Whether tall and muscular, or short and lean, they are often reputed to be sons of Adon, the First Man and God of the son. Typically known for their great passions, in love and in war, men are revered in the worlds of humans and orcs as the superior race, yet amongst elves, dwarves, and pyrelings, share equality with the rest. Adonites are the pinnacle of masculinity, a race of only men, and are the source of envy and resentment in many individuals across the world.",
    "female": "The Gift of Hela onto the world, children of the moon and her divine right, women are known for their mystery and beauty alike. Whilst they may range in size, stature, and disposition, one truth remains - hell hath no fury like a woman scorned. Known for their exceptional wit and persuasion, they have no less found themselves in a more submissive society amongst some races. Yet, in others, they are known as leaders - the nymphs and the beastials revere their matriarchs and follow their wisdom, whilst the Helias commonly cloister themselves away, such that to see one might be a rarity to happen in a single lifetime. In fact, it is considered an ill omen when the Helias are seen in numbers, as if portents of the world's end.",
    "androgynous": "For some, the world is not so easily viewed as day and night, as light or dark, as black or white - for many, it is the colors and forms in between which speak to their truth, and so is it said that Gan, the Ruler of the Twilight Realm, gifted mortality with the ability to choose. When a soul is beyond the scope, their form takes the shape of their choosing, as varied and unique as they themselves. In fact, it is said that the Twils, a race of individuals who dwell within the twilight, might change their shape at will, adapting to suit their heart's fancy, Gan's greatest gift to their beloved people.\n\nAndrogynous individuals are generally accepted in most societies, but some may have found their homes more accepting than others, or less willing to understand their dispositions. In main cities, it is considered very disrespectful, and sometimes illegal, to disregard an individual's identity.",
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
