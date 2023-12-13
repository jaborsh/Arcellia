from evennia.utils import dedent

_RACE_INFO_DICT = {
    "human": "The most common face to see in Arcellia, known for their tenacity, creativity, and endless capacity for growth.",
    "elf": "With an ethereal countenance and long lifespans, elves are at home with nature's power, flourishing in the light and dark alike.",
    "drow": "Raised by cults, the drow extol the virtues of corruption and mercilessness. They're a result of an ancient schism with the elves. Treachery drove the drow into the depths of the world where they splintered into warring factions.",
    "dwarf": "As durable and unyielding as their homes of stone, dwarves are some of the finest warriors, miners, and smiths in all of Arcellia. They're known for their confidence and keen intuition, valuing family, ritual, and fine craftsmanship. Many of their ancient kingdoms have been surrendered to goblins and other creatures of the deep.",
    "orc": "Orcs exhibit widely varying appearances. Creatures of intense emotion, the orcs are more inclined to act than contemplate - whether the rage burning their bodies compels them to fight, or the love of filling their hearts inspires acts of incredible kindness.",
    "feline": "Felines are lithe and graceful, with a keen intellect and a strong sense of curiosity. They're known for their love of the hunt, and their ability to move with the shadows.",
    "nymph": "Nymphs are ethereal beings, with a deep connection to the elements. They're known for their beauty and grace, but also their capriciousness.",
}


def chargen_welcome(caller):
    def _set_male(caller):
        caller.db.gender = "male"
        return "chargen_race"

    def _set_female(caller):
        caller.db.gender = "female"
        return "chargen_race"

    text = dedent(
        """\
        You, the nascent traveler, float amidst this gentle void. A mere wisp of consciousness, you harbor the power to mold your very essence. Here in this prelude to adventure, the choice of one's very existence is the first dalliance with creation.
        
        At the center of this void, two figures emerge from the nebulous gray, standing as pillars of potentiality. One basks in a soft radiance which might be likened to the sun's touch, strength and grace melded in harmony. The other exudes a quiet luminescence reminiscent of the moon's tender glow, an elegance that dances in union with resilience.

        In this moment, suspended between the not-yet-shaped and the eternal, a question crystallizes before your burgeoning self.
        """
    )

    options = (
        {"key": "", "goto": "chargen_welcome"},
        {"key": "male", "desc": "Become male", "goto": _set_male},
        {"key": "female", "desc": "Become female", "goto": _set_female},
        {"key": "_default", "goto": "chargen_welcome"},
    )

    return text, options


def chargen_race(caller, raw_string, **kwargs):
    selected_race = kwargs.get("selected_race", None)
    text = (
        _RACE_INFO_DICT[selected_race]
        if selected_race
        else dedent(
            """
        As your new being accepts its form, the figures that once stood as abstract representations melt away like wisps of morning mist succumbing to day's embrace. From the tranquil canvas of nothingness, contours of lands and realms begin to emerge, brief glimpses of the world beyond. Therein lies the flourish of diversity.

        A multitude of silhouettes coalesce, each bearing the unique visage of another kind of being. There is the diverse tapestry of Humanity, resilient and adaptable, wielding determination as their banner; the lofty elegance of the Elves, threaded with the ancient magics of the woods and stars; the steadfast stoicism of the Dwarves with their spirited etched in stone and song.
        
        And there are others, less known, perhaps more alluring for their rarity: the shadowy tie of the Drow to the night, moving like a whisper through darkness; the orcs, whose dual nature is a dance of the primal and the civilized; the lithe grace of the Felines, their feral nature tempered by keen intellect; and the ethereal beauty of the Nymphs, whose very essence is a bridge to the elements.

        |wSelect: |whuman|n, |welf|n, |wdwarf|n, |wdrow|n, |worc|n, |wfeline|n, or |wnymph|n
        """
        )
    )

    options = []

    if selected_race:
        options.append(
            {
                "key": ("human", "confirm", "y", "yes"),
                "desc": f"Confirm {selected_race}",
                "goto": "chargen_race",
            }
        )

    for race in _RACE_INFO_DICT.keys():
        if race != selected_race:
            options.append(
                {"key": race, "goto": ("chargen_race", {"selected_race": race})}
            )
    return text, options
