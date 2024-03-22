FIEND = {
    "key": "fiend",
    "name": "|rFiend|n",
    "typeclass": "typeclasses.mobs.Monster",
    "prototype": "world.tutorial.prototypes.mobs.FIEND",
    "location": (1, 3),
    "desc": "The creature's limbs contort with the discord of nature's laws broken. A skin of discomforting pallid greens melding into deep purples resembles a bruised sky after tempest, both taut and strangely glistening with a veneer of unwholesome moisture. Eyes offset the countenance of the beast, scattered as if by a mad painter's errant brush, their luminescence piercing the surroundings with malevolent interest. Tatters of flesh drape about its gaunt frame. Nestled within the fiend's ghastly visage, a cavernous mouth agape reveals a nightmare collection of fangs, asymmetrical and serrated like the remnants of a shattered iron gate. Its tongue spills forth with sickening liberty, painting the air with the anticipation.",
    "senses": {
        "feel": "A shiver traverses the spine, born of the inherent cold that seems to emanate from the fiend's grotesque form.",
        "smell": "The stench of moist earth and the aftermath of a fierce blaze combine to assault the senses with a scent most foul.",
        "sound": "The silence is pierced by the subtle shiftings of this abomination, the scrape of its talons a grim melody upon the hardened earth.",
        "taste": "A metallic tang invades the mouth, as though the mere sight of the fiend sours the air and poisons the tongue.",
    },
    # "spawns": [martial.SCIMITAR, clothing.SIMPLE_ROBE],
    "stats": {
        "strength": 5,
        "dexterity": 8,
        "constitution": 10,
        "intelligence": 8,
        "wisdom": 9,
        "charisma": 10,
        "health": 6,
    },
    "quantity": 3,
}

ENCHANTRESS = {
    "key": "enchantress",
    "name": "|cTrapped Enchantress|n",
    "typeclass": "world.tutorial.mobs.Enchantress",
    "prototype": "world.tutorial.prototypes.mobs.ENCHANTRESS",
    "location": (4, 3),
    # gender: female
    "desc": "With eyes like the twilight sky after a storm, she holds a universe of wisdom veiled beneath a countenance marked by trials unknown. Her visage, fair as the last bloom of winter, carries the freckles of a warrior painted by the brush of skirmish. Trapped as she is, behind the gnarled ironwork of her cell, there's an insidious darkness that shrouds her form. The hold's malignant grimness mocks her with its unyielding decay, the iron lattice of her door sealed by salt and moisture.",
    # "interaction": "world.tutorial.interactions.enchantress",
}

CULTIST = {
    "key": "cultist",
    "name": "|xCultist|n",
    "typeclass": "typeclasses.mobs.Mob",
    "prototype": "world.tutorial.prototypes.mobs.CULTIST",
    "location": (4, 2),
    "desc": "Enshrouded in a tattered robe of the deepest nightshade, a cultist stands, a supplicant to secret and eldritch forces beyond mortal ken. The garment veils the figure in mystery, obscuring the outlines of humanity. Upon the figure's head, a hood looms shadowy, half-concealing a visage that bears the etchings of devotion and madness intertwined like the roots of some blighted tree. This face is hollow-cheeked and with skin as pallid as the underbelly of a long-dead fish.",
    "senses": {
        "feel": "A sensation of prickled apprehension sweeps to the skin, as an unseen aura of fanaticism emanates from the cloaked figure.",
        "smell": "The air is thick with the musk of incense turned heavy and cloying, weaving a tapestry of scent that speaks to clandestine gatherings.",
        "sound": "A low chant, barely more than the breath of wind through a keyhole, suggests the presence of well-guarded secrets.",
        "taste": "The back of the throat catches an acrid taste, akin to the sudden fear that perhaps the reality of these obscure doctrines is more tangible than once believed.",
    },
    "stats": {
        "strength": 11,
        "dexterity": 12,
        "constitution": 10,
        "intelligence": 10,
        "wisdom": 11,
        "charisma": 10,
        "health": 9,
    },
}

BEHEMOTH = {
    "key": "behemoth",
    "name": "|xBehemoth|n",
    "typeclass": "typeclasses.mobs.Monster",
    "prototype": "world.tutorial.prototypes.mobs.BEHEMOTH",
    "location": (3, 2),
    "desc": "The Behemoth looms, a colossus sculpted by the somber hands of shadow itself. Its eyes, twin embers smoldering beneath the craggy brow of a primeval cliff, pierce the murk with an infernal glow. The massive creature bears a carapace as intricate as the wrought gates of a forsaken fortress. Its formidable countenance, framed by a serrated beak sharp as the guillotine's blade, betrays a visage not of this gentle Earth. Muscle-bound limbs, hewn as if from the roots of ancient oaks, carry it forward with the inevitability of a tempest's advance.",
    "stats": {
        "strength": 12,
        "dexterity": 11,
        "constitution": 12,
        "intelligence": 6,
        "wisdom": 8,
        "charisma": 5,
        "health": 11,
    },
}

