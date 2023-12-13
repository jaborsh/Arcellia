from evennia.utils import dedent
from typeclasses.characters import GenderType

_RACE_INFO_DICT = {
    "human": "An adaptable and diverse people. Their aspirations drive them to achieve greatness in the fields of art, science, magic, and war. With lifespans briefer than their elven or dwarven counterparts, humans pursue their legacies with zeal, their determination fueling the engine of societies both vast and intricate. From the verdant valleys of agrarian communities to the towering spires of metropolitan achievement, humans shape the world with their fervent pace of progress, ever-expanding the boundaries of their dominion and the scope of their ambition.",
    "elf": "Elves of Arcellia embody an ageless grace, their histories etched into the very forests and rivers of the world. Ancient and wise, they live in harmonious synchrony with the natural tapestry that surrounds them, their lifelines stretching across eras like the boughs of the World Tree. With eyes that reflect the depth of the stars, elves harbor a mastery over magic few can rival, their arcane heritage as intrinsic as the wind's whisper. Bound by traditions woven through the fabric of time, they walk paths shadowed by lore, their existence a melody harmonizing with the ethereal song of eternity.",
    "drow": "The drow emerge from Arcellia's underbelly: a society that flourishes in the echoes of deep caverns and shunned fortresses. Their skin, ashen and cool to the touch, shimmers faintly with the ghostly beauty of the subterranean glow. Revered for their martial prowess and feared for their cunning, the Nocturnes navigate the world in relentless pursuit of power and arcane knowledge. Descended from their surface-dwelling kin through an ancient rift seeped in betrayal, they weave their existence in darkness.",
    "pyreling": "The Pyreling are descendents cloaked in myth, born of the mingling between mortal essence and the enigmatic energies of hell. They carry within them a flickering flame that manifests in eyes that glow like coals and skin in shades of smoldering dusk. Misunderstood by many, the Pyrelings wander through Arcellia bearing gifts of arcane affinity, as well as a propensity for the extraordinary, often leaving tales of fear and fascination in their wake.",
    "dwarf": "As durable and unyielding as their homes of stone, dwarves are some of the finest warriors, miners, and smiths in all of Arcellia. They're known for their confidence and keen intuition, valuing family, ritual, and fine craftsmanship. Many of their ancient kingdoms have been surrendered to goblins and other creatures of the deep.",
    "halfling": "Halflings, with their diminutive stature, are a jovial folk whose stories are laced with luck and a penchant for the comfortable life, relishing in homely joys and a peaceful existence. Their nimble fingers and silent footfalls often steer their paths toward unexpected adventures.",
    "orc": "Orcs exhibit widely varying appearances. Creatures of intense emotion, the orcs are more inclined to act than contemplate - whether the rage burning their bodies compels them to fight, or the love of filling their hearts inspires acts of incredible kindness.",
    "nymph": "Nymphs are the beguiling offspring of the Arcellian elements, their spirits echoing with the whispers of the natural world. Born from the raw forces that shape land, water, air, fire, or something more hybrid, each nymph carries the essence of their elemental facet within them. Their appearance radiates the beauty of the fae; they move with an otherworldly grace that captivates beholders. Sensual and enchanting, nymphs possess an innate magnetism that mirrors the primal allure of the wilds. The complexity of their heritage weaves them into every crevice of Arcellia, where they venerate the profound powers of their elemental ancestors.",
    "gnome": "Gnomes are diminutive, inquisitive inventors, their minds ever-ticking gears amidst a whirlwind of arcane intellect. They thrive on innovation, their lives a constant pursuit of knowledge, enchantment, and mechanical wonders that teeter on the brink of whimsy and genius.",
    "lupine": "Canine-folk are social creatures with a robust code of honor. They walk with unmatched loyalty and fierce camaraderie. Equipped with acute senses and a formidable presence, the Lupines are revered as trackers and mediators, their howling sagas echoing under open skies and across wild expanses.",
    "feline": "The feline people glide through Arcellia with a pounce of curiosity and a gait that whispers tales of distant lands. Cloaked in spotted or striped pelts that ripple with each measured move, these cat-like beings embody the very spirit of adventure. Felines collect stories and artifacts with a fervor as intense as their feral grace, with eyes alight with the gleam of the seeker. They are lore-weavers, nimble tricksters, and seekers of horizons, their lives a collection of tales and trinkets gathered from peaks unclimbed and paths untrodden. Their tales are as varied as their coats, each a patchwork of myriad experiences and encounters, chronicling the dance between wild instincts and thoughtful contemplation.",
    "taurakin": "Taurakin stride through the diverse realms of Arcellia, their robust and commanding presence a sight to behold. These horn-rowned denizens, while not towering as giants, stand with an undeniable air of fortitude, often reaching the heights of ten feet. Their heritage is of labyrinthine ancestries and the vast, open skies over sprawling vistas. Known for the rich wisdom and respect for ancestral traditions, Taurakin culture is grounded in principles of courage, loyalty, and the pursuit of personal excellence. Their homes range from the heart of sun-kissed savannas to the architectural wonders of their own creation, echoing the sturdy and determined nature of the Taurakin spirit.",
}


def chargen_welcome(caller):
    def _set_gender(caller, choice):
        choice = choice.strip().lower()[0]
        if choice == "m":
            caller.gender = GenderType.MALE
        elif choice == "f":
            caller.gender = GenderType.FEMALE
        elif choice == "a":
            caller.gender = GenderType.AMBIGUOUS
        else:
            return "chargen_welcome"

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
        {"key": ("male", "m"), "desc": "Become male", "goto": _set_gender},
        {"key": ("female", "f"), "desc": "Become female", "goto": _set_gender},
        {"key": ("ambiguous", "a"), "desc": "Become ambiguous", "goto": _set_gender},
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
        Majestic landscapes unfold around you, a canvas for ethnic identities roaming within the bounds of thought. Mighty mountainscapes craft silhouettes against the sky, where the kin of giants and dwarves could forge their legacies in stone and steel. Lush forests carpet the realms below, bearing the sagas of elves and faefolk, their lifespans entwined with the ageless trees. Vast plains stretch out, horizons unbroken, where the footsteps of nomadic tribes echo with the steadfast will of orcish clans. Deep waters shimmer, hiding the secretive abodes of merfolk and naiads, whose songs thread through the currents, weaving stories of depth and mystery.

        Time teems on the brink of stillness, waiting for you to reach out and grasp the thread of existence calling to your spirit.
        """
        )
    )

    if selected_race:
        options = (
            {
                "key": "y",
                "desc": f"Confirm {selected_race}",
                "goto": "chargen_race",
            },
            {
                "key": "n",
                "desc": "Return",
                "goto": ("chargen_race", {"selected_race": None}),
            },
        )
    else:
        options = []
        for race in _RACE_INFO_DICT.keys():
            if race != selected_race:
                options.append(
                    {"key": race, "goto": ("chargen_race", {"selected_race": race})}
                )
    return text, options
