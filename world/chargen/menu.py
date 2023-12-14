from typeclasses.characters import GenderType, RaceType

from evennia.utils import dedent

_RACE_INFO_DICT = {
    "human": "The most common face to see in Arcellia, humans are known for their tenacity, creativity, and endless capacity for growth.",  # noqa: E501
    "elf": "Elves of Arcellia embody an ageless grace, their histories etched into the very forests and rivers of the world. Ancient and wise, they live in harmonious synchrony with the natural tapestry that surrounds them, their lifelines stretching across eras like the boughs of the World Tree. With eyes that reflect the depth of the stars, elves harbor a mastery over magic few can rival, their arcane heritage as intrinsic as the wind's whisper. Bound by traditions woven through the fabric of time, they walk paths shadowed by lore, their existence a melody harmonizing with the ethereal song of eternity.",  # noqa: E501
    "half-elf": "Half-Elves inherit blessings from both their parents, but at the price of never quite fitting in. Curious, ambitious, and versatile, half-elves are welcome everywhere, but struggle without a community to call their own.",  # noqa: E501
    "dwarf": "As durable and unyielding as their homes of stone, dwarves are some of the finest warriors, miners, and smiths in all of Arcellia. They're known for their confidence and keen intuition, valuing family, ritual, and fine craftsmanship. Many of their ancient kingdoms have been surrendered to goblins and other creatures of the deep.",  # noqa: E501
    "halfling": "Halflings, with their diminutive stature, are a jovial folk whose stories are laced with luck and a penchant for the comfortable life, relishing in homely joys and a peaceful existence. Their nimble fingers and silent footfalls often steer their paths toward unexpected adventures.",  # noqa: E501
    "gnome": "Gnomes are diminutive, inquisitive inventors, their minds ever-ticking gears amidst a whirlwind of arcane intellect. They thrive on innovation, their lives a constant pursuit of knowledge, enchantment, and mechanical wonders that teeter on the brink of whimsy and genius.",  # noqa: E501
    "nymph": "Each Nymphkind bears an Elemental Allure, an innate charm that captures hearts as effortlessly as the elements wield their power. These beguiling beings breathe an otherworldly magnetism, entwining those who fall under their gaze with strands of lust, adoration, or sheer bewitchment. Like the ripples upon a still pond or the flickering dance of flames, their seductive powers manifest in various forms, reflecting the vast spectrum of their ancestral realm.",  # noqa: E501
    "orc": "Orcs exhibit widely varying appearances. Creatures of intense emotion, the orcs are more inclined to act than contemplate - whether the rage burning their bodies compels them to fight, or the love of filling their hearts inspires acts of incredible kindness.",  # noqa: E501
    "pyreling": "The Pyreling are descendents cloaked in myth, born of the mingling between mortal essence and the enigmatic energies of hell. They carry within them a flickering flame that manifests in eyes that glow like coals and skin in shades of smoldering dusk. Misunderstood by many, the Pyrelings wander through Arcellia bearing gifts of arcane affinity, as well as a propensity for the extraordinary, often leaving tales of fear and fascination in their wake.",  # noqa: E501
    # "drow": "The drow emerge from Arcellia's underbelly: a society that flourishes in the echoes of deep caverns and shunned fortresses. Their skin, ashen and cool to the touch, shimmers faintly with the ghostly beauty of the subterranean glow. Revered for their martial prowess and feared for their cunning, the Nocturnes navigate the world in relentless pursuit of power and arcane knowledge. Descended from their surface-dwelling kin through an ancient rift seeped in betrayal, they weave their existence in darkness.",  # noqa: E501
    # "lupine": "Canine-folk are social creatures with a robust code of honor. They walk with unmatched loyalty and fierce camaraderie. Equipped with acute senses and a formidable presence, the Lupines are revered as trackers and mediators, their howling sagas echoing under open skies and across wild expanses.",  # noqa: E501
    # "feline": "The feline people glide through Arcellia with a pounce of curiosity and a gait that whispers tales of distant lands. Cloaked in spotted or striped pelts that ripple with each measured move, these cat-like beings embody the very spirit of adventure. Felines collect stories and artifacts with a fervor as intense as their feral grace, with eyes alight with the gleam of the seeker. They are lore-weavers, nimble tricksters, and seekers of horizons, their lives a collection of tales and trinkets gathered from peaks unclimbed and paths untrodden. Their tales are as varied as their coats, each a patchwork of myriad experiences and encounters, chronicling the dance between wild instincts and thoughtful contemplation.",  # noqa: E501
}