COMMANDER = {
    "key": "commander",
    "name": "|rCommander Ambrose Harrowgate|n",
    "aliases": [
        "ambrose",
        "harrowgate",
        "ambrose harrowgate",
        "commander harrowgate",
        "commander ambrose harrowgate",
    ],
    "typeclass": "typeclasses.mobs.Mob",
    "prototype": "world.tutorial.prototypes.mobs.COMMANDER",
    "location": (3, 4),
    # gender: male,
    "desc": "His presence is as commanding as the rolling waves, his features carved by salt winds and the unforgiving sun. Indomitable winter-blue eyes gleam with the wisdom of ancient mariners and stories of the deep. A heavy, dark beard, peppered with the white of seafoam, adorns a face weathered and bronzed. Adorned in a long coat that fluttered like a banner against the relentless wind, his hands are calloused and firm, each scar and rough patch a chronicle of survival and mastery of the aquatic realm.",
    "senses": {
        "feel": "An aura of respect and subtle intimidation surrounds him, akin to the anticipation before a storm's first mighty thunderclap.",
        "smell": "The essence of brine and aged wood mingles with the natural musk of a life spent at sea, omnipresent on his being.",
        "sound": "His words cut through the din of water and wind, each command resonating with the power of the waves he has long conquered.",
        "taste": "The air around him carries the tang of salt, a reminder of his unbreakable bond with the boundless seas.",
    },
    "stats": {
        "strength": 20,
        "dexterity": 18,
        "constitution": 16,
        "intelligence": 14,
        "wisdom": 12,
        "charisma": 16,
        "health": 150,
    },
}

MOBILE_PROTOTYPES = {
    "fiend": FIEND,
    "enchantress": ENCHANTRESS,
    "cultist": CULTIST,
    "behemoth": BEHEMOTH,
    "commander": COMMANDER,
}

__all__ = (
    FIEND,
    ENCHANTRESS,
    CULTIST,
    BEHEMOTH,
    COMMANDER,
)


