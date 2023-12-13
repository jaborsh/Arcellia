CHARGEN_MAP = r"""
 + 0

 5 #

 4 #

 3 #

 2 #

 1 #
   
 0 #

 + 0
"""

PROTOTYPES = {
    (0, 0): {
        "key": "|wArcellia - Sanctum of Arrival|n",
        "desc": "There is a peculiar equilibrium: neither warmth nor chill, brightness nor shadow - this is the cradle of beginnings, a sanctuary untouched by the passage of time or the fleetingness of mortality. This place is the absence of all things, and the sheer and utter silence of that nothingness covers the expanse like a thick blanket. Oblivion is peaceful; yet amongst the muted gray tranquility, there is a discordant spark of chaos, the faintest heartbeat: a blip of existence.|/|/    It is you.|/|/    You, the nascent traveler, float amidst this gentle void. A mere wisp of consciousness, you harbor the power to mold your very essence. Here in this prelude to adventure, the choice of one's very existence is the first dalliance with creation.|/|/    A whisper of thought suffices, and the echoes shall craft your being - masculine, feminine, or the enigmatic allure of that which transcends such simple definitions.",
        "senses": {
            "feel": "A serene comfort envelops you, like floating in a tranquil sea of possibility.",
            "smell": "The scent of creation, raw and primeval, faintly fills the void.",
            "sound": "An expectant hush pervades, the quiet before a new beginning.",
            "taste": "The essence of potential lingers on the palate, as if tasting the very air cound speak of worlds unexplored.",
        },
    },
    (0, 1): {
        "key": "|wArcellia - Sanctum of Heritage|n",
        "desc": "Beneath the gaze of watchful stars, you pass like a breath through the threshold of possibility, drawn by an invisible thread towards the chamber of lineage. Here, encased in walls unseen, the very air pulses with an ancestral chorus, the echoes of eons whispering of bloodlines steeped in legend and lore. A kaleidoscope of histories swirls in a phantom dance, each thread yearning to be plucked and woven into the fabric of your being.",
        "senses": {
            "feel": "The air teems with the invisible warmth of countless hearths and the chill of untrodded paths.",
            "smell": "Fleeting scents waft by - pine's crispness, the earth's musk, the sea's salt.",
            "sound": "Faint murmurs of ancient tongues and the resonance of distant lands manifest as if every race whispers its own invitation.",
            "taste": "Each potential lineage bestows upon the tongue the subtle flavor of its distinct land: a touch of iron, hints of honeyed mead, a zest of sea foam.",
        },
    },
    (0, 2): {
        "key": "|wArcellia - Sanctum of Vocation|n",
        "desc": "The next vault unfurls, adorned with the invisible relics of triumph and travail, a pantheon of purpose laid out like a grand feast. Here in the sanctum of vocation, the essence of every deed ever dared whispers of the roles that shape destiny's spine.|/|/    Swords lay upon a wall, edges shining with the promise of valor. Tomes line a shelf, holding arcane secrets to dance at the fingertips. The writing of a prayer is etched into a plaque, speaking to compassion and balming frayed souls. Other relics abound, each mantles of ancient crafts and purposes.",
        "senses": {
            "feel": "The air crackles with anticipation, heavy with the gravity of tradition.",
            "smell": "Scents of leather, aged parchment, and smoldering embers curl through the space.",
            "sound": "Soft clamors of battle, murmured incantations, and the soothing cadence of life-giving chants fill the chamber like an orchestra.",
            "taste": "The air bears the salt of sweat, the sweetness of triumph, and the bitter tang of fallen ambition.",
        },
    },
    (0, 3): {
        "key": "|wArcellia - Sanctum of History|n",
        "desc": "You find yourself in an austere chamber bathed in the soft glow of opportunity. This is a repository of lives past, the walls lined with alcoves, each a window into the essence of myriad backgrounds. The chamber, an architect's marvel, is cylindrical in shape, with shelves gracefully curving along its walls, each bearing relics and tomes.|/|/    Looming gracefully above, a domed ceiling painted with murals of epic tales captures the reverence of a thousand watchful eyes. The space, though unmistakably grand, conveys an intimate sense, as though history itself converges to cradle one's decision. Each background stands as a living tableau, rich in detail: inkwells and quills that quiver with untold stories, maps of distant shores promising the romance of the unknown, and humble tools of trade whispering of craftsmanship and daily toil.",
        "senses": {
            "feel": "A reverent stillness caresses the skin.",
            "smell": "A mosaic of scents looms - leather, ink, fresh hay.",
            "sound": "The faint rustle of parchment and a distant echo of labor create an atmosphere of industrial candor.",
            "taste": "The air yields flavors of ink and timber, a subtle, nourishing blend.",
        },
    },
    (0, 4): {
        "key": "|wArcellia - Sanctum of Reflection|n",
        "desc": "You advance towards a luminous gallery, an atrium of mirrors that reflect not just form, but the essence of self. The sanctum of reflection, pristine and hushed, offers one such mirror for every soul to step within its confines.|/|/    Shimmering surfaces line the chamber, suspended in timeless grace, each an artisan's masterpiece framed in ornate craftsmanship. The floors, inlaid with pearlescent tiles, shine with an inner light that casts a warm, inviting glow upon the room, dancing upon each reflective pane like the soft touch of dawn.|/|/    The glass, still and patient, awaits the contours of your flesh, the hue of your complexion, the sweep of your hair. Eyes, the lanterns of the spirit, seek their color and sparkle from within these silent guides.",
        "senses": {
            "feel": "The caress of tranquil air embraces you, nuturing the blossoming of your corporeal self.",
            "smell": "Amidst the clinical absence of fragrance, a clean and pure scent underlines the sanctity of this space.",
            "sound": "The muted whispers of your own movement resonate softly, as if the quiet itself lends an ear to your direction.",
            "taste": "The air is pregnant with the cirspness of creation, refreshing and invigorating the soul poised on the cusp of self-realization.",
        },
    },
    (0, 5): {
        "key": "|wArcellia - Sanctum of Soul|n",
        "desc": "You traverse the threshold into a chamber of an altogether more cerebral nature. Within these confines, the abstract becomes tangible, a spacious hall where the elements of mind and body are hewn into the building blocks of capability. The ambient glow of cognition suffuses the air, each ray cast from luminescent orbs that float by as if suspended by an enchanter's hand.|/|/    Knowledge and prowess align in a grand array of pedestals, each bearing an emblem of the traits one may possess. Strength's sigil rests on a pillar of stone. Intelligence lies inscribed upon a prism. Dexterity, constitution, wisdom, charisma - each attribute presented as a resplendent icon of personal excellence.",
        "senses": {
            "feel": "A purposeful energy courses through the chamber, electrifying your skin.",
            "smell": "The scent of oiled metal and weatherworn tomes blend.",
            "sound": "A low hum of ethereal harmonics reverberates, the resonance echoing off the chamber's walls.",
            "taste": "The air carries hints of metallic tang and crisp parchment.",
        },
    },
}

