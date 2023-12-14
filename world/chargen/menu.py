from typeclasses.characters import BackgroundType, ClassType, GenderType, RaceType

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

_RACE_SUBRACE_MAPPING = {
    "human": RaceType.HUMAN,
    "elf": {"high": RaceType.HIGH_ELF, "wood": RaceType.WOOD_ELF},
    "half-elf": {"high": RaceType.HIGH_HALF_ELF, "wood": RaceType.WOOD_HALF_ELF},
    "dwarf": {
        "emberheart": RaceType.EMBERHEART_DWARF,
        "stoneguard": RaceType.STONEGUARD_DWARF,
        "ironvein": RaceType.IRONVEIN_DWARF,
    },
    "halfling": {
        "swiftshadow": RaceType.SWIFTSHADOW_HALFLING,
        "hearthstone": RaceType.HEARTHSTONE_HALFLING,
    },
    "gnome": {
        "sylvan": RaceType.SYLVAN_GNOME,
        "dusk": RaceType.DUSK_GNOME,
        "hearth": RaceType.HEARTH_GNOME,
    },
    "nymph": RaceType.NYMPH,
    "orc": RaceType.ORC,
    "pyreling": {
        "emberkin": RaceType.EMBERKIN_PYRELING,
        "arcanist": RaceType.ARCANIST_PYRELING,
        "warbrand": RaceType.WARBRAND_PYRELING,
    },
}

_CLASS_INFO_DICT = {
    "artisan": "In the dance of creation and the craftsmanship of worlds, the Aristan weaves innovation and artistry into every tangible form.",
    "cleric": "Carrying a divine's mandate, the Cleric strides with purpose, a bastion of sacred power where faith's incandescent flame burns fiercely within.",
    "druid": "Bound to the rhythms of nature's deepest chants, the Druid communes with the ancient spirits of the wild, embracing the ebb and flow of the living land.",
    "fighter": "Forged in the crucible of combat, the Fighter stands undaunted, wielding martial prowess and unyielding bravery in the face of adversity.",
    "monk": "A disciple of inner harmony and disciplined focus, the Monk seeks enlightenment upon a path paved by contemplative strength and kinetic grace.",
    "paladin": "Sworn to uphold the confluence of valor and virtue, the Paladin wields both sword and piety with an unwavering resolve.",
    "ranger": "A wayfarer of the untrodden landscapes, the Ranger is the master of the wilds, their arrows as true as their intimate kinship with nature's secrets.",
    "rogue": "In the embrace of shadows and the subtlety of silence, the Rogue navigates a world unseen, where guild and finesse are the keys to survival and success.",
    "sorcerer": "Born of innate magical essence, the Sorcerer channels the raw energies of the arcane, their very blood a conduit for reality-altering forces.",
    "warlock": "Bound by pact to an eldritch entity, the Warlock wields otherwordly might, drawing upon forbidden secrets to manifest their dread patrons' will.",
    "warrior": "The quintessential embodiment of battle's ire, the Warrior matches their unrelenting ferocity with a robust tenacity for the clamor and clash of war.",
    "wizard": "A scholar of the esoteric and seeker of hidden truths, the Wizard commands the fabric of magic through meticulous study and unwavering discipline.",
}

_CLASS_MAPPING = {
    "artisan": ClassType.ARTISAN,
    "cleric": ClassType.CLERIC,
    "druid": ClassType.DRUID,
    "fighter": ClassType.FIGHTER,
    "monk": ClassType.MONK,
    "paladin": ClassType.PALADIN,
    "ranger": ClassType.RANGER,
    "rogue": ClassType.ROGUE,
    "sorcerer": ClassType.SORCERER,
    "warlock": ClassType.WARLOCK,
    "warrior": ClassType.WARRIOR,
    "wizard": ClassType.WIZARD,
}

