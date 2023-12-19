from evennia.utils import dedent

from world.characters import backgrounds, classes, genders, races

_RACE_INFO_DICT = {
    "human": "The most common face to see in Arcellia, humans are known for their tenacity, creativity, and endless capacity for growth.",  # noqa: E501
    "elf": "Elves of Arcellia embody an ageless grace, their histories etched into the very forests and rivers of the world. Ancient and wise, they live in harmonious synchrony with the natural tapestry that surrounds them, their lifelines stretching across eras like the boughs of the World Tree. With eyes that reflect the depth of the stars, elves harbor a mastery over magic few can rival, their arcane heritage as intrinsic as the wind's whisper. Bound by traditions woven through the fabric of time, they walk paths shadowed by lore, their existence a melody harmonizing with the ethereal song of eternity.",  # noqa: E501
    "dwarf": "As durable and unyielding as their homes of stone, dwarves are some of the finest warriors, miners, and smiths in all of Arcellia. They're known for their confidence and keen intuition, valuing family, ritual, and fine craftsmanship. Many of their ancient kingdoms have been surrendered to goblins and other creatures of the deep.",  # noqa: E501
    "gnome": "Gnomes are diminutive, inquisitive inventors, their minds ever-ticking gears amidst a whirlwind of arcane intellect. They thrive on innovation, their lives a constant pursuit of knowledge, enchantment, and mechanical wonders that teeter on the brink of whimsy and genius.",  # noqa: E501
    "nymph": "Each Nymphkind bears an Elemental Allure, an innate charm that captures hearts as effortlessly as the elements wield their power. These beguiling beings breathe an otherworldly magnetism, entwining those who fall under their gaze with strands of lust, adoration, or sheer bewitchment. Like the ripples upon a still pond or the flickering dance of flames, their seductive powers manifest in various forms, reflecting the vast spectrum of their ancestral realm.",  # noqa: E501
    "orc": "Orcs exhibit widely varying appearances. Creatures of intense emotion, the orcs are more inclined to act than contemplate - whether the rage burning their bodies compels them to fight, or the love of filling their hearts inspires acts of incredible kindness.",  # noqa: E501
    "pyreling": "The Pyreling are descendents cloaked in myth, born of the mingling between mortal essence and the enigmatic energies of hell. They carry within them a flickering flame that manifests in eyes that glow like coals and skin in shades of smoldering dusk. Misunderstood by many, the Pyrelings wander through Arcellia bearing gifts of arcane affinity, as well as a propensity for the extraordinary, often leaving tales of fear and fascination in their wake.",  # noqa: E501
}

