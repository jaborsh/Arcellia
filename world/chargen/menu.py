from evennia.utils import dedent

from world.characters import appearances, backgrounds, classes, genders, races

_RACE_INFO_DICT = {
    "human": "|YHumans|n:\n\nThe most common face to see in Arcellia, humans are known for their tenacity, creativity, and endless capacity for growth.",  # noqa: E501
    "elf": "|YElves|n:\n\nElves of Arcellia embody an ageless grace, their histories etched into the very forests and rivers of the world. Ancient and wise, they live in harmonious synchrony with the natural tapestry that surrounds them, their lifelines stretching across eras like the boughs of the World Tree. With eyes that reflect the depth of the stars, elves harbor a mastery over magic few can rival, their arcane heritage as intrinsic as the wind's whisper. Bound by traditions woven through the fabric of time, they walk paths shadowed by lore, their existence a melody harmonizing with the ethereal song of eternity.",  # noqa: E501
    "dwarf": "|YDwarves|n:\n\nAs durable and unyielding as their homes of stone, dwarves are some of the finest warriors, miners, and smiths in all of Arcellia. They're known for their confidence and keen intuition, valuing family, ritual, and fine craftsmanship. Many of their ancient kingdoms have been surrendered to goblins and other creatures of the deep.",  # noqa: E501
    "gnome": "|YGnomes|n:\n\nGnomes are diminutive, inquisitive inventors, their minds ever-ticking gears amidst a whirlwind of arcane intellect. They thrive on innovation, their lives a constant pursuit of knowledge, enchantment, and mechanical wonders that teeter on the brink of whimsy and genius.",  # noqa: E501
    "nymph": "|YNymphs|n:\n\nEach Nymphkind bears an Elemental Allure, an innate charm that captures hearts as effortlessly as the elements wield their power. These beguiling beings breathe an otherworldly magnetism, entwining those who fall under their gaze with strands of lust, adoration, or sheer bewitchment. Like the ripples upon a still pond or the flickering dance of flames, their seductive powers manifest in various forms, reflecting the vast spectrum of their ancestral realm.",  # noqa: E501
    "orc": "|YOrcs|n:\n\nOrcs exhibit widely varying appearances. Creatures of intense emotion, the orcs are more inclined to act than contemplate - whether the rage burning their bodies compels them to fight, or the love of filling their hearts inspires acts of incredible kindness.",  # noqa: E501
    "pyreling": "|YPyrelings|n:\n\nThe Pyreling are descendents cloaked in myth, born of the mingling between mortal essence and the enigmatic energies of hell. They carry within them a flickering flame that manifests in eyes that glow like coals and skin in shades of smoldering dusk. Misunderstood by many, the Pyrelings wander through Arcellia bearing gifts of arcane affinity, as well as a propensity for the extraordinary, often leaving tales of fear and fascination in their wake.",  # noqa: E501
}