_BACKGROUND_INFO_DICT = {
    "acolyte": "You have spent your life in service to a temple, learning sacred rites and providing sacrifices to the god or gods you worship. Serving the gods and discovering their sacred works will guide you to greatness.",
    "charlatan": "You're an expert in manipulation, prone to exaggeration, and more than happy to profit from it. Bending the truth and turning allies against each other will lead to greater success down the road.",
    "criminal": "You have a history of breaking the law and survive by leveraging less-than-legal connections. Profiting from criminal enterprise will lead to greater opportunities in the future.",
    "entertainer": "You live to sway and subvert your audience, engaging common crowds and high society alike. Preserving art and bringing joy to the hapless and downtrodden heightens your charismatic aura.",
    "folkhero": "You're the champion of the common people, challenging tyrants and monsters to protect the helpless. Saving innocents in imminent danger will make your legend grow.",
    "hermit": "You've lived in seclusion for years, away from society and the hardships of the world. Discovering hidden secrets and sharing them with others will bring you closer to the world.",
    "merchant": "Your skill in a particular craft has earned you membership in a mercantile guild, offering privileges and protection while engaging in your art. Repairing and discovering rare crafts will bring new inspiration.",
    "noble": "You were raised in a family among the social elite, accustomed to power and privilege. Accumulating renown, power, and loyalty will raise your status.",
    "outlander": "You grew up in the wilds, learning to survive far from the comforts of civilization. Surviving unusual hazards of the wild will enhance your prowess and understanding.",
    "sage": "You're curious and well-read, with an unending thirst for knowledge. Learning about rare lore of the world will inspire you to put this knowledge to greater purpose.",
    "sailor": "You've spent your life on the sea, learning the ins and outs of sailing and navigation. Surviving storms and other hazards of the sea will enhance your prowess and understanding.",
    "soldier": "You are trained in battlefield tactics and combat, having served in a militia, mercenary company, or officer corps. Show smart tactics and bravery on the battlefield to enhance your prowess.",
    "urchin": "After surviving a poor and bleak childhood, you know how to make the most out of very little. Using your street smarts bolsters your spirit for the journey ahead.",
}