_SUBRACE_INFO_DICT = {
    "elf": {
        "high": "The High Elves, ethereal as the twilight heavens, draw their lineage from the stars. With minds sharp as the crescent moon, they are curators of arcane wisdom, their lives as elongated as the very eternities they study. Their enclaves, built where ley lines converge, resonate with the harmonious magic of the firmament, reflecting the astral glory of their heritage in every spell they weave and every blade they forge under the watchful eyes of the constellations.",  # noqa: E501
        "night": "It was they who first delved deep into the arcane arts, their insatiable curiosity unraveling the fabric of reality nearly a millennia past. The night elves' unbridled use of sorcery summoned forth cataclysmic force that ignited a war of unspeakable devastation between mortals and entities of pure destruction. Only through immense sacrifice did the night elves drive back this ruinous presence, preserving the world at the dire cost of their own splendid realm, now lost beneath relentless tides.",
        "wood": "Beneath emerald canopies, where life thrums in every leaf and branch, dwell the Wood Elves. Their souls are the voice of the forest, as serene as still water and as wild as the untamed grove. These elves are guardians of the natural world, moving with a grace that matches the swaying boughs and flowing streams, their instincts finely honed to the rhythm of the wilderness. Bridging the material plane and the natural realm in harmonious co-existence, Wood Elves invoke the vitality of the woods in their tireless defense against those who would despoil their verdant home.",  # noqa: E501
    },
    "dwarf": {
        "emberheart": "The Emberheart Dwarves glow with an inner fire, their souls alight with consummate confidence and a sharp, unerring insight. Celebrated for their intricate craftsmanship and elaborate ceremonies, the Emberhearts dwell within the grand vocanic forges of the Molten Hold, where kinship and artistry burn brighter than the furnaces that warm their halls.",  # noqa: E501
        "stoneguard": "Bearing the weight of history upon their broad shoulders, Stoneguard Dwarves have weathered the collapse of their once-mighty bastions, stoically surrendering their dominion to the relentless advance of goblin hordes and orcish legions. With hearts like the bedrock they cleave, these Dwarves nurture a collective resilience, driven by a cynical yet unwavering resolve to reclaim the glory and the halls of their ancestors.",  # noqa: E501
        "ironvein": "Forged in the dark crucible of the world's underbelly, the Ironvein Dwarves trace their lineage through centuries spent in the eerie expanses of the deep. Exposed to mysteries that warp mind and matter, imbued with the arcane residue that pulses through their cavernous abyss, they have emerged with esoteric powers that are both a gift and a legacy of old tyrannies. Survival meant enduring cruel manipulation by aberrant overlords, and from such depths of despair rose the fortitude and psionic might that now courses through the veins of these steely-eyed survivors. Though the chains of the past have been cast off, the Ironveins have never forgotten the cold embrace of subjugation, nor the sweet taste of hard-won freedom.",  # noqa: E501
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

_CLASS_INFO_DICT = {
    "artisan": "In the dance of creation and the craftsmanship of worlds, the Aristan weaves innovation and artistry into every tangible form.",
    "cleric": "Carrying a divine's mandate, the Cleric strides with purpose, a bastion of sacred power where faith's incandescent flame burns fiercely within.",
    "druid": "Keepers of the world and masters of nature, the Druid commands Arcellia's wrath, capable of a diverse range of environmental abilities.",
    "hunter": "Deadly marksmen and skilled survivalists, the Hunter possesses a primal connection with beasts of all types, capable of training them as loyal companions.",
    "mage": "A scholar of the esoteric and seeker of hidden truths, the Mage commands the fabric of magic through meticulous study and unwavering discipline.",
    "paladin": "Sworn to uphold the confluence of valor and virtue, the Paladin wields both sword and piety with an unwavering resolve.",
    "rogue": "In the embrace of shadows and the subtlety of silence, the Rogue navigates a world unseen, where guild and finesse are the keys to survival and success.",
    "shaman": "The spiritual leaders of tribes and clans. The Shaman use their connection to the spirit world to unleash fury upon their foes.",
    "warlock": "Bound by pact to an eldritch entity, the Warlock wields otherwordly might, drawing upon forbidden secrets to manifest their dread patrons' will.",
    "warrior": "The quintessential embodiment of battle's ire, the Warrior matches their unrelenting ferocity with a robust tenacity for the clamor and clash of war.",
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


def chargen_welcome(caller):
    def _set_gender(caller, choice):
        choice = choice.strip().lower()[0]
        if choice == "m":
            caller.character.add(
                "gender",
                "Gender",
                trait_type="trait",
                value=genders.CharacterGender.MALE,
            )
        elif choice == "f":
            caller.character.add(
                "gender", "Gender", value=genders.CharacterGender.FEMALE
            )
        elif choice == "a":
            caller.character.add(
                "gender", "Gender", value=genders.CharacterGender.ANDROGYNOUS
            )
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
        {"key": ("male", "m"), "goto": _set_gender},
        {"key": ("female", "f"), "goto": _set_gender},
        {"key": ("androgynous", "a"), "goto": _set_gender},
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
            {"key": "y", "desc": "Confirm appearance", "goto": "chargen_finalize"},
            {
                "key": "n",
                "desc": "Return",
                "goto": ("chargen_appearance", {"appearance": None}),
            },
        )

    return text, options


def chargen_finalize(caller, raw_string):
    return "", ""
