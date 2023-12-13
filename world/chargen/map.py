CHARGEN_MAP = r"""
 + 0
   
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
}

CREATION_ROOM_PARENT = {"typeclass": "typeclasses.chargen.rooms.CreationRoom"}
CREATION_EXIT_PARENT = {"typeclass": "typeclasses.exits.XYExit"}

for key, prot in PROTOTYPES.items():
    if len(key) == 2:
        prot["prototype_parent"] = CREATION_ROOM_PARENT
    else:
        prot["prototype_parent"] = CREATION_EXIT_PARENT

XYMAP_DATA = {
    "zcoord": "chargen",
    "map": CHARGEN_MAP,
    "prototypes": PROTOTYPES,
}