_BACKGROUND_MAPPING = {
    "acolyte": BackgroundType.ACOLYTE,
    "charlatan": BackgroundType.CHARLATAN,
    "criminal": BackgroundType.CRIMINAL,
    "entertainer": BackgroundType.ENTERTAINER,
    "folkhero": BackgroundType.FOLK_HERO,
    "hermit": BackgroundType.HERMIT,
    "merchant": BackgroundType.MERCHANT,
    "noble": BackgroundType.NOBLE,
    "outlander": BackgroundType.OUTLANDER,
    "sage": BackgroundType.SAGE,
    "sailor": BackgroundType.SAILOR,
    "soldier": BackgroundType.SOLDIER,
    "urchin": BackgroundType.URCHIN,
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

        race_type = _RACE_SUBRACE_MAPPING.get(race)
        if isinstance(race_type, dict):
            race_type = race_type.get(subrace, None)

        if not race_type:
            caller.msg("An error occurred. Contact an administrator.")
            return "chargen_welcome"

        caller.race = race_type
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


def chargen_class(caller, raw_string, **kwargs):
    def _set_class(caller, **kwargs):
        selected_class = kwargs.get("selected_class", None)

        if not selected_class:
            caller.msg("An error occurred. Contact an administrator.")
            return "chargen_welcome"

        class_type = _CLASS_MAPPING.get(selected_class, None)
        caller.class_ = class_type
        return "chargen_background"

    selected_class = kwargs.get("selected_class", None)
    if selected_class:
        text = _CLASS_INFO_DICT[selected_class]
        options = (
            {
                "key": "y",
                "desc": f"Confirm {selected_class}",
                "goto": (_set_class, {"selected_class": selected_class}),
            },
            {
                "key": "n",
                "desc": "Return",
                "goto": ("chargen_class", {"selected_class": None}),
            },
        )
    else:
        text = dedent(
            """
            The void breathes - an exhalation of nebulous beauty, and as it does, a dreamscape coalesces from the expanse of endless potential. Colors unhdread of and light unknown to the waking world begin to dance before your senses, sculpting not a figure but the essence of self. From the formless, limbs stretch forth, reaching into the vastness as though testing the fabric of reality. A face emerges, eyes closed as if in peaceful repose, soon to open upon your new existence. Your presence, once only a thought, gains substance.

            Textures of the world write their legacy upon you. The softness of petals bestows a gentleness of touch, while the resilience of ancient bark imparts the steadfastness of soul. The dreamscape's water, pure and shimmering, caresses your form, granting fluidity to each nascent motion. Vibrations resonate through the intangible fibers of your being. Each note shapes a facet of character - courage, wisdom, and curiosity unfold like wings, preluding a flight into uncharted skies.

            The essence of will emerges, a guiding force within your forming hand. Firm yet ethereal, an unseen marker of your intentions, the silent declaration of your unborn strengths. Promsie fills the void - a theater of dreams, of life in potentia - and wraps around you in an embrace. Soft as silk and yet unyielding.
            """
        )
        options = []
        for class_name in _CLASS_INFO_DICT.keys():
            options.append(
                {
                    "key": class_name,
                    "goto": ("chargen_class", {"selected_class": class_name}),
                }
            )

    return text, options


def chargen_background(caller, raw_string, **kwargs):
    def _set_background(caller, **kwargs):
        background = kwargs.get("selected_background", None)

        if not background:
            caller.msg("An error occurred. Contact an administrator.")
            return "chargen_welcome"

        background = _BACKGROUND_MAPPING.get(background, None)
        caller.background = background
        return "chargen_appearance"

    selected_background = kwargs.get("selected_background", None)
    if selected_background:
        text = _BACKGROUND_INFO_DICT[selected_background]
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
            Memories, intangible yet vivid, paint upon the canvas of the void. You witness the strokes of struggles and triumphs, fleeting moments of joy and sorrow without discernible form. Fragments of these narratives, like leaves carried upon an unseen stream, drift past you. Their origins and destinations obscured, yet they hint at the rich soil from which your being has sprung. Tales of kinship, loss, laughter, and hardship softly tumble around you, each a color, a texture, in the portrait of life.

            Bright skies and storm clouds alike craft a backdrop without revealing the lands beneath. Echoes of past voices rise and fall in a quiet crescendo. Their words are muted, yet the emotions carried upon them resonate deeply, sculpting the contours of disposition and ethos.
            """
        )

        options = []
        for background in _BACKGROUND_INFO_DICT.keys():
            options.append(
                {
                    "key": background,
                    "goto": ("chargen_background", {"selected_background": background}),
                }
            )

    return text, options


def chargen_appearance(caller, raw_string, **kwargs):
    def _set_appearance(caller, appearance, **kwargs):
        appearance = appearance.strip()
        caller.db.desc = appearance
        return ("chargen_appearance", {"appearance": appearance})

    if not kwargs.get("appearance", None):
        text = dedent(
            """
            The void becomes a mirror of liquid silver. Your outline shimmers upon it, ephemeral and primed to accept the hues of existence. The dreamscape's palette brims with countless visages, eyes like polished gems, hair cascading in waves of imaginable textures and colors, skin tones capturing the spectrum of earthen clay to sun-kissed gold.
            """
        )

        options = (
            {"key": "", "goto": "chargen_appearance"},
            {"key": "_default", "goto": _set_appearance},
        )
    else:
        text = dedent(
            """
            The mirror of liquid silver reflects your appearance:
            
            {appearance}

            Is this correct?
            """.format(
                appearance=kwargs.get("appearance", "")
            )
        )
        options = (
            {"key": "y", "desc": "Confirm appearance", "goto": "chargen_attributes"},
            {
                "key": "n",
                "desc": "Return",
                "goto": ("chargen_appearance", {"appearance": None}),
            },
        )

    return text, options


def chargen_attributes(caller, raw_string, **kwargs):
    def _set_attributes(caller):
        if caller.class_ == ClassType.ARTISAN:
            caller.strength = 10
            caller.dexterity = 10
            caller.constitution = 10
            caller.intelligence = 14
            caller.wisdom = 14
            caller.charisma = 16
        elif caller.class_ == ClassType.CLERIC:
            caller.strength = 10
            caller.dexterity = 10
            caller.constitution = 10
            caller.intelligence = 14
            caller.wisdom = 16
            caller.charisma = 14
        elif caller.class_ == ClassType.DRUID:
            caller.strength = 10
            caller.dexterity = 10
            caller.constitution = 10
            caller.intelligence = 14
            caller.wisdom = 16
            caller.charisma = 14
        elif caller.class_ == ClassType.FIGHTER:
            caller.strength = 16
            caller.dexterity = 14
            caller.constitution = 14
            caller.intelligence = 10
            caller.wisdom = 10
            caller.charisma = 10
        elif caller.class_ == ClassType.MONK:
            caller.strength = 10
            caller.dexterity = 16
            caller.constitution = 14
            caller.intelligence = 10
            caller.wisdom = 14
            caller.charisma = 10
        elif caller.class_ == ClassType.PALADIN:
            caller.strength = 16
            caller.dexterity = 10
            caller.constitution = 14
            caller.intelligence = 10
            caller.wisdom = 10
            caller.charisma = 14
        elif caller.class_ == ClassType.RANGER:
            caller.strength = 14
            caller.dexterity = 16
            caller.constitution = 14
            caller.intelligence = 10
            caller.wisdom = 10
            caller.charisma = 10
        elif caller.class_ == ClassType.ROGUE:
            caller.strength = 10
            caller.dexterity = 16
            caller.constitution = 12
            caller.intelligence = 10
            caller.wisdom = 10
            caller.charisma = 16
        elif caller.class_ == ClassType.SORCERER:
            caller.strength = 10
            caller.dexterity = 10
            caller.constitution = 10
            caller.intelligence = 14
            caller.wisdom = 14
            caller.charisma = 16
        elif caller.class_ == ClassType.WARLOCK:
            caller.strength = 10
            caller.dexterity = 10
            caller.constitution = 10
            caller.intelligence = 14
            caller.wisdom = 14
            caller.charisma = 16
        elif caller.class_ == ClassType.WARRIOR:
            caller.strength = 16
            caller.dexterity = 12
            caller.constitution = 16
            caller.intelligence = 10
            caller.wisdom = 10
            caller.charisma = 10
        elif caller.class_ == ClassType.WIZARD:
            caller.strength = 10
            caller.dexterity = 10
            caller.constitution = 10
            caller.intelligence = 16
            caller.wisdom = 16
            caller.charisma = 12

        return "chargen_finalize"

    text = dedent(
        """
        As the final threads of your physical form intertwine, a new phase of creation yields, one that defines not the body, but the essence of your capabilities. It's a moment of introspection, a silent communion between you and the energies which animate the soul.

        The dreamscape, now more a feeling than a place, aligns with the resonance of your inner voice. It hums with the frequency of unseen strengths, a melody that only you can hear - a harmony that beckons you to claim it as your own.
        """
    )

    options = (
        {"key": "", "goto": "chargen_attributes"},
        # {
        #    "key": "simple",
        #    "desc": "Accept the default attributes for your class.",
        #    "goto": _set_attributes,
        # },
        {
            "key": "detailed",
            "desc": "Choose your own attributes.",
            "goto": "chargen_attributes_detailed",
        },
        {"key": "_default", "goto": "chargen_attributes"},
    )

    return text, options


def chargen_attributes_detailed(caller, raw_string, **kwargs):
    ATTRIBUTES = [
        "strength",
        "dexterity",
        "constitution",
        "intelligence",
        "wisdom",
        "charisma",
    ]
    TOTAL_POINTS = 75
    MIN_ATTRIBUTE_VALUE = 8
    MAX_ATTRIBUTE_VALUE = 16

    def calculate_points_used(caller):
        return sum(getattr(caller, attr, 0) for attr in ATTRIBUTES)

    def _set_attribute(caller, allocation, **kwargs):
        attribute, value = allocation.split(" ")
        value = int(value.strip())

        if attribute not in ATTRIBUTES:
            caller.msg("An error occurred. Contact an administrator.")
            return "chargen_attributes_detailed"

        if not (MIN_ATTRIBUTE_VALUE <= value <= MAX_ATTRIBUTE_VALUE):
            caller.msg(
                f"Attribute values must be between {MIN_ATTRIBUTE_VALUE} and {MAX_ATTRIBUTE_VALUE}."
            )
            return "chargen_attributes_detailed"

        current_value = getattr(caller, attribute, 0)
        points_used = calculate_points_used(caller)
        additional_points_needed = value - current_value

        if points_used + additional_points_needed > TOTAL_POINTS:
            caller.msg("You don't have enough points remaining.")
            return "chargen_attributes_detailed"

        setattr(caller, attribute, value)
        return "chargen_attributes_detailed"

    points_used = calculate_points_used(caller)
    points_remaining = TOTAL_POINTS - points_used

    help = dedent(
        """
        Strength: Enhances physical prowess in melee combat, improves carrying capacity, and augments certain physical actions.

        Dexterity: Boosts precision and agility, influences armor effectiveness, and is crucial for avoiding certain hazards.

        Constitution: Vital for overall health, resisting certain ailments, and enduring the effects of debilitating conditions. 

        Intelligence: Governs the depth of knowledge and arcane mastery, affecting the capability to unravel mysteries, recall lesser-known lore, and is the key for magic wielded by more scholarly adventurers.

        Wisdom: Reflects awareness and intuition, key to perceiving the world and its creatures, influencing survival and is primary for divine or nature-based adventurers.

        Charisma: Represents personal magnetism and strength of character, crucial for those who rely on their personality to succeed, and impacts social interactions.
        """
    )
    text = dedent(
        """
        Your attributes: STR: {strength}, DEX: {dexterity}, CON: {constitution}, INT: {intelligence}, WIS: {wisdom}, CHA: {charisma}

        Points Remaining: {points_remaining}

        Use the following command to set your attributes:
                 <attribute> <value>
        Example: strength 10. Value must be between 8 and 16.
        """
    ).format(
        strength=caller.strength,
        dexterity=caller.dexterity,
        constitution=caller.constitution,
        intelligence=caller.intelligence,
        wisdom=caller.wisdom,
        charisma=caller.charisma,
        points_remaining=points_remaining,
    )

    options = (
        {"key": "", "goto": "chargen_abilities_detailed"},
        {"key": "y", "desc": "Confirm attributes", "goto": "chargen_finalize"},
        {"key": "_default", "goto": _set_attribute},
    )

    return (text, help), options


def chargen_finalize(caller, raw_string):
    return "", ""