_SUBRACE_INFO_DICT = {
    "elf": {
        "high": "The High Elves, ethereal as the twilight heavens, draw their lineage from the stars. With minds sharp as the crescent moon, they are curators of arcane wisdom, their lives as elongated as the very eternities they study. Their enclaves, built where ley lines converge, resonate with the harmonious magic of the firmament, reflecting the astral glory of their heritage in every spell they weave and every blade they forge under the watchful eyes of the constellations.",  # noqa: E501
        "wood": "Beneath emerald canopies, where life thrums in every leaf and branch, dwell the Wood Elves. Their souls are the voice of the forest, as serene as still water and as wild as the untamed grove. These elves are guardians of the natural world, moving with a grace that matches the swaying boughs and flowing streams, their instincts finely honed to the rhythm of the wilderness. Bridging the material plane and the natural realm in harmonious co-existence, Wood Elves invoke the vitality of the woods in their tireless defense against those who would despoil their verdant home.",  # noqa: E501
    },
    "half-elf": {
        "high": "High Half-Elves are the progeny of human aspiration and the sublime heritage of High Elves. They inherit an inncate arcane spark that illuminates their path, granting them access to the mystical arts that flow through their elvish bloodline. Walking the illuminated cooridors of ancient libraries as comfortably as the bustling human streets, they serve as conduits for the celestial wisdom of their elven ancestors, tempered by the practical innovation of their human side.",  # noqa: E501
        "wood": "Born from the marriage of human tenacity and the Wood Elders' natural attunement, Wood Half-Elves stand as champions of the wild frontiers. They share in the Wood Elves' harmonious connection with nature, yet are bolstered by human resilience and resourcefulness. Their affinity for the woodland realm and its denizens enables them to navigate the thicket and thorns of life with an ease that belies their half-human heritage, ensuring that they are as formidable in the wild as they are within the myriad enclaves of humanity.",  # noqa: E501
    },
    "dwarf": {
        "emberheart": "The Emberheart Dwarves glow with an inner fire, their souls alight with consummate confidence and a sharp, unerring insight. Celebrated for their intricate craftsmanship and elaborate ceremonies, the Emberhearts dwell within the grand vocanic forges of the Molten Hold, where kinship and artistry burn brighter than the furnaces that warm their halls.",  # noqa: E501
        "stoneguard": "Bearing the weight of history upon their broad shoulders, Stoneguard Dwarves have weathered the collapse of their once-mighty bastions, stoically surrendering their dominion to the relentless advance of goblin hordes and orcish legions. With hearts like the bedrock they cleave, these Dwarves nurture a collective resilience, driven by a cynical yet unwavering resolve to reclaim the glory and the halls of their ancestors.",  # noqa: E501
        "ironvein": "Forged in the dark crucible of the world's underbelly, the Ironvein Dwarves trace their lineage through centuries spent in the eerie expanses of the deep. Exposed to mysteries that warp mind and matter, imbued with the arcane residue that pulses through their cavernous abyss, they have emerged with esoteric powers that are both a gift and a legacy of old tyrannies. Survival meant enduring cruel manipulation by aberrant overlords, and from such depths of despair rose the fortitude and psionic might that now courses through the veins of these steely-eyed survivors. Though the chains of the past have been cast off, the Ironveins have never forgotten the cold embrace of subjugation, nor the sweet taste of hard-won freedom.",  # noqa: E501
    },
    "halfling": {
        "swiftshadow": "Swiftshadow Halflings, nimble and gregarious souls, flit through the realms of Arcellia with a wanderlust as light as their footsteps. Known for melding into shadows with a whispering grace, they traverse far and wide, tales woven into stores shared around hearth and marketplace. Despite their elusive nature, they foster bonds that cross continents, always eager to etch their names into the annals of adventure with their convivial spirit and artful stealth.",  # noqa: E501
        "hearthstone": "Hearthstone Halflings, steadfast as the earth beneath them, boast a fortitude born of legend, rumored to be touched by the ancient vigor of dwarven ancestry. In the wake of adversity, they stand undaunted. With a quiet strength, Hearthstone Halflings carve their legacy into the heart of the community, enduring in the face of trial as any mountain stands against the tempest's siege.",  # noqa: E501
    },
    "gnome": {
        "sylvan": "Sylvan Gnomes, sprightly and secretive as the woodland sprites, dwell amidst the verdant groves and dappled glades of Arcellia's vast forests. Whispering to the trees and laughing with the brooks, they are unseen keepers of nature's most secluded riddles, guarding the sylvan sanctuaries against those who would dare disturb them. With an affinity for the woods, these Gnomes craft enchantments as delicate as cobwebs, and their laughter is as fleeting as the wind through the leaves.",  # noqa: E501
        "dusk": "Veiled in mystery and born of the shadowy embrace of the subterranean world, Dusk Gnomes traverse the hidden depths with a grace that belies their surroundings. Illuminated by the faint glow of luminescent fungi and echoing caverns, they are silent witnesses to secrets entombed in stone. Masters of quietude and guile, Dusk Gnomes navigate the labyrinthine underworld with an innate understanding that is as profound as the ancient darkness from which they emerge.",  # noqa: E501
        "hearth": "An embodiment of scrupulous ingenuity and unshakable stability, Hearth Gnomes thrive within the heart of bustling communities or quaint hamlets. With hands weathered by toil, yet as precise as a master clockmaker's, they churn out marvels of craftsmanship and innovation. Hearth Gnomes are the cornerstone of tradition, etching each day's labor into the enduring legacy of their kin. Their tenacious spirits are akin to the enduring stone, shaping society with the chisel of their relentless pursuit of excellence and progress.",  # noqa: E501
    },
    "pyreling": {
        "emberkin": "Emberkin Pyrelings harbor the essence of smoldering embers and soul-deep shadows. Their lineage serves as a conduit for fiery dominion, allowing them to summon both the scalding wrath and the obsidian shroud of their fearsome forefathers.",  # noqa: E501
        "arcanist": "The Arcanist Pyrelings trace their heritage to the inscrutable compact with the grand magus of the Infernal. These Pyrelings are imbued with an arcane reservoir, deep and vast, granting them an affinity for the eldritch arts that is both singular and potent. With a mere incantation, they can bend the weft of magical energies to their will, shaping the fabric of spellcraft with ease.",  # noqa: E501
        "warbrand": "Forged in the martial traditions of the fiery fortresses, Warbrand Pyrelings are the progeny of pacts with war-torn overlords. Their very beings thrum with martial prowess and the relentless surge of the inferno that fuels their relentless spirit.",  # noqa: E501
    },
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
        """  # noqa: E501
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
    def _set_race(caller, **kwargs):
        race = kwargs.get("selected_race", None)
        subrace = kwargs.get("selected_subrace", None)

        if not race:
            caller.msg("An error occurred. Contact an administrator.")
            return "chargen_welcome"

        if race == "human":
            caller.race = RaceType.HUMAN
        elif race == "elf" and subrace == "high":
            caller.race = RaceType.HIGH_ELF
        elif race == "elf" and subrace == "wood":
            caller.race = RaceType.WOOD_ELF
        elif race == "half-elf" and subrace == "high":
            caller.race = RaceType.HIGH_HALF_ELF
        elif race == "half-elf" and subrace == "wood":
            caller.race = RaceType.WOOD_HALF_ELF
        elif race == "dwarf" and subrace == "emberheart":
            caller.race = RaceType.EMBERHEART_DWARF
        elif race == "dwarf" and subrace == "stoneguard":
            caller.race = RaceType.STONEGUARD_DWARF
        elif race == "dwarf" and subrace == "ironvein":
            caller.race = RaceType.IRONVEIN_DWARF
        elif race == "halfling" and subrace == "swiftshadow":
            caller.race = RaceType.SWIFTSHADOW_HALFLING
        elif race == "halfling" and subrace == "hearthstone":
            caller.race = RaceType.HEARTHSTONE_HALFLING
        elif race == "gnome" and subrace == "sylvan":
            caller.race = RaceType.SYLVAN_GNOME
        elif race == "gnome" and subrace == "dusk":
            caller.race = RaceType.DUSK_GNOME
        elif race == "gnome" and subrace == "hearth":
            caller.race = RaceType.HEARTH_GNOME
        elif race == "nymph":
            caller.race = RaceType.NYMPH
        elif race == "orc":
            caller.race = RaceType.ORC
        elif race == "pyreling" and subrace == "emberkin":
            caller.race = RaceType.EMBERKIN_PYRELING
        elif race == "pyreling" and subrace == "arcanist":
            caller.race = RaceType.ARCANIST_PYRELING
        elif race == "pyreling" and subrace == "warbrand":
            caller.race = RaceType.WARBRAND_PYRELING
        else:
            caller.msg("An error occurred. Contact an administrator.")
            return "chargen_welcome"

        return "chargen_class"

    selected_race = kwargs.get("selected_race", None)
    selected_subrace = kwargs.get("selected_subrace", "")

    if selected_subrace:
        text = _SUBRACE_INFO_DICT[selected_race][selected_subrace]
    elif selected_race:
        text = _RACE_INFO_DICT[selected_race]
    else:
        text = dedent(
            """
            Majestic landscapes unfold around you, a canvas for ethnic identities roaming within the bounds of thought. Mighty mountainscapes craft silhouettes against the sky, where the kin of giants and dwarves could forge their legacies in stone and steel. Lush forests carpet the realms below, bearing the sagas of elves and faefolk, their lifespans entwined with the ageless trees. Vast plains stretch out, horizons unbroken, where the footsteps of nomadic tribes echo with the steadfast will of orcish clans. Deep waters shimmer, hiding the secretive abodes of merfolk and naiads, whose songs thread through the currents, weaving stories of depth and mystery.

            Time teems on the brink of stillness, waiting for you to reach out and grasp the thread of existence calling to your spirit.
            """  # noqa: E501
        )

    if not selected_race:
        options = []
        for race in _RACE_INFO_DICT.keys():
            options.append(
                {"key": race, "goto": ("chargen_race", {"selected_race": race})}
            )

    elif (
        selected_race
        and not selected_subrace
        and _SUBRACE_INFO_DICT.get(selected_race, None)
    ):
        options = []
        for subrace in _SUBRACE_INFO_DICT[selected_race].keys():
            options.append(
                {
                    "key": subrace,
                    "goto": (
                        "chargen_race",
                        {"selected_race": selected_race, "selected_subrace": subrace},
                    ),
                }
            )

    elif (selected_race and selected_subrace) or (
        selected_race and not _SUBRACE_INFO_DICT.get(selected_race, None)
    ):
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