_SUBRACE_INFO_DICT = {
    "elf": {
        "high": "|YHigh Elves|n:\n\nThe High Elves, ethereal as the twilight heavens, draw their lineage from the stars. With minds sharp as the crescent moon, they are curators of arcane wisdom, their lives as elongated as the very eternities they study. Their enclaves, built where ley lines converge, resonate with the harmonious magic of the firmament, reflecting the astral glory of their heritage in every spell they weave and every blade they forge under the watchful eyes of the constellations.",  # noqa: E501
        "night": "|YNight Elves|n:\n\nIt was they who first delved deep into the arcane arts, their insatiable curiosity unraveling the fabric of reality nearly a millennia past. The night elves' unbridled use of sorcery summoned forth cataclysmic force that ignited a war of unspeakable devastation between mortals and entities of pure destruction. Only through immense sacrifice did the night elves drive back this ruinous presence, preserving the world at the dire cost of their own splendid realm, now lost beneath relentless tides.",
        "wood": "|YWood Elves|n:\n\nBeneath emerald canopies, where life thrums in every leaf and branch, dwell the Wood Elves. Their souls are the voice of the forest, as serene as still water and as wild as the untamed grove. These elves are guardians of the natural world, moving with a grace that matches the swaying boughs and flowing streams, their instincts finely honed to the rhythm of the wilderness. Bridging the material plane and the natural realm in harmonious co-existence, Wood Elves invoke the vitality of the woods in their tireless defense against those who would despoil their verdant home.",  # noqa: E501
    },
    "dwarf": {
        "emberheart": "|YEmberheart Dwarves|n:\n\nThe Emberheart Dwarves glow with an inner fire, their souls alight with consummate confidence and a sharp, unerring insight. Celebrated for their intricate craftsmanship and elaborate ceremonies, the Emberhearts dwell within the grand vocanic forges of the Molten Hold, where kinship and artistry burn brighter than the furnaces that warm their halls.",  # noqa: E501
        "stoneguard": "|YStoneguard Dwarves|n:\n\nBearing the weight of history upon their broad shoulders, Stoneguard Dwarves have weathered the collapse of their once-mighty bastions, stoically surrendering their dominion to the relentless advance of goblin hordes and orcish legions. With hearts like the bedrock they cleave, these Dwarves nurture a collective resilience, driven by a cynical yet unwavering resolve to reclaim the glory and the halls of their ancestors.",  # noqa: E501
        "ironvein": "|YIronvein Dwarves|n:\n\nForged in the dark crucible of the world's underbelly, the Ironvein Dwarves trace their lineage through centuries spent in the eerie expanses of the deep. Exposed to mysteries that warp mind and matter, imbued with the arcane residue that pulses through their cavernous abyss, they have emerged with esoteric powers that are both a gift and a legacy of old tyrannies. Survival meant enduring cruel manipulation by aberrant overlords, and from such depths of despair rose the fortitude and psionic might that now courses through the veins of these steely-eyed survivors. Though the chains of the past have been cast off, the Ironveins have never forgotten the cold embrace of subjugation, nor the sweet taste of hard-won freedom.",  # noqa: E501
    },
    "gnome": {
        "sylvan": "|YSylvan Gnomes|n:\n\nSylvan Gnomes, sprightly and secretive as the woodland sprites, dwell amidst the verdant groves and dappled glades of Arcellia's vast forests. Whispering to the trees and laughing with the brooks, they are unseen keepers of nature's most secluded riddles, guarding the sylvan sanctuaries against those who would dare disturb them. With an affinity for the woods, these Gnomes craft enchantments as delicate as cobwebs, and their laughter is as fleeting as the wind through the leaves.",  # noqa: E501
        "dusk": "|YDusk Gnomes|n:\n\nVeiled in mystery and born of the shadowy embrace of the subterranean world, Dusk Gnomes traverse the hidden depths with a grace that belies their surroundings. Illuminated by the faint glow of luminescent fungi and echoing caverns, they are silent witnesses to secrets entombed in stone. Masters of quietude and guile, Dusk Gnomes navigate the labyrinthine underworld with an innate understanding that is as profound as the ancient darkness from which they emerge.",  # noqa: E501
        "hearth": "|YHearth Gnomes|n:\n\nAn embodiment of scrupulous ingenuity and unshakable stability, Hearth Gnomes thrive within the heart of bustling communities or quaint hamlets. With hands weathered by toil, yet as precise as a master clockmaker's, they churn out marvels of craftsmanship and innovation. Hearth Gnomes are the cornerstone of tradition, etching each day's labor into the enduring legacy of their kin. Their tenacious spirits are akin to the enduring stone, shaping society with the chisel of their relentless pursuit of excellence and progress.",  # noqa: E501
    },
    "pyreling": {
        "emberkin": "|YEmberkin Pyrelings|n:\n\nEmberkin Pyrelings harbor the essence of smoldering embers and soul-deep shadows. Their lineage serves as a conduit for fiery dominion, allowing them to summon both the scalding wrath and the obsidian shroud of their fearsome forefathers.",  # noqa: E501
        "arcanist": "|YArcanist Pyrelings|n:\n\nThe Arcanist Pyrelings trace their heritage to the inscrutable compact with the grand magus of the Infernal. These Pyrelings are imbued with an arcane reservoir, deep and vast, granting them an affinity for the eldritch arts that is both singular and potent. With a mere incantation, they can bend the weft of magical energies to their will, shaping the fabric of spellcraft with ease.",  # noqa: E501
        "warbrand": "|YWarbrand Pyrelings|n:\n\nForged in the martial traditions of the fiery fortresses, Warbrand Pyrelings are the progeny of pacts with war-torn overlords. Their very beings thrum with martial prowess and the relentless surge of the inferno that fuels their relentless spirit.",  # noqa: E501
    },
}

_CLASS_INFO_DICT = {
    "cleric": "|wClerics|n:\n\nCarrying a divine's mandate, the Cleric strides with purpose, a bastion of sacred power where faith's incandescent flame burns fiercely within.",
    "druid": "|gDruids|n:\n\nKeepers of the world and masters of nature, the Druid commands Arcellia's wrath, capable of a diverse range of environmental abilities.",
    "hunter": "|GHunters|n:\n\nDeadly marksmen and skilled survivalists, the Hunter possesses a primal connection with beasts of all types, capable of training them as loyal companions.",
    "mage": "|mMages|n:\n\nA scholar of the esoteric and seeker of hidden truths, the Mage commands the fabric of magic through meticulous study and unwavering discipline.",
    "merchant": "|yMerchants|n:\n\nIn the dance of creation and the craftsmanship of worlds, the Merchant weaves innovation and artistry into every tangible form.",
    "paladin": "|cPaladins|n:\n\nSworn to uphold the confluence of valor and virtue, the Paladin wields both sword and piety with an unwavering resolve.",
    "rogue": "|xRogues|n:\n\nIn the embrace of shadows and the subtlety of silence, the Rogue navigates a world unseen, where guild and finesse are the keys to survival and success.",
    "shaman": "|CShaman|n:\n\nThe spiritual leaders of tribes and clans. The Shaman use their connection to the spirit world to unleash fury upon their foes.",
    "warlock": "|MWarlocks|n:\n\nBound by pact to an eldritch entity, the Warlock wields otherwordly might, drawing upon forbidden secrets to manifest their dread patrons' will.",
    "warrior": "|rWarriors|n:\n\nThe quintessential embodiment of battle's ire, the Warrior matches their unrelenting ferocity with a robust tenacity for the clamor and clash of war.",
}

