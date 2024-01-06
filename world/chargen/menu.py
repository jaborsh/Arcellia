from evennia.utils import dedent

from world.characters import backgrounds, genders, races

_GENDER_INFO_DICT = {
    "male": "Men in Arcellia come in many shapes and sizes, from many races and many backgrounds. Whether tall and muscular, or short and lean, they are often reputed to be sons of Adon, the First Man and God of the son. Typically known for their great passions, in love and in war, men are revered in the worlds of humans and orcs as the superior race, yet amongst elves, dwarves, and pyrelings, share equality with the rest. Adonites are the pinnacle of masculinity, a race of only men, and are the source of envy and resentment in many individuals across the world.",
    "female": "The Gift of Hela onto the world, children of the moon and her divine right, women are known for their mystery and beauty alike. Whilst they may range in size, stature, and disposition, on truth remains - hell hath no fury like a woman scorned. Known for their exceptional wit and persuasion, they have no less found themselves in a more submissive society amongst some races. Yet, in others, they are known as leaders - the nymphs and the beastials revere their matriarchs and follow their wisdom, whilst the Helias commonly cloister themselves away, such that to see one might be a rarity to happen in a single lifetime. In fact, it is considered an ill omen when the Helias are seen in numbers, as if portents of the world's end.",
    "androgynous": "For some, the world is not so easily viewed as day and night, as light or dark, as black or white - for many, it is the colors and forms in between which speak to their truth, and so is it said that Gan, the Ruler of the Twilight Realm, gifted mortality with the ability to choose. When a soul is beyond the scope, their form takes the shape of their choosing, as varied and unique as they themselves. In fact, it is said that the Twils, a race of individuals who dwell within the twilight, might change their shape at will, adapting to suit their heart's fancy, Gan's greatest gift to their beloved people.\n\nAndrogynous individuals are generally accepted in most societies, but some may have found their homes more accepting than others, or less willing to understand their dispositions. In main cities, it is considered very disrespectful, and sometimes illegal, to disregard an individual's identity.",
}