CREATION_ROOM_PARENT = {"typeclass": "typeclasses.chargen.rooms.CreationRoom"}
CREATION_ROOM_INTRO = {"typeclass": "typeclasses.chargen.rooms.CreationRoomIntro"}
CREATION_ROOM_RACE = {"typeclass": "typeclasses.chargen.rooms.CreationRoomRace"}
CREATION_ROOM_CLASS = {"typeclass": "typeclasses.chargen.rooms.CreationRoomClass"}
CREATION_ROOM_BACKGROUND = {
    "typeclass": "typeclasses.chargen.rooms.CreationRoomBackground"
}
CREATION_ROOM_APPEARANCE = {
    "typeclass": "typeclasses.chargen.rooms.CreationRoomAppearance"
}
CREATION_ROOM_ATTRIBUTES = {
    "typeclass": "typeclasses.chargen.rooms.CreationRoomAttributes"
}

CREATION_EXIT_PARENT = {"typeclass": "typeclasses.exits.XYExit"}

for key, prot in PROTOTYPES.items():
    if len(key) == 2:
        if key == (0, 0):
            prot["prototype_parent"] = CREATION_ROOM_INTRO
        elif key == (0, 1):
            prot["prototype_parent"] = CREATION_ROOM_RACE
        elif key == (0, 2):
            prot["prototype_parent"] = CREATION_ROOM_CLASS
        elif key == (0, 3):
            prot["prototype_parent"] = CREATION_ROOM_BACKGROUND
        elif key == (0, 4):
            prot["prototype_parent"] = CREATION_ROOM_APPEARANCE
        elif key == (0, 5):
            prot["prototype_parent"] = CREATION_ROOM_ATTRIBUTES
        else:
            prot["prototype_parent"] = CREATION_ROOM_PARENT
    else:
        prot["prototype_parent"] = CREATION_EXIT_PARENT

XYMAP_DATA = {
    "zcoord": "chargen",
    "map": CHARGEN_MAP,
    "prototypes": PROTOTYPES,
}