_BACKGROUND_INFO_DICT = {
    "acolyte": "|YAcolyte|n:\n\nYou have spent your life in service to a temple, learning sacred rites and providing sacrifices to the god or gods you worship. Serving the gods and discovering their sacred works will guide you to greatness.",
    "charlatan": "|YCharlatan|n:\n\nYou're an expert in manipulation, prone to exaggeration, and more than happy to profit from it. Bending the truth and turning allies against each other will lead to greater success down the road.",
    "criminal": "|YCriminal|n:\n\nYou have a history of breaking the law and survive by leveraging less-than-legal connections. Profiting from criminal enterprise will lead to greater opportunities in the future.",
    "entertainer": "|YEntertainer|n:\n\nYou live to sway and subvert your audience, engaging common crowds and high society alike. Preserving art and bringing joy to the hapless and downtrodden heightens your charismatic aura.",
    "folkhero": "|YFolk Hero|n:\n\nYou're the champion of the common people, challenging tyrants and monsters to protect the helpless. Saving innocents in imminent danger will make your legend grow.",
    "hermit": "|YHermit|n:\n\nYou've lived in seclusion for years, away from society and the hardships of the world. Discovering hidden secrets and sharing them with others will bring you closer to the world.",
    "merchant": "|YMerchant|n:\n\nYour skill in a particular craft has earned you membership in a mercantile guild, offering privileges and protection while engaging in your art. Repairing and discovering rare crafts will bring new inspiration.",
    "noble": "|YNoble|n:\n\nYou were raised in a family among the social elite, accustomed to power and privilege. Accumulating renown, power, and loyalty will raise your status.",
    "outlander": "|YOutlander|n:\n\nYou grew up in the wilds, learning to survive far from the comforts of civilization. Surviving unusual hazards of the wild will enhance your prowess and understanding.",
    "sage": "|YSage|n:\n\nYou're curious and well-read, with an unending thirst for knowledge. Learning about rare lore of the world will inspire you to put this knowledge to greater purpose.",
    "sailor": "|YSailor|n:\n\nYou've spent your life on the sea, learning the ins and outs of sailing and navigation. Surviving storms and other hazards of the sea will enhance your prowess and understanding.",
    "soldier": "|YSoldier|n:\n\nYou are trained in battlefield tactics and combat, having served in a militia, mercenary company, or officer corps. Show smart tactics and bravery on the battlefield to enhance your prowess.",
    "urchin": "|YUrchin|n:\n\nAfter surviving a poor and bleak childhood, you know how to make the most out of very little. Using your street smarts bolsters your spirit for the journey ahead.",
}