_RACE_INFO_DICT = {
    "human": "|YHumans|n:\n\nThey are creatures of passion and paradox, canvases of immeasurable depth painted with the vibrant hues of their experiences. In their eyes, one finds the glimmer of stars they have yet to chart, and in the steady rhythm of their hearts, the beat of the ancient drums that have long echoed through the corridors of time. Bound to the wheel of progress, humans traverse the breadth of their realm with insatiable curiosity. They are builders and dreamers, forging empires from the raw materials of nature, etching their histories into the stones of the world. With hands capable of both creation and destruction, they mold their destinies, leaving the echoes of their triumphs and tragedies in the whispers of the wind. Amongst them walk the valiant and the villainous, a spectrum of souls whose choices thread the fine line between heroism and infamy. Love is their greatest strength, and it is love that can be their undoing - such are the stark contrasts that define them. Every smile and tear, a note in the human spirit.",  # noqa: E501
    "elf": "|YElves|n:\n\nTall and regal, draped in the elegance of their rich culture, elves move with a grace that belies their formidable strength. Their features, sharp and delicately crafted, mirror the beauty of their surroundings, where each leaf and bud thrives under their tender care. Eyes that sparkle with the wisdom of ages seem to pierce through the veils of time, beholding the mysteries that lie hidden to the more fleeting gazes of other beings. Bound by ancient traditions and an unwavering respect for the balance of nature, these denizens cultivate a deep-seated magic that breathes in harmony with the world. The arcane whispers of the earth are their companions, a silent dialogue that has stretched unbroken since the dawn of time. In their hands, spells weave seamlessly, and the pulse of the land resonates through their songs and storied craftwork which reflects both the beauty of the natural world and the depth of their reverence for it.",  # noqa: E501
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
        "ironvein": "|YIronvein Dwarves|n:\n\nForged in the dark crucible of the world's underbelly, the Ironvein Dwarves trace their lineage through centuries spent in the eerie expanses of the deep. Exposed to mysteries that warp mind and matter, imbued with the arcane residue that pulses through their cavernous abyss, they have emerged with esoteric powers that are both a gift and a legacy of old tyrannies. Survival meant enduring cruel manipulation by aberrant overlords, and from such depths of despair rose the fortitude and psionic might that now courses through the veins of these steely-eyed survivors. Though the chains of the past have been cast off, the Ironveins have never forgotten the cold embrace of subjugation, nor the sweet taste of hard-won freedom.",  # noqa: E501
        "stoneguard": "|YStoneguard Dwarves|n:\n\nBearing the weight of history upon their broad shoulders, Stoneguard Dwarves have weathered the collapse of their once-mighty bastions, stoically surrendering their dominion to the relentless advance of goblin hordes and orcish legions. With hearts like the bedrock they cleave, these Dwarves nurture a collective resilience, driven by a cynical yet unwavering resolve to reclaim the glory and the halls of their ancestors.",  # noqa: E501
    },
    "gnome": {
        "dusk": "|YDusk Gnomes|n:\n\nVeiled in mystery and born of the shadowy embrace of the subterranean world, Dusk Gnomes traverse the hidden depths with a grace that belies their surroundings. Illuminated by the faint glow of luminescent fungi and echoing caverns, they are silent witnesses to secrets entombed in stone. Masters of quietude and guile, Dusk Gnomes navigate the labyrinthine underworld with an innate understanding that is as profound as the ancient darkness from which they emerge.",  # noqa: E501
        "hearth": "|YHearth Gnomes|n:\n\nAn embodiment of scrupulous ingenuity and unshakable stability, Hearth Gnomes thrive within the heart of bustling communities or quaint hamlets. With hands weathered by toil, yet as precise as a master clockmaker's, they churn out marvels of craftsmanship and innovation. Hearth Gnomes are the cornerstone of tradition, etching each day's labor into the enduring legacy of their kin. Their tenacious spirits are akin to the enduring stone, shaping society with the chisel of their relentless pursuit of excellence and progress.",  # noqa: E501
        "sylvan": "|YSylvan Gnomes|n:\n\nSylvan Gnomes, sprightly and secretive as the woodland sprites, dwell amidst the verdant groves and dappled glades of Arcellia's vast forests. Whispering to the trees and laughing with the brooks, they are unseen keepers of nature's most secluded riddles, guarding the sylvan sanctuaries against those who would dare disturb them. With an affinity for the woods, these Gnomes craft enchantments as delicate as cobwebs, and their laughter is as fleeting as the wind through the leaves.",  # noqa: E501
    },
    "pyreling": {
        "emberkin": "|YEmberkin Pyrelings|n:\n\nEmberkin Pyrelings harbor the essence of smoldering embers and soul-deep shadows. Their lineage serves as a conduit for fiery dominion, allowing them to summon both the scalding wrath and the obsidian shroud of their fearsome forefathers.",  # noqa: E501
        "arcanist": "|YArcanist Pyrelings|n:\n\nThe Arcanist Pyrelings trace their heritage to the inscrutable compact with the grand magus of the Infernal. These Pyrelings are imbued with an arcane reservoir, deep and vast, granting them an affinity for the eldritch arts that is both singular and potent. With a mere incantation, they can bend the weft of magical energies to their will, shaping the fabric of spellcraft with ease.",  # noqa: E501
        "warbrand": "|YWarbrand Pyrelings|n:\n\nForged in the martial traditions of the fiery fortresses, Warbrand Pyrelings are the progeny of pacts with war-torn overlords. Their very beings thrum with martial prowess and the relentless surge of the inferno that fuels their relentless spirit.",  # noqa: E501
    },
}