# MOBILE_PROTOTYPES = {
#     "fiend": {
#         "key": "fiend",
#         "name": "|rFiend|n",
#         "typeclass": "typeclasses.mobs.Monster",
#         "prototype": "world.tutorial.prototypes.mobs.FIEND",
#         "location": (1, 3),
#         "desc": "The creature's limbs contort with the discord of nature's laws broken. A skin of discomforting pallid greens melding into deep purples resembles a bruised sky after tempest, both taut and strangely glistening with a veneer of unwholesome moisture. Eyes offset the countenance of the beast, scattered as if by a mad painter's errant brush, their luminescence piercing the surroundings with malevolent interest. Tatters of flesh drape about its gaunt frame. Nestled within the fiend's ghastly visage, a cavernous mouth agape reveals a nightmare collection of fangs, asymmetrical and serrated like the remnants of a shattered iron gate. Its tongue spills forth with sickening liberty, painting the air with the anticipation.",
#         "senses": {
#             "feel": "A shiver traverses the spine, born of the inherent cold that seems to emanate from the fiend's grotesque form.",
#             "smell": "The stench of moist earth and the aftermath of a fierce blaze combine to assault the senses with a scent most foul.",
#             "sound": "The silence is pierced by the subtle shiftings of this abomination, the scrape of its talons a grim melody upon the hardened earth.",
#             "taste": "A metallic tang invades the mouth, as though the mere sight of the fiend sours the air and poisons the tongue.",
#         },
#         # "spawns": [martial.SCIMITAR, clothing.SIMPLE_ROBE],
#         "stats": {
#             "strength": 5,
#             "dexterity": 8,
#             "constitution": 10,
#             "intelligence": 8,
#             "wisdom": 9,
#             "charisma": 10,
#             "health": 6,
#         },
#         "quantity": 3,
#     },
#     "enchantress": {
#         "key": "enchantress",
#         "name": "|cTrapped Enchantress|n",
#         "typeclass": "world.tutorial.mobs.Enchantress",
#         "prototype": "world.tutorial.prototypes.mobs.ENCHANTRESS",
#         "location": (4, 3),
#         # gender: female
#         "desc": "With eyes like the twilight sky after a storm, she holds a universe of wisdom veiled beneath a countenance marked by trials unknown. Her visage, fair as the last bloom of winter, carries the freckles of a warrior painted by the brush of skirmish. Trapped as she is, behind the gnarled ironwork of her cell, there's an insidious darkness that shrouds her form. The hold's malignant grimness mocks her with its unyielding decay, the iron lattice of her door sealed by salt and moisture.",
#         # "interaction": "world.tutorial.interactions.enchantress",
#     },
#     "cultist": {
#         "key": "cultist",
#         "name": "|xCultist|n",
#         "typeclass": "typeclasses.mobs.Mob",
#         "prototype": "world.tutorial.prototypes.mobs.CULTIST",
#         "location": (4, 2),
#         "desc": "Enshrouded in a tattered robe of the deepest nightshade, a cultist stands, a supplicant to secret and eldritch forces beyond mortal ken. The garment veils the figure in mystery, obscuring the outlines of humanity. Upon the figure's head, a hood looms shadowy, half-concealing a visage that bears the etchings of devotion and madness intertwined like the roots of some blighted tree. This face is hollow-cheeked and with skin as pallid as the underbelly of a long-dead fish.",
#         "senses": {
#             "feel": "A sensation of prickled apprehension sweeps to the skin, as an unseen aura of fanaticism emanates from the cloaked figure.",
#             "smell": "The air is thick with the musk of incense turned heavy and cloying, weaving a tapestry of scent that speaks to clandestine gatherings.",
#             "sound": "A low chant, barely more than the breath of wind through a keyhole, suggests the presence of well-guarded secrets.",
#             "taste": "The back of the throat catches an acrid taste, akin to the sudden fear that perhaps the reality of these obscure doctrines is more tangible than once believed.",
#         },
#         "stats": {
#             "strength": 11,
#             "dexterity": 12,
#             "constitution": 10,
#             "intelligence": 10,
#             "wisdom": 11,
#             "charisma": 10,
#             "health": 9,
#         },
#     },
#     "behemoth": {
#         "key": "behemoth",
#         "name": "|xBehemoth|n",
#         "typeclass": "typeclasses.mobs.Monster",
#         "prototype": "world.tutorial.prototypes.mobs.BEHEMOTH",
#         "location": (3, 2),
#         "desc": "The Behemoth looms, a colossus sculpted by the somber hands of shadow itself. Its eyes, twin embers smoldering beneath the craggy brow of a primeval cliff, pierce the murk with an infernal glow. The massive creature bears a carapace as intricate as the wrought gates of a forsaken fortress. Its formidable countenance, framed by a serrated beak sharp as the guillotine's blade, betrays a visage not of this gentle Earth. Muscle-bound limbs, hewn as if from the roots of ancient oaks, carry it forward with the inevitability of a tempest's advance.",
#         "stats": {
#             "strength": 12,
#             "dexterity": 11,
#             "constitution": 12,
#             "intelligence": 6,
#             "wisdom": 8,
#             "charisma": 5,
#             "health": 11,
#         },
#     },
#     "commander": {
#         "key": "commander",
#         "name": "|rCommander Ambrose Harrowgate|n",
#         "aliases": [
#             "ambrose",
#             "harrowgate",
#             "ambrose harrowgate",
#             "commander harrowgate",
#             "commander ambrose harrowgate",
#         ],
#         "typeclass": "typeclasses.mobs.Mob",
#         "prototype": "world.tutorial.prototypes.mobs.COMMANDER",
#         "location": (3, 4),
#         # gender: male,
#         "desc": "His presence is as commanding as the rolling waves, his features carved by salt winds and the unforgiving sun. Indomitable winter-blue eyes gleam with the wisdom of ancient mariners and stories of the deep. A heavy, dark beard, peppered with the white of seafoam, adorns a face weathered and bronzed. Adorned in a long coat that fluttered like a banner against the relentless wind, his hands are calloused and firm, each scar and rough patch a chronicle of survival and mastery of the aquatic realm.",
#         "senses": {
#             "feel": "An aura of respect and subtle intimidation surrounds him, akin to the anticipation before a storm's first mighty thunderclap.",
#             "smell": "The essence of brine and aged wood mingles with the natural musk of a life spent at sea, omnipresent on his being.",
#             "sound": "His words cut through the din of water and wind, each command resonating with the power of the waves he has long conquered.",
#             "taste": "The air around him carries the tang of salt, a reminder of his unbreakable bond with the boundless seas.",
#         },
#         "stats": {
#             "strength": 20,
#             "dexterity": 18,
#             "constitution": 16,
#             "intelligence": 14,
#             "wisdom": 12,
#             "charisma": 16,
#             "health": 150,
#         },
#     },
# }