def chargen_welcome(caller):
    def _set_gender(caller, choice):
        choice = choice.strip().lower()[0]
        if choice in ("1", "m"):
            caller.character.add(
                "gender",
                "Gender",
                trait_type="trait",
                value=genders.CharacterGender.MALE,
            )
        elif choice in ("2", "f"):
            caller.character.add(
                "gender", "Gender", value=genders.CharacterGender.FEMALE
            )
        elif choice in ("3", "a"):
            caller.character.add(
                "gender", "Gender", value=genders.CharacterGender.ANDROGYNOUS
            )
        else:
            return "chargen_welcome"

        return "chargen_race"

    text = dedent(
        """\
        You, the nascent traveler, float amidst this gentle void. A mere wisp of consciousness, you harbor the power to mold your very essence. Here in this prelude to adventure, the choice of one's very existence is the first dalliance with creation.
        
        At the center of this void, three figures emerge from the nebulous gray, standing as pillars of potentiality. The first, a male figure, basks in a soft radiance akin to the sun's embrace, his strength and grace woven in harmony. Beside him, a female figure exudes a gentle luminescence reminiscent of the moon's tender caress, her elegance dancing in union with resilience. Between them, an androgynous figure radiates an ethereal light, a fusion of sun and moon.

        In this moment, suspended between the not-yet-shaped and the eternal, a question crystallizes before your burgeoning self.

        |CSelect your Gender|n:
        """  # noqa: E501
    )

    options = (
        {"key": "", "goto": "chargen_welcome"},
        {"key": ("1", "male", "m"), "desc": "Male", "goto": _set_gender},
        {"key": ("2", "female", "f"), "desc": "Female", "goto": _set_gender},
        {"key": ("3", "androgynous", "a"), "desc": "Androgynous", "goto": _set_gender},
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

        if subrace:
            race_type = f"{subrace} {race}"
        else:
            race_type = f"{race}"

        race_type = races.race_registry.get(race_type)

        if not race_type:
            caller.msg("An error occurred. Contact an administrator.")
            return "chargen_welcome"

        caller.character.add("race", "Race", trait_type="trait", value=race_type)
        return "chargen_class"

    selected_race = kwargs.get("selected_race", None)
    selected_subrace = kwargs.get("selected_subrace", "")

    if selected_subrace:
        text = _SUBRACE_INFO_DICT[selected_race][selected_subrace] + "\n"
    elif selected_race:
        text = _RACE_INFO_DICT[selected_race] + "\n"
    else:
        text = dedent(
            """
            Majestic landscapes unfold around you, a canvas for ethnic identities roaming within the bounds of thought. Mighty mountainscapes craft silhouettes against the sky, where the kin of giants and dwarves could forge their legacies in stone and steel. Lush forests carpet the realms below, bearing the sagas of elves and faefolk, their lifespans entwined with the ageless trees. Vast plains stretch out, horizons unbroken, where the footsteps of nomadic tribes echo with the steadfast will of orcish clans. Deep waters shimmer, hiding the secretive abodes of merfolk and naiads, whose songs thread through the currents, weaving stories of depth and mystery.

            Time teems on the brink of stillness, waiting for you to reach out and grasp the thread of existence calling to your spirit.

            |CSelect your Race|n:
            """  # noqa: E501
        )

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


def chargen_class(caller, raw_string, **kwargs):
    def _set_class(caller, **kwargs):
        selected_class = kwargs.get("selected_class", None)

        class_type = classes.class_registry.get(selected_class)

        if not class_type:
            caller.msg("An error occurred. Contact an administrator.")
            return "chargen_welcome"

        caller.character.add(
            "character_class", "Class", trait_type="trait", value=class_type
        )
        return "chargen_background"

    selected_class = kwargs.get("selected_class", None)
    if selected_class:
        text = _CLASS_INFO_DICT[selected_class] + "\n\n|CConfirm your Class|n:"
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

            |CSelect your Class|n:
            """
        )
        options = []
        i = 0
        for class_name in _CLASS_INFO_DICT.keys():
            i += 1
            options.append(
                {
                    "key": (str(i), class_name),
                    "desc": class_name.capitalize(),
                    "goto": ("chargen_class", {"selected_class": class_name}),
                }
            )

    return text, options


def chargen_background(caller, raw_string, **kwargs):
    def _set_background(caller, **kwargs):
        background = kwargs.get("selected_background", None)
        background = backgrounds.background_registry.get(background)

        if not background:
            caller.msg("An error occurred. Contact an administrator.")
            return "chargen_welcome"

        caller.character.add(
            "background", "Background", trait_type="trait", value=background
        )
        return "chargen_appearance"

    selected_background = kwargs.get("selected_background", None)
    if selected_background:
        text = (
            _BACKGROUND_INFO_DICT[selected_background]
            + "\n\n|CConfirm your Background|n:"
        )
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

            |CSelect your Background|n:
            """
        )

        options = []
        i = 0
        for background in _BACKGROUND_INFO_DICT.keys():
            i += 1
            options.append(
                {
                    "key": (str(i), background),
                    "desc": background.capitalize(),
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

            |CWrite your appearance or select an option|n:
            """
        )

        options = (
            {"key": "", "goto": "chargen_appearance"},
            {"key": ("1", "height"), "desc": "Height", "goto": "appearance_height"},
            {
                "key": ("2", "body", "body type"),
                "desc": "Body Type",
                "goto": "appearance_body",
            },
            {
                "key": ("3", "eye color", "ec"),
                "desc": "Eye Color",
                "goto": "appearance_eye_color",
            },
            {
                "key": ("4", "hair color", "hc"),
                "desc": "Hair Color",
                "goto": "appearance_hair_color",
            },
            {
                "key": ("5", "skin type", "st"),
                "desc": "Skin Type",
                "goto": "appearance_skin_type",
            },
            {
                "key": ("6", "eye type", "et"),
                "desc": "Eye Type",
                "goto": "appearance_eye_type",
            },
            {
                "key": ("7", "nose type", "nt"),
                "desc": "Nose Type",
                "goto": "appearance_nose_type",
            },
            {
                "key": ("8", "mouth type", "mt"),
                "desc": "Mouth Type",
                "goto": "appearance_mouth_type",
            },
            {
                "key": ("9", "f", "finalize"),
                "desc": "Finalize Appearance",
                "goto": "chargen_finalize",
            },
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
            {"key": "y", "desc": "Confirm appearance", "goto": "chargen_finalize"},
            {
                "key": "n",
                "desc": "Return",
                "goto": ("chargen_appearance", {"appearance": None}),
            },
        )

    return text, options


def appearance_body(caller, raw_string, **kwargs):
    def _set_body(caller, **kwargs):
        body = kwargs.get("body", None)
        if body == "petite":
            caller.appearance.add(
                "body_type",
                "Body Type",
                trait_type="trait",
                value=appearances.CharacterBodyType.PETITE,
            )
        elif body == "slender":
            caller.appearance.add(
                "body_type",
                "Body Type",
                trait_type="trait",
                value=appearances.CharacterBodyType.SLENDER,
            )
        elif body == "average":
            caller.appearance.add(
                "body_type",
                "Body Type",
                trait_type="trait",
                value=appearances.CharacterBodyType.AVERAGE,
            )
        elif body == "athletic":
            caller.appearance.add(
                "body_type",
                "Body Type",
                trait_type="trait",
                value=appearances.CharacterBodyType.ATHLETIC,
            )
        elif body == "robust":
            caller.appearance.add(
                "body_type",
                "Body Type",
                trait_type="trait",
                value=appearances.CharacterBodyType.ROBUST,
            )
        else:
            return "chargen_appearance"

        return "chargen_appearance"

    text = "|CSelect your Body Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_body"},
        {
            "key": ("1", "petite", "p"),
            "desc": "Petite",
            "goto": (_set_body, {"body": "petite"}),
        },
        {
            "key": ("2", "slender", "s"),
            "desc": "Slender",
            "goto": (_set_body, {"body": "slender"}),
        },
        {
            "key": ("3", "average", "av"),
            "desc": "Average",
            "goto": (_set_body, {"body": "average"}),
        },
        {
            "key": ("4", "athletic", "at"),
            "desc": "Athletic",
            "goto": (_set_body, {"body": "athletic"}),
        },
        {
            "key": ("5", "robust", "r"),
            "desc": "Robust",
            "goto": (_set_body, {"body": "robust"}),
        },
        {"key": "_default", "goto": "chargen_appearance"},
    )

    return text, options


def appearance_height(caller, raw_string, **kwargs):
    def _set_height(caller, **kwargs):
        height = kwargs.get("height", None)
        if height == "short":
            caller.appearance.add(
                "height",
                "Height",
                trait_type="trait",
                value=appearances.CharacterHeight.SHORT,
            )
        elif height == "average":
            caller.appearance.add(
                "height",
                "Height",
                trait_type="trait",
                value=appearances.CharacterHeight.AVERAGE,
            )
        elif height == "tall":
            caller.appearance.add(
                "height",
                "Height",
                trait_type="trait",
                value=appearances.CharacterHeight.TALL,
            )
        else:
            return "chargen_appearance"

        return "chargen_appearance"

    text = "|CSelect your Height|n:\n"
    options = (
        {"key": "", "goto": "appearance_height"},
        {
            "key": ("1", "short", "sh"),
            "desc": "Short",
            "goto": (_set_height, {"height": "short"}),
        },
        {
            "key": ("2", "average", "av"),
            "desc": "Average",
            "goto": (_set_height, {"height": "average"}),
        },
        {
            "key": ("3", "tall", "t"),
            "desc": "Tall",
            "goto": (_set_height, {"height": "tall"}),
        },
        {"key": "_default", "goto": "chargen_appearance"},
    )

    return text, options


def appearance_eye_color(caller, raw_string, **kwargs):
    def _set_eye_color(caller, **kwargs):
        eye_color = kwargs.get("eye_color", None)
        if eye_color == "amber":
            caller.appearance.add(
                "eye_color",
                "Eye Color",
                trait_type="trait",
                value=appearances.CharacterEyeColor.AMBER,
            )
        elif eye_color == "blue":
            caller.appearance.add(
                "eye_color",
                "Eye Color",
                trait_type="trait",
                value=appearances.CharacterEyeColor.BLUE,
            )
        elif eye_color == "brown":
            caller.appearance.add(
                "eye_color",
                "Eye Color",
                trait_type="trait",
                value=appearances.CharacterEyeColor.BROWN,
            )
        elif eye_color == "green":
            caller.appearance.add(
                "eye_color",
                "Eye Color",
                trait_type="trait",
                value=appearances.CharacterEyeColor.GREEN,
            )
        elif eye_color == "grey":
            caller.appearance.add(
                "eye_color",
                "Eye Color",
                trait_type="trait",
                value=appearances.CharacterEyeColor.GREY,
            )
        elif eye_color == "hazel":
            caller.appearance.add(
                "eye_color",
                "Eye Color",
                trait_type="trait",
                value=appearances.CharacterEyeColor.HAZEL,
            )
        elif eye_color == "black":
            caller.appearance.add(
                "eye_color",
                "Eye Color",
                trait_type="trait",
                value=appearances.CharacterEyeColor.BLACK,
            )
        elif eye_color == "copper":
            caller.appearance.add(
                "eye_color",
                "Eye Color",
                trait_type="trait",
                value=appearances.CharacterEyeColor.COPPER,
            )
        elif eye_color == "crimson":
            caller.appearance.add(
                "eye_color",
                "Eye Color",
                trait_type="trait",
                value=appearances.CharacterEyeColor.CRIMSON,
            )
        elif eye_color == "emerald":
            caller.appearance.add(
                "eye_color",
                "Eye Color",
                trait_type="trait",
                value=appearances.CharacterEyeColor.EMERALD,
            )
        elif eye_color == "gold":
            caller.appearance.add(
                "eye_color",
                "Eye Color",
                trait_type="trait",
                value=appearances.CharacterEyeColor.GOLD,
            )
        elif eye_color == "opal":
            caller.appearance.add(
                "eye_color",
                "Eye Color",
                trait_type="trait",
                value=appearances.CharacterEyeColor.OPAL,
            )
        elif eye_color == "onyx":
            caller.appearance.add(
                "eye_color",
                "Eye Color",
                trait_type="trait",
                value=appearances.CharacterEyeColor.ONYX,
            )
        elif eye_color == "red":
            caller.appearance.add(
                "eye_color",
                "Eye Color",
                trait_type="trait",
                value=appearances.CharacterEyeColor.RED,
            )
        elif eye_color == "sapphire":
            caller.appearance.add(
                "eye_color",
                "Eye Color",
                trait_type="trait",
                value=appearances.CharacterEyeColor.SAPPHIRE,
            )
        elif eye_color == "silver":
            caller.appearance.add(
                "eye_color",
                "Eye Color",
                trait_type="trait",
                value=appearances.CharacterEyeColor.SILVER,
            )
        elif eye_color == "violet":
            caller.appearance.add(
                "eye_color",
                "Eye Color",
                trait_type="trait",
                value=appearances.CharacterEyeColor.VIOLET,
            )
        elif eye_color == "white":
            caller.appearance.add(
                "eye_color",
                "Eye Color",
                trait_type="trait",
                value=appearances.CharacterEyeColor.WHITE,
            )
        else:
            return "chargen_appearance"

        return "chargen_appearance"

    text = "|CSelect your Eye Color|n:\n"
    options = (
        {"key": "", "goto": "appearance_eye_color"},
        {
            "key": ("1", "amber", "a"),
            "desc": "Amber",
            "goto": (_set_eye_color, {"eye_color": "amber"}),
        },
        {
            "key": ("2", "blue", "b"),
            "desc": "Blue",
            "goto": (_set_eye_color, {"eye_color": "blue"}),
        },
        {
            "key": ("3", "brown", "br"),
            "desc": "Brown",
            "goto": (_set_eye_color, {"eye_color": "brown"}),
        },
        {
            "key": ("4", "green", "g"),
            "desc": "Green",
            "goto": (_set_eye_color, {"eye_color": "green"}),
        },
        {
            "key": ("5", "grey", "gr"),
            "desc": "Grey",
            "goto": (_set_eye_color, {"eye_color": "grey"}),
        },
        {
            "key": ("6", "hazel", "h"),
            "desc": "Hazel",
            "goto": (_set_eye_color, {"eye_color": "hazel"}),
        },
        {
            "key": ("7", "black", "bl"),
            "desc": "Black",
            "goto": (_set_eye_color, {"eye_color": "black"}),
        },
        {
            "key": ("8", "copper", "c"),
            "desc": "Copper",
            "goto": (_set_eye_color, {"eye_color": "copper"}),
        },
        {
            "key": ("9", "crimson", "cr"),
            "desc": "Crimson",
            "goto": (_set_eye_color, {"eye_color": "crimson"}),
        },
        {
            "key": ("10", "emerald", "e"),
            "desc": "Emerald",
            "goto": (_set_eye_color, {"eye_color": "emerald"}),
        },
        {
            "key": ("11", "gold", "go"),
            "desc": "Gold",
            "goto": (_set_eye_color, {"eye_color": "gold"}),
        },
        {
            "key": ("12", "opal", "o"),
            "desc": "Opal",
            "goto": (_set_eye_color, {"eye_color": "opal"}),
        },
        {
            "key": ("13", "onyx", "on"),
            "desc": "Onyx",
            "goto": (_set_eye_color, {"eye_color": "onyx"}),
        },
        {
            "key": ("14", "red", "r"),
            "desc": "Red",
            "goto": (_set_eye_color, {"eye_color": "red"}),
        },
        {
            "key": ("15", "sapphire", "sa"),
            "desc": "Sapphire",
            "goto": (_set_eye_color, {"eye_color": "sapphire"}),
        },
        {
            "key": ("16", "silver", "si"),
            "desc": "Silver",
            "goto": (_set_eye_color, {"eye_color": "silver"}),
        },
        {
            "key": ("17", "violet", "v"),
            "desc": "Violet",
            "goto": (_set_eye_color, {"eye_color": "violet"}),
        },
        {
            "key": ("18", "white", "w"),
            "desc": "White",
            "goto": (_set_eye_color, {"eye_color": "white"}),
        },
        {"key": "_default", "goto": "chargen_appearance"},
    )

    return text, options


def appearance_hair_color(caller, raw_string, **kwargs):
    def _set_hair_color(caller, **kwargs):
        hair_color = kwargs.get("hair_color", None)
        if hair_color == "auburn":
            caller.appearance.add(
                "hair_color",
                "Hair Color",
                trait_type="trait",
                value=appearances.CharacterHairColor.AUBURN,
            )
        elif hair_color == "black":
            caller.appearance.add(
                "hair_color",
                "Hair Color",
                trait_type="trait",
                value=appearances.CharacterHairColor.BLACK,
            )
        elif hair_color == "blonde":
            caller.appearance.add(
                "hair_color",
                "Hair Color",
                trait_type="trait",
                value=appearances.CharacterHairColor.BLONDE,
            )
        elif hair_color == "brown":
            caller.appearance.add(
                "hair_color",
                "Hair Color",
                trait_type="trait",
                value=appearances.CharacterHairColor.BROWN,
            )
        elif hair_color == "grey":
            caller.appearance.add(
                "hair_color",
                "Hair Color",
                trait_type="trait",
                value=appearances.CharacterHairColor.GREY,
            )
        elif hair_color == "red":
            caller.appearance.add(
                "hair_color",
                "Hair Color",
                trait_type="trait",
                value=appearances.CharacterHairColor.RED,
            )
        elif hair_color == "white":
            caller.appearance.add(
                "hair_color",
                "Hair Color",
                trait_type="trait",
                value=appearances.CharacterHairColor.WHITE,
            )
        elif hair_color == "blue":
            caller.appearance.add(
                "hair_color",
                "Hair Color",
                trait_type="trait",
                value=appearances.CharacterHairColor.BLUE,
            )
        elif hair_color == "green":
            caller.appearance.add(
                "hair_color",
                "Hair Color",
                trait_type="trait",
                value=appearances.CharacterHairColor.GREEN,
            )
        elif hair_color == "pink":
            caller.appearance.add(
                "hair_color",
                "Hair Color",
                trait_type="trait",
                value=appearances.CharacterHairColor.PINK,
            )
        elif hair_color == "purple":
            caller.appearance.add(
                "hair_color",
                "Hair Color",
                trait_type="trait",
                value=appearances.CharacterHairColor.PURPLE,
            )
        elif hair_color == "silver":
            caller.appearance.add(
                "hair_color",
                "Hair Color",
                trait_type="trait",
                value=appearances.CharacterHairColor.SILVER,
            )
        elif hair_color == "teal":
            caller.appearance.add(
                "hair_color",
                "Hair Color",
                trait_type="trait",
                value=appearances.CharacterHairColor.TEAL,
            )
        elif hair_color == "yellow":
            caller.appearance.add(
                "hair_color",
                "Hair Color",
                trait_type="trait",
                value=appearances.CharacterHairColor.YELLOW,
            )
        else:
            return "chargen_appearance"

        return "chargen_appearance"

    text = "|CSelect your Hair Color|n:\n"
    options = (
        {"key": "", "goto": "appearance_hair_color"},
        {
            "key": ("1", "auburn", "a"),
            "desc": "Auburn",
            "goto": (_set_hair_color, {"hair_color": "auburn"}),
        },
        {
            "key": ("2", "black", "bl"),
            "desc": "Black",
            "goto": (_set_hair_color, {"hair_color": "black"}),
        },
        {
            "key": ("3", "blonde", "b"),
            "desc": "Blonde",
            "goto": (_set_hair_color, {"hair_color": "blonde"}),
        },
        {
            "key": ("4", "brown", "br"),
            "desc": "Brown",
            "goto": (_set_hair_color, {"hair_color": "brown"}),
        },
        {
            "key": ("5", "grey", "gr"),
            "desc": "Grey",
            "goto": (_set_hair_color, {"hair_color": "grey"}),
        },
        {
            "key": ("6", "red", "r"),
            "desc": "Red",
            "goto": (_set_hair_color, {"hair_color": "red"}),
        },
        {
            "key": ("7", "white", "w"),
            "desc": "White",
            "goto": (_set_hair_color, {"hair_color": "white"}),
        },
        {
            "key": ("8", "blue", "bl"),
            "desc": "Blue",
            "goto": (_set_hair_color, {"hair_color": "blue"}),
        },
        {
            "key": ("9", "green", "g"),
            "desc": "Green",
            "goto": (_set_hair_color, {"hair_color": "green"}),
        },
        {
            "key": ("10", "pink", "p"),
            "desc": "Pink",
            "goto": (_set_hair_color, {"hair_color": "pink"}),
        },
        {
            "key": ("11", "purple", "pu"),
            "desc": "Purple",
            "goto": (_set_hair_color, {"hair_color": "purple"}),
        },
        {
            "key": ("12", "silver", "si"),
            "desc": "Silver",
            "goto": (_set_hair_color, {"hair_color": "silver"}),
        },
        {
            "key": ("13", "teal", "t"),
            "desc": "Teal",
            "goto": (_set_hair_color, {"hair_color": "teal"}),
        },
        {
            "key": ("14", "yellow", "y"),
            "desc": "Yellow",
            "goto": (_set_hair_color, {"hair_color": "yellow"}),
        },
    )

    return text, options


def appearance_skin_type(caller, raw_string, **kwargs):
    def _set_skin_type(caller, **kwargs):
        skin_type = kwargs.get("skin_type", None)
        if skin_type == "freckled":
            caller.appearance.add(
                "skin_type",
                "Skin Type",
                trait_type="trait",
                value=appearances.CharacterSkinType.FRECKLED,
            )
        elif skin_type == "scarred":
            caller.appearance.add(
                "skin_type",
                "Skin Type",
                trait_type="trait",
                value=appearances.CharacterSkinType.SCARRED,
            )
        elif skin_type == "wrinkled":
            caller.appearance.add(
                "skin_type",
                "Skin Type",
                trait_type="trait",
                value=appearances.CharacterSkinType.WRINKLED,
            )
        elif skin_type == "unblemished":
            caller.appearance.add(
                "skin_type",
                "Skin Type",
                trait_type="trait",
                value=appearances.CharacterSkinType.UNBLEMISHED,
            )
        else:
            return "chargen_appearance"

        return "chargen_appearance"

    text = "|CSelect your Skin Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_skin_type"},
        {
            "key": ("1", "freckled", "f"),
            "desc": "Freckled",
            "goto": (_set_skin_type, {"skin_type": "freckled"}),
        },
        {
            "key": ("2", "scarred", "sc"),
            "desc": "Scarred",
            "goto": (_set_skin_type, {"skin_type": "scarred"}),
        },
        {
            "key": ("3", "wrinkled", "w"),
            "desc": "Wrinkled",
            "goto": (_set_skin_type, {"skin_type": "wrinkled"}),
        },
        {
            "key": ("4", "unblemished", "u"),
            "desc": "Unblemished",
            "goto": (_set_skin_type, {"skin_type": "unblemished"}),
        },
        {"key": "_default", "goto": "chargen_appearance"},
    )

    return text, options


def appearance_eye_type(caller, raw_string, **kwargs):
    def _set_eye_type(caller, **kwargs):
        eye_type = kwargs.get("eye_type", None)
        if eye_type == "almond":
            caller.appearance.add(
                "eye_type",
                "Eye Type",
                trait_type="trait",
                value=appearances.CharacterEyeType.ALMOND,
            )
        elif eye_type == "hooded":
            caller.appearance.add(
                "eye_type",
                "Eye Type",
                trait_type="trait",
                value=appearances.CharacterEyeType.HOODED,
            )
        elif eye_type == "round":
            caller.appearance.add(
                "eye_type",
                "Eye Type",
                trait_type="trait",
                value=appearances.CharacterEyeType.ROUND,
            )
        else:
            return "chargen_appearance"

        return "chargen_appearance"

    text = "|CSelect your Eye Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_eye_type"},
        {
            "key": ("1", "almond", "a"),
            "desc": "Almond",
            "goto": (_set_eye_type, {"eye_type": "almond"}),
        },
        {
            "key": ("2", "hooded", "h"),
            "desc": "Hooded",
            "goto": (_set_eye_type, {"eye_type": "hooded"}),
        },
        {
            "key": ("3", "round", "r"),
            "desc": "Round",
            "goto": (_set_eye_type, {"eye_type": "round"}),
        },
        {"key": "_default", "goto": "chargen_appearance"},
    )

    return text, options


def appearance_nose_type(caller, raw_string, **kwargs):
    def _set_nose_type(caller, **kwargs):
        nose_type = kwargs.get("nose_type", None)
        if nose_type == "aquiline":
            caller.appearance.add(
                "nose_type",
                "Nose Type",
                trait_type="trait",
                value=appearances.CharacterNoseType.AQUILINE,
            )
        elif nose_type == "button":
            caller.appearance.add(
                "nose_type",
                "Nose Type",
                trait_type="trait",
                value=appearances.CharacterNoseType.BUTTON,
            )
        elif nose_type == "flat":
            caller.appearance.add(
                "nose_type",
                "Nose Type",
                trait_type="trait",
                value=appearances.CharacterNoseType.FLAT,
            )
        elif nose_type == "wide":
            caller.appearance.add(
                "nose_type",
                "Nose Type",
                trait_type="trait",
                value=appearances.CharacterNoseType.WIDE,
            )
        else:
            return "chargen_appearance"

        return "chargen_appearance"

    text = "|CSelect your Nose Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_nose_type"},
        {
            "key": ("1", "aquiline", "a"),
            "desc": "Aquiline",
            "goto": (_set_nose_type, {"nose_type": "aquiline"}),
        },
        {
            "key": ("2", "button", "b"),
            "desc": "Button",
            "goto": (_set_nose_type, {"nose_type": "button"}),
        },
        {
            "key": ("3", "flat", "f"),
            "desc": "Flat",
            "goto": (_set_nose_type, {"nose_type": "flat"}),
        },
        {
            "key": ("4", "wide", "w"),
            "desc": "Wide",
            "goto": (_set_nose_type, {"nose_type": "wide"}),
        },
        {"key": "_default", "goto": "chargen_appearance"},
    )

    return text, options


def appearance_mouth_type(caller, raw_string, **kwargs):
    def _set_mouth_type(caller, **kwargs):
        mouth_type = kwargs.get("mouth_type", None)
        if mouth_type == "full":
            caller.appearance.add(
                "mouth_type",
                "Mouth Type",
                trait_type="trait",
                value=appearances.CharacterMouthType.FULL,
            )
        elif mouth_type == "small":
            caller.appearance.add(
                "mouth_type",
                "Mouth Type",
                trait_type="trait",
                value=appearances.CharacterMouthType.SMALL,
            )
        elif mouth_type == "thin":
            caller.appearance.add(
                "mouth_type",
                "Mouth Type",
                trait_type="trait",
                value=appearances.CharacterMouthType.THIN,
            )
        elif mouth_type == "wide":
            caller.appearance.add(
                "mouth_type",
                "Mouth Type",
                trait_type="trait",
                value=appearances.CharacterMouthType.WIDE,
            )
        else:
            return "chargen_appearance"

        return "chargen_appearance"

    text = "|CSelect your Mouth Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_mouth_type"},
        {
            "key": ("1", "full", "f"),
            "desc": "Full",
            "goto": (_set_mouth_type, {"mouth_type": "full"}),
        },
        {
            "key": ("2", "small", "s"),
            "desc": "Small",
            "goto": (_set_mouth_type, {"mouth_type": "small"}),
        },
        {
            "key": ("3", "thin", "t"),
            "desc": "Thin",
            "goto": (_set_mouth_type, {"mouth_type": "thin"}),
        },
        {
            "key": ("4", "wide", "w"),
            "desc": "Wide",
            "goto": (_set_mouth_type, {"mouth_type": "wide"}),
        },
        {"key": "_default", "goto": "chargen_appearance"},
    )

    return text, options


def appearance_jaw_type(caller, raw_string, **kwargs):
    def _set_jaw_type(caller, **kwargs):
        jaw_type = kwargs.get("jaw_type", None)
        if jaw_type == "pointed":
            caller.appearance.add(
                "jaw_type",
                "Jaw Type",
                trait_type="trait",
                value=appearances.CharacterJawType.POINTED,
            )
        elif jaw_type == "round":
            caller.appearance.add(
                "jaw_type",
                "Jaw Type",
                trait_type="trait",
                value=appearances.CharacterJawType.ROUND,
            )
        elif jaw_type == "square":
            caller.appearance.add(
                "jaw_type",
                "Jaw Type",
                trait_type="trait",
                value=appearances.CharacterJawType.SQUARE,
            )
        else:
            return "chargen_appearance"

        return "chargen_appearance"

    text = "|CSelect your Jaw Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_jaw_type"},
        {
            "key": ("1", "pointed", "p"),
            "desc": "Pointed",
            "goto": (_set_jaw_type, {"jaw_type": "pointed"}),
        },
        {
            "key": ("2", "round", "r"),
            "desc": "Round",
            "goto": (_set_jaw_type, {"jaw_type": "round"}),
        },
        {
            "key": ("3", "square", "s"),
            "desc": "Square",
            "goto": (_set_jaw_type, {"jaw_type": "square"}),
        },
        {"key": "_default", "goto": "chargen_appearance"},
    )

    return text, options


def appearance_eyebrow_type(caller, raw_string, **kwargs):
    def _set_eyebrow_type(caller, **kwargs):
        eyebrow_type = kwargs.get("eyebrow_type", None)
        if eyebrow_type == "arched":
            caller.appearance.add(
                "eyebrow_type",
                "Eyebrow Type",
                trait_type="trait",
                value=appearances.CharacterEyebrowType.ARCHED,
            )
        elif eyebrow_type == "straight":
            caller.appearance.add(
                "eyebrow_type",
                "Eyebrow Type",
                trait_type="trait",
                value=appearances.CharacterEyebrowType.STRAIGHT,
            )
        elif eyebrow_type == "thick":
            caller.appearance.add(
                "eyebrow_type",
                "Eyebrow Type",
                trait_type="trait",
                value=appearances.CharacterEyebrowType.THICK,
            )
        elif eyebrow_type == "thin":
            caller.appearance.add(
                "eyebrow_type",
                "Eyebrow Type",
                trait_type="trait",
                value=appearances.CharacterEyebrowType.THIN,
            )
        else:
            return "chargen_appearance"

        return "chargen_appearance"

    text = "|CSelect your Eyebrow Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_eyebrow_type"},
        {
            "key": ("1", "arched", "a"),
            "desc": "Arched",
            "goto": (_set_eyebrow_type, {"eyebrow_type": "arched"}),
        },
        {
            "key": ("2", "straight", "s"),
            "desc": "Straight",
            "goto": (_set_eyebrow_type, {"eyebrow_type": "straight"}),
        },
        {
            "key": ("3", "thick", "t"),
            "desc": "Thick",
            "goto": (_set_eyebrow_type, {"eyebrow_type": "thick"}),
        },
        {
            "key": ("4", "thin", "th"),
            "desc": "Thin",
            "goto": (_set_eyebrow_type, {"eyebrow_type": "thin"}),
        },
        {"key": "_default", "goto": "chargen_appearance"},
    )

    return text, options


def chargen_finalize(caller, raw_string):
    return "", ""