_BACKGROUND_INFO_DICT = {
    "acolyte": "|YAcolyte|n:\n\nYou have spent your life in service to a temple, learning sacred rites and providing sacrifices to the god or gods you worship. Serving the gods and discovering their sacred works will guide you to greatness.",
    "charlatan": "|YCharlatan|n:\n\nYou're an expert in manipulation, prone to exaggeration, and more than happy to profit from it. Bending the truth and turning allies against each other will lead to greater success down the road.",
    "criminal": "|YCriminal|n:\n\nYou have a history of breaking the law and survive by leveraging less-than-legal connections. Profiting from criminal enterprise will lead to greater opportunities in the future.",
    "entertainer": "|YEntertainer|n:\n\nYou live to sway and subvert your audience, engaging common crowds and high society alike. Preserving art and bringing joy to the hapless and downtrodden heightens your charismatic aura.",
    "folk hero": "|YFolk Hero|n:\n\nYou're the champion of the common people, challenging tyrants and monsters to protect the helpless. Saving innocents in imminent danger will make your legend grow.",
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
    def _set_screenreader(caller):
        for session in caller.account.sessions.all():
            session.protocol_flags["SCREENREADER"] = True
            session.update_flags(screenreader=True)
        return "chargen_gender"

    text = dedent(
        """\
        Enveloped in a cocoon of primordial blackness, warmth wraps around the tiny essence of being, a lone conscience no more significant than a grain of malt in an endless expanse of darkness. It floats in this tranquil void, beyond the realms of obligation, where time and duty dissolve into an eternal, serene abyss. Thought and action meld into the nothingness; here one finds peace in the still, comforting promise of an existence unburdened by the need to do, to be, to strive - forevermore in an endless canvas of never ever.

        |CDo you use a screenreader?|n
        """
    )

    options = (
        {"key": "", "goto": "chargen_welcome"},
        {"key": ("y", "yes"), "desc": "Enable Screenreader", "goto": _set_screenreader},
        {"key": ("n", "no"), "desc": " Disable Screenreader", "goto": "chargen_gender"},
        {"key": "_default", "goto": "chargen_welcome"},
    )

    return text, options


def chargen_gender(caller, raw_string, **kwargs):
    def _set_gender(caller):
        selected_gender = kwargs.get("selected_gender", None)
        if selected_gender == "male":
            caller.character.add(
                "gender",
                "Gender",
                trait_type="trait",
                value=genders.CharacterGender.MALE,
            )
        elif selected_gender == "female":
            caller.character.add(
                "gender", "Gender", value=genders.CharacterGender.FEMALE
            )
        elif selected_gender == "androgynous":
            caller.character.add(
                "gender", "Gender", value=genders.CharacterGender.ANDROGYNOUS
            )
        else:
            return "chargen_welcome"

        return "chargen_race"

    if selected_gender := kwargs.get("selected_gender", None):
        text = _GENDER_INFO_DICT[selected_gender] + "\n\n|CConfirm your Gender|n:"
        options = (
            {"key": "", "goto": "chargen_welcome"},
            {
                "key": ("y", "yes"),
                "desc": f"Confirm {selected_gender.capitalize()}",
                "goto": (_set_gender, {"selected_gender": selected_gender}),
            },
            {
                "key": ("n", "no"),
                "desc": "Return to Gender Selection",
                "goto": ("chargen_gender", {"selected_gender": None}),
            },
        )

    else:
        text = dedent(
            """\
            As immeasurable time drifts by, untouched by the suffocating grasp of struggle, existence remains unfathomably tranquil. But in the midst of this hushed eternity, a whisper of consciousness begins to stir. Somewhere just beyond perception, shrouded in the unseen recesses of this void, a presence makes itself known. It festers, submerged in a vile, caustic broth that seeps into the edges of awareness. This entity envelops the serene conscience, injecting a sense of disquiet into the calm that once reigned.

            All at once, as if gasping for breath from beneath an ocean of nothingness, there is light and form upon the horizon. The chance to become, to be, to exist, dwells solely within your heart.

            |CSelect your Gender|n:
            """
        )  # noqa: E501

        options = (
            {"key": "", "goto": "chargen_welcome"},
            {
                "key": ("1", "male", "m"),
                "desc": "Male",
                "goto": ("chargen_gender", {"selected_gender": "male"}),
            },
            {
                "key": ("2", "female", "f"),
                "desc": "Female",
                "goto": ("chargen_gender", {"selected_gender": "female"}),
            },
            {
                "key": ("3", "androgynous", "a"),
                "desc": "Androgynous",
                "goto": ("chargen_gender", {"selected_gender": "androgynous"}),
            },
            {"key": "_default", "goto": "chargen_gender"},
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
        return "chargen_background"

    selected_race = kwargs.get("selected_race", None)
    selected_subrace = kwargs.get("selected_subrace", "")

    if selected_subrace:
        text = _SUBRACE_INFO_DICT[selected_race][selected_subrace] + "\n"
    elif selected_race:
        text = _RACE_INFO_DICT[selected_race] + "\n"
    else:
        text = dedent(
            """
            A notion unfurls within the stillness, one you might rather remain oblivious to. Consider the reason behind this self-imposed exile into nothingness. Perhaps there's a part of you, marinated in the excesses of your own actions, that recoils from such revelations. In eagerness, perhaps, you deluged yourself in oblivion, tipping the balance beyond a simple seasoning to a state of overwhelming saturation.

            Imagine, if you dare, a colossal sphere where malevolence brews. On this orb, simian creatures of nefarious intent wage an incessant war, a tableau of chaos underpinned by brutality. You are among them - no mere observer, but an active participant. This sphere is your arena, your world; the others, your kindred and adversaries.

            They clash with savage fervor over scraps and dominance, a dance as old as time itself, couched in a rhetoric that seems all too familiar - a hollow phrase adopted from the ether to give a shade of meaning to the struggle. Take with you the grim axiom from this metaphorical panorama: in the contest for survival amongst your own, it is conquer or be conquered, to prevail in might or be reduced to insignificance.

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
            Drawn inexorably as if fated, your awareness adheres to a most disquieting realization, much like the unfortunate insect ensnared by a viscous trap. The fleshly construct you inhabit, a machine wrought of limbs, burdened with the intrinsic nature of life begins its laborious reawakening. This vessel, animated by a tumultuous spirit, yearns for the expanse of a world where purpose is the currency of existence, where desire is ever-present.

            Suddenly, a searing lance of light pierces the tranquility that shrouds your mind, an invasive force intent on prying your eyes from their restful closure. Accompanying this intrusion is a sound, a sonorous peal that resonates with the very essence of perdition. It heralds an awakening, a clarion so powerful, it is as if the very gates of hell themselves were orchestrating your return to the waking world.

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
    text = dedent(
        """
        Suspended above a basin twisted and marred by neglect, a mirror holds court. From the damaged faucet, a jet of scalding water erupts, casting a shroud of steam across the glass, obscuring clarity. There, in the fogged reflection, only the barest hint of a figure can be discerned, a specter of self without detail or form. A startling epiphany cascades over you in that ill-defined moment; your own visage is a mystery, lost beneath the gentle veil of mist.

        |CSelect an Appearance Option|n:
        """
    )

    options = (
        {"key": "", "goto": "chargen_appearance"},
        {
            "key": ("1", "detailed", "d"),
            "desc": "Create a Customized Description",
            "goto": "chargen_appearance_detailed",
        },
        {
            "key": ("2", "template", "t"),
            "desc": "Select Template Descriptors",
            "goto": "chargen_appearance_template",
        },
        {"key": "_default", "goto": "chargen_appearance"},
    )

    return text, options


def chargen_appearance_detailed(caller, raw_string, **kwargs):
    def _set_appearance(caller, appearance, **kwargs):
        caller.db.desc = appearance.strip()
        return ("chargen_apperance_detailed", {"appearance": appearance.strip()})

    if appearance := kwargs.get("appearance", None):
        text = f"|CConfirm your Appearance|n:\n{appearance}"
        options = (
            {"key": "y", "desc": "Confirm Appearance", "goto": "chargen_finalize"},
            {
                "key": "n",
                "desc": "Return",
                "goto": ("chargen_appearance_detailed", {"appearance": None}),
            },
        )
    else:
        text = dedent(
            """
            The time has come: a defining instant that invites no delay, and fosters no escape. What lies beyond that soft and swirling vapor is a truth that must be faced. With a breath that is both anticipatory and anxious, the facade you're about to unveil comes with the peril of true self-revelation. Therein lies the precipice of identity - you stand poised to meet the eyes of the being you inhabit, to witness the countenance that is undeniably yours, irrespective of reverberations they might cause within the core of who you are.

            |CWrite your Description|n:
            """
        )
        options = (
            {"key": "", "goto": "chargen_appearance_detailed"},
            {"key": "_default", "goto": (_set_appearance, {"appearance": raw_string})},
        )

    return text, options


def chargen_appearance_template(caller, raw_string, **kwargs):
    def _set_appearance(caller, **kwargs):
        desc = dedent(
            """
            {race} {gender}, standing with {height} stature, embodies the life they've lived through the form of their {body} physique. Their {skin} skin, a canvas of their heritage, captures and plays with the light, be it the golden touch of the sun or the moon's soft glow. {eye_type} eyes, rich in {eye_color}, reveal the depths of their experiences. Hair, in varying shades of {hair_color}, crowns their head, a well-proportioned {nose} finds harmony with a {mouth}, together sketching the visage of character.
            """.format(
                race=caller.race.value.name,
                gender=caller.gender.value,
                height=kwargs.get("height"),
                body=kwargs.get("body"),
                skin=kwargs.get("skin_type"),
                eye_type=kwargs.get("eye_type"),
                eye_color=kwargs.get("eye_color"),
                hair_color=kwargs.get("hair_color"),
                nose=kwargs.get("nose_type"),
                mouth=kwargs.get("mouth_type"),
            )
        )

        desc = (
            "A " + desc.lstrip()
            if desc[0].lower() not in ["a", "e", "i", "o", "u"]
            else "An " + desc.lstrip()
        )

        caller.db.desc = desc.strip()
        return "chargen_finalize"

    text = dedent(
        """
        A figure stares back from the other side of the obscured mirror, its features hidden beneath the mist's caress. It exists there as an enigma, a stranger composed of familiar lines and curves, yet wholly unrecognizable. A shiver of alienation creeps along your spine - the realization dawns upon you that the entity reflected in the glass, this 'thing' that should be as known to you as the very beat of your heart, remains anonymous. It is as if you are gazing upon an intimate unknown, a specter of self that is both intimately close and unsettlingly foreign.

        |CSelect an Appearance Option|n:
        """
    )

    height = kwargs.get("height", "")
    body = kwargs.get("body", "")
    eye_color = kwargs.get("eye_color", "")
    hair_color = kwargs.get("hair_color", "")
    skin_type = kwargs.get("skin_type", "")
    eye_type = kwargs.get("eye_type", "")
    nose_type = kwargs.get("nose_type", "")
    mouth_type = kwargs.get("mouth_type", "")

    options = (
        {"key": "", "goto": "chargen_appearance"},
        {
            "key": ("1", "height"),
            "desc": f"Height ({height})",
            "goto": ("appearance_height", kwargs),
        },
        {
            "key": ("2", "body", "body type"),
            "desc": f"Body Type ({body})",
            "goto": ("appearance_body", kwargs),
        },
        {
            "key": ("3", "eye color", "ec"),
            "desc": f"Eye Color ({eye_color})",
            "goto": ("appearance_eye_color", kwargs),
        },
        {
            "key": ("4", "hair color", "hc"),
            "desc": f"Hair Color ({hair_color})",
            "goto": ("appearance_hair_color", kwargs),
        },
        {
            "key": ("5", "skin type", "st"),
            "desc": f"Skin Type ({skin_type})",
            "goto": ("appearance_skin_type", kwargs),
        },
        {
            "key": ("6", "eye type", "et"),
            "desc": f"Eye Type ({eye_type})",
            "goto": ("appearance_eye_type", kwargs),
        },
        {
            "key": ("7", "nose type", "nt"),
            "desc": f"Nose Type ({nose_type})",
            "goto": ("appearance_nose_type", kwargs),
        },
        {
            "key": ("8", "mouth type", "mt"),
            "desc": f"Mouth Type ({mouth_type})",
            "goto": ("appearance_mouth_type", kwargs),
        },
    )

    if len(kwargs) == 9:
        options += (
            {
                "key": ("9", "f", "finalize"),
                "desc": "|CFinalize Appearance|n",
                "goto": (_set_appearance, kwargs),
            },
        )

    return text, options


def appearance_height(caller, raw_string, **kwargs):
    text = "|CSelect your Height|n:\n"
    options = (
        {"key": "", "goto": "appearance_height"},
        {
            "key": ("1", "short", "sh"),
            "desc": "Short",
            "goto": ("chargen_appearance_template", kwargs | {"height": "short"}),
        },
        {
            "key": ("2", "average", "av"),
            "desc": "Average",
            "goto": ("chargen_appearance_template", kwargs | {"height": "average"}),
        },
        {
            "key": ("3", "tall", "t"),
            "desc": "Tall",
            "goto": ("chargen_appearance_template", kwargs | {"height": "tall"}),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def appearance_body(caller, raw_string, **kwargs):
    text = "|CSelect your Body Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_body"},
        {
            "key": ("1", "petite", "p"),
            "desc": "Petite",
            "goto": ("chargen_appearance_template", kwargs | {"body": "petite"}),
        },
        {
            "key": ("2", "slender", "s"),
            "desc": "Slender",
            "goto": ("chargen_appearance_template", kwargs | {"body": "slender"}),
        },
        {
            "key": ("3", "average", "av"),
            "desc": "Average",
            "goto": ("chargen_appearance_template", kwargs | {"body": "average"}),
        },
        {
            "key": ("4", "athletic", "at"),
            "desc": "Athletic",
            "goto": ("chargen_appearance_template", kwargs | {"body": "athletic"}),
        },
        {
            "key": ("5", "robust", "r"),
            "desc": "Robust",
            "goto": ("chargen_appearance_template", kwargs | {"body": "robust"}),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def appearance_eye_color(caller, raw_string, **kwargs):
    text = "|CSelect your Eye Color|n:\n"
    options = (
        {"key": "", "goto": "appearance_eye_color"},
        {
            "key": ("1", "amber", "a"),
            "desc": "Amber",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "amber"}),
        },
        {
            "key": ("2", "blue", "b"),
            "desc": "Blue",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "blue"}),
        },
        {
            "key": ("3", "brown", "br"),
            "desc": "Brown",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "brown"}),
        },
        {
            "key": ("4", "green", "g"),
            "desc": "Green",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "green"}),
        },
        {
            "key": ("5", "grey", "gr"),
            "desc": "Grey",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "grey"}),
        },
        {
            "key": ("6", "hazel", "h"),
            "desc": "Hazel",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "hazel"}),
        },
        {
            "key": ("7", "black", "bl"),
            "desc": "Black",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "black"}),
        },
        {
            "key": ("8", "copper", "c"),
            "desc": "Copper",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "copper"}),
        },
        {
            "key": ("9", "crimson", "cr"),
            "desc": "Crimson",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "crimson"}),
        },
        {
            "key": ("10", "emerald", "e"),
            "desc": "Emerald",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "emerald"}),
        },
        {
            "key": ("11", "gold", "go"),
            "desc": "Gold",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "gold"}),
        },
        {
            "key": ("12", "opal", "o"),
            "desc": "Opal",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "opal"}),
        },
        {
            "key": ("13", "onyx", "on"),
            "desc": "Onyx",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "onyx"}),
        },
        {
            "key": ("14", "red", "r"),
            "desc": "Red",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "red"}),
        },
        {
            "key": ("15", "sapphire", "sa"),
            "desc": "Sapphire",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "sapphire"}),
        },
        {
            "key": ("16", "silver", "si"),
            "desc": "Silver",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "silver"}),
        },
        {
            "key": ("17", "violet", "v"),
            "desc": "Violet",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "violet"}),
        },
        {
            "key": ("18", "white", "w"),
            "desc": "White",
            "goto": ("chargen_appearance_template", kwargs | {"eye_color": "white"}),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def appearance_hair_color(caller, raw_string, **kwargs):
    text = "|CSelect your Hair Color|n:\n"
    options = (
        {"key": "", "goto": "appearance_hair_color"},
        {
            "key": ("1", "auburn", "a"),
            "desc": "Auburn",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "auburn"}),
        },
        {
            "key": ("2", "black", "bl"),
            "desc": "Black",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "black"}),
        },
        {
            "key": ("3", "blonde", "b"),
            "desc": "Blonde",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "blonde"}),
        },
        {
            "key": ("4", "brown", "br"),
            "desc": "Brown",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "brown"}),
        },
        {
            "key": ("5", "grey", "gr"),
            "desc": "Grey",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "grey"}),
        },
        {
            "key": ("6", "red", "r"),
            "desc": "Red",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "red"}),
        },
        {
            "key": ("7", "white", "w"),
            "desc": "White",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "white"}),
        },
        {
            "key": ("8", "blue", "bl"),
            "desc": "Blue",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "blue"}),
        },
        {
            "key": ("9", "green", "g"),
            "desc": "Green",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "green"}),
        },
        {
            "key": ("10", "pink", "p"),
            "desc": "Pink",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "pink"}),
        },
        {
            "key": ("11", "purple", "pu"),
            "desc": "Purple",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "purple"}),
        },
        {
            "key": ("12", "silver", "si"),
            "desc": "Silver",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "silver"}),
        },
        {
            "key": ("13", "teal", "t"),
            "desc": "Teal",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "teal"}),
        },
        {
            "key": ("14", "yellow", "y"),
            "desc": "Yellow",
            "goto": ("chargen_appearance_template", kwargs | {"hair_color": "yellow"}),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def appearance_skin_type(caller, raw_string, **kwargs):
    text = "|CSelect your Skin Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_skin_type"},
        {
            "key": ("1", "freckled", "f"),
            "desc": "Freckled",
            "goto": ("chargen_appearance_template", kwargs | {"skin_type": "freckled"}),
        },
        {
            "key": ("2", "scarred", "sc"),
            "desc": "Scarred",
            "goto": ("chargen_appearance_template", kwargs | {"skin_type": "scarred"}),
        },
        {
            "key": ("3", "wrinkled", "w"),
            "desc": "Wrinkled",
            "goto": ("chargen_appearance_template", kwargs | {"skin_type": "wrinkled"}),
        },
        {
            "key": ("4", "unblemished", "u"),
            "desc": "Unblemished",
            "goto": (
                "chargen_appearance_template",
                kwargs | {"skin_type": "unblemished"},
            ),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def appearance_eye_type(caller, raw_string, **kwargs):
    text = "|CSelect your Eye Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_eye_type"},
        {
            "key": ("1", "almond", "a"),
            "desc": "Almond",
            "goto": ("chargen_appearance_template", kwargs | {"eye_type": "almond"}),
        },
        {
            "key": ("2", "hooded", "h"),
            "desc": "Hooded",
            "goto": ("chargen_appearance_template", kwargs | {"eye_type": "hooded"}),
        },
        {
            "key": ("3", "round", "r"),
            "desc": "Round",
            "goto": ("chargen_appearance_template", kwargs | {"eye_type": "round"}),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def appearance_nose_type(caller, raw_string, **kwargs):
    text = "|CSelect your Nose Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_nose_type"},
        {
            "key": ("1", "aquiline", "a"),
            "desc": "Aquiline",
            "goto": ("chargen_appearance_template", kwargs | {"nose_type": "aquiline"}),
        },
        {
            "key": ("2", "button", "b"),
            "desc": "Button",
            "goto": ("chargen_appearance_template", kwargs | {"nose_type": "button"}),
        },
        {
            "key": ("3", "flat", "f"),
            "desc": "Flat",
            "goto": ("chargen_appearance_template", kwargs | {"nose_type": "flat"}),
        },
        {
            "key": ("4", "wide", "w"),
            "desc": "Wide",
            "goto": ("chargen_appearance_template", kwargs | {"nose_type": "wide"}),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def appearance_mouth_type(caller, raw_string, **kwargs):
    text = "|CSelect your Mouth Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_mouth_type"},
        {
            "key": ("1", "full", "f"),
            "desc": "Full",
            "goto": ("chargen_appearance_template", kwargs | {"mouth_type": "full"}),
        },
        {
            "key": ("2", "small", "s"),
            "desc": "Small",
            "goto": ("chargen_appearance_template", kwargs | {"mouth_type": "small"}),
        },
        {
            "key": ("3", "thin", "t"),
            "desc": "Thin",
            "goto": ("chargen_appearance_template", kwargs | {"mouth_type": "thin"}),
        },
        {
            "key": ("4", "wide", "w"),
            "desc": "Wide",
            "goto": ("chargen_appearance_template", kwargs | {"mouth_type": "wide"}),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def appearance_jaw_type(caller, raw_string, **kwargs):
    text = "|CSelect your Jaw Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_jaw_type"},
        {
            "key": ("1", "pointed", "p"),
            "desc": "Pointed",
            "goto": ("chargen_appearance_template", kwargs | {"jaw_type": "pointed"}),
        },
        {
            "key": ("2", "round", "r"),
            "desc": "Round",
            "goto": ("chargen_appearance_template", kwargs | {"jaw_type": "round"}),
        },
        {
            "key": ("3", "square", "s"),
            "desc": "Square",
            "goto": ("chargen_appearance_template", kwargs | {"jaw_type": "square"}),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def appearance_eyebrow_type(caller, raw_string, **kwargs):
    text = "|CSelect your Eyebrow Type|n:\n"
    options = (
        {"key": "", "goto": "appearance_eyebrow_type"},
        {
            "key": ("1", "arched", "a"),
            "desc": "Arched",
            "goto": (
                "chargen_appearance_template",
                kwargs | {"eyebrow_type": "arched"},
            ),
        },
        {
            "key": ("2", "straight", "s"),
            "desc": "Straight",
            "goto": (
                "chargen_appearance_template",
                kwargs | {"eyebrow_type": "straight"},
            ),
        },
        {
            "key": ("3", "thick", "t"),
            "desc": "Thick",
            "goto": ("chargen_appearance_template", kwargs | {"eyebrow_type": "thick"}),
        },
        {
            "key": ("4", "thin", "th"),
            "desc": "Thin",
            "goto": ("chargen_appearance_template", kwargs | {"eyebrow_type": "thin"}),
        },
        {"key": "_default", "goto": "chargen_appearance_template"},
    )

    return text, options


def chargen_finalize(caller, raw_string):
    return "", ""
