from handlers.clothing.clothing_types import ClothingType

# Mobs
NAUTILUS_FIEND = {
    "key": "fiend",
    "display_name": "|rFiend|n",
    "typeclass": "typeclasses.mobs.Mob",
    "desc": "The creature's limbs contort with the discord of nature's laws broken. A skin of discomforting pallid greens melding into deep purples resembles a bruised sky after tempest, both taut and strangely glistening with a veneer of unwholesome moisture. Eyes offset the countenance of the beast, scattered as if by a mad painter's errant brush, their luminescence piercing the surroundings with malevolent interest. Tatters of flesh drape about its gaunt frame. Nestled within the fiend's ghastly visage, a cavernous mouth agape reveals a nightmare collection of fangs, asymmetrical and serrated like the remnants of a shattered iron gate. Its tongue spills forth with sickening liberty, painting the air with the anticipation.",
    "prototype_tags": [("nautilus", "zone")],
    "senses": {
        "feel": "A shiver traverses the spine, born of the inherent cold that seems to emanate from the fiend's grotesque form.",
        "smell": "The stench of moist earth and the aftermath of a fierce blaze combine to assault the senses with a scent most foul.",
        "sound": "The silence is pierced by the subtle shiftings of this abomination, the scrape of its talons a grim melody upon the hardened earth.",
        "taste": "A metallic tang invades the mouth, as though the mere sight of the fiend sours the air and poisons the tongue.",
    },
}

NAUTILUS_ENCHANTRESS = {
    "key": "enchantress",
    "display_name": "|cEnchantress|n",
    "typeclass": "world.nautilus.mobs.Enchantress",
    "desc": "With eyes like the twilight sky after a storm, she holds a universe of wisdom veiled beneath a countenance marked by trials unknown. Her visage, fair as the last bloom of winter, carries the freckles of a warrior painted by the brush of skirmish. Trapped as she is, behind the gnarled ironwork of her cell, there's an insidious darkness that shrouds her form. The hold's malignant grimness mocks her with its unyielding decay, the iron lattice of her door sealed by salt and moisture.",
    "prototype_tags": [("nautilus", "zone")],
    "senses": {
        "feel": "The damp walls have leeched the warmth from her skin, leaving her perpetually chilled to the bone.",
        "smell": "A faint whiff of her own perfume - a ghostly reminder of her former life now nearly overpowered by sea salt and decay.",
        "sound": "The soft rustle of her own clothing as she shifts in her confinement, and barely the audible whisper of her own breath.",
        "taste": "A memory of sweet berries and fresh spring water.",
    },
    "interaction": "world.nautilus.interactions.enchantress",
}

NAUTILUS_CULTIST = {
    "key": "cultist",
    "display_name": "|xCultist|n",
    "typeclass": "typeclasses.mobs.Mob",
    "desc": "Enshrouded in a tattered robe of the deepest nightshade, a cultist stands, a supplicant to secret and eldritch forces beyond mortal ken. The garment veils the figure in mystery, obscuring the outlines of humanity. Upon the figure's head, a hood looms shadowy, half-concealing a visage that bears the etchings of devotion and madness intertwined like the roots of some blighted tree. This face is hollow-cheeked and with skin as pallid as the underbelly of a long-dead fish.",
    "prototype_tags": [("nautilus", "zone")],
    "senses": {
        "feel": "A sensation of prickled apprehension sweeps to the skin, as an unseen aura of fanaticism emanates from the cloaked figure.",
        "smell": "The air is thick with the musk of incense turned heavy and cloying, weaving a tapestry of scent that speaks to clandestine gatherings.",
        "sound": "A low chant, barely more than the breath of wind through a keyhole, suggests the presence of well-guarded secrets.",
        "taste": "The back of the throat catches an acrid taste, akin to the sudden fear that perhaps the reality of these obscure doctrines is more tangible than once believed.",
    },
}

NAUTILUS_BEHEMOTH = {
    "key": "behemoth",
    "display_name": "|xBehemoth|n",
    "typeclass": "typeclasses.mobs.Mob",
    "desc": "The behemoth looms, a colossus sculpted by the somber hands of shadow itself. Its eyes, twin embers smoldering beneath the craggy brow of a primeval cliff, pierce the murk with an infernal glow. The massive creature bears a carapace as intricate as the wrought gates of a forsaken fortress. Its formidable countenance, framed by a serrated beak sharp as the guillotine's blade, betrays a visage not of this gentle Earth. Muscle-bound limbs, hewn as if from the roots of ancient oaks, carry it forward with the inevitability of a tempest's advance.",
    "prototype_tags": [("nautilus", "zone")],
    "senses": {
        "feel": "The ground trembles beneath the behemoth's titanic tread, each footfall sending shockwaves through the earth. The air grows heavy with an oppressive, suffocating presence as the creature draws near.",
        "smell": "A pungent, ancient odor emanates from the behemoth, a blend of musty caverns, decaying foliage, and the acrid tang of brimstone. The scent is overwhelming, invading the nostrils and lingering like a malevolent miasma.",
        "sound": "The behemoth's approach is heralded by a symphony of dread: the grinding of stone against stone, the creaking of its armored plates, and the low, rumbling growl that echoes from deep within its cavernous chest.",
        "taste": "The air around the behemoth is thick with an unsettling, metallic taste, as if the very essence of the creature has seeped into the atmosphere. It coats the tongue like the bitter residue of fear and leaves a lingering, unpleasant aftertaste.",
    },
}

NAUTILUS_COMMANDER = {
    "key": "commander",
    "display_name": "|rCommander Ambrose Harrowgate|n",
    "aliases": ["ambrose", "harrowgate"],
    "typeclass": "typeclasses.mobs.Mob",
    "desc": "His presence is as commanding as the rolling waves, his features carved by salt winds and the unforgiving sun. Indomitable winter-blue eyes gleam with the wisdom of ancient mariners and stories of the deep. A heavy, dark beard, peppered with the white of seafoam, adorns a face weathered and bronzed. Adorned in a long coat that fluttered like a banner against the relentless wind, his hands are calloused and firm, each scar and rough patch a chronicle of survival and mastery of the aquatic realm.",
    "prototype_tags": [("nautilus", "zone")],
    "senses": {
        "feel": "An aura of respect and subtle intimidation surrounds him, akin to the anticipation before a storm's first mighty thunderclap.",
        "smell": "The essence of brine and aged wood mingles with the natural musk of a life spent at sea, omnipresent on his being.",
        "sound": "His words cut through the din of water and wind, each command resonating with the power of the waves he has long conquered.",
        "taste": "The air around him carries the tang of salt, a reminder of his unbreakable bond with the boundless seas.",
    },
}

# Interactives
NAUTILUS_BROKEN_BODY = {
    "typeclass": "typeclasses.objects.InteractiveObject",
    "key": "broken body",
    "display_name": "|#9E768FBroken Body|n",
    "aliases": ["body", "corpse"],
    "desc": "The figure is a tragic centerpiece amidst the room's cartographic splendor. Seated with their cranium partially exposed to the whims of cruel fate, their visage is frozen in an eerie semblance of ponderous thought. The soft, vulnerable tissue of the brain is a stark contrast to the rigid discipline of the maps that encircle them. Traces of blood, now dry and darkened, have painted rivulets along their weathered skin - a macabre depiction of the body's fragility.|/|/|y[Hint]|n: Maybe you can |C'interact'|n with the body.",
    "locks": "get:pperm(Admin)",
    "prototype_tags": [("nautilus", "zone")],
    "tags": ["interactive"],
    "senses": {
        "feel": "A visceral discomfort arises at the sight, a tension that coils in the pit of one's being, as if in the presence of nature's uncanny aberration.",
        "smell": "The metallic pungency of blood intermingles with the sterile scent of exposed cerebral matter.",
        "sound": "An unsettling silence emanates from the figure, their breaths having long since yielded to the quietude that now claims the air.",
        "taste": "Clinically bitter, the mind's flesh exudes an intangible flavor that speaks to innermost sanctums violated.",
    },
    "interaction": "world.nautilus.interactions.broken_body",
}

NAUTILUS_LEFT_LEVER = {
    "key": "left lever",
    "aliases": ["lever"],
    "display_name": "|#0047ABLeft Lever|n",
    "desc": "Its polished steel handle catches the eye like a diamond in the rough. The lever's base is firmly anchored to the ship's hull. The smooth metal bears the patina of age.\n\n|y[Hint]|n: Maybe you can |C'pull'|n the lever.",
    "locks": "get:pperm(Admin)",
    "prototype_tags": [("nautilus", "zone")],
    "senses": {
        "feel": "The lever's handle is smooth and cool to the touch, its solid presence reassuring in the hand.",
        "smell": "The faint scent of oil and salty sea air mingles around the lever.",
        "sound": "The gentle creaking of the ship's timbers and the distant lapping of waves against the hull fill the air.",
        "taste": "The tang of salt on the lips and the mentallic taste of the lever linger.",
    },
}

NAUTILUS_RIGHT_LEVER = {
    "key": "right lever",
    "aliases": ["lever"],
    "display_name": "|#4B7F52|nRight Lever|n",
    "desc": "Lurking in the shadows, the right lever looms like a sinister specter. Its tarnished steel handle seems to recoil from the light as if harboring dark secrets. The lever's base is haphazardly welded to the ship's hull, a cruel mockery of its counterpart's steadfast purpose.\n\n|y[Hint]|n: You should probably not |C'pull'|n this lever.",
    "locks": "get:pperm(Admin)",
    "prototype_tags": [("nautilus", "zone")],
    "senses": {
        "feel": "The lever's handle is rough and pitted, its surface seeming to writhe beneath the touch like something alive and malignant.",
        "smell": "The acrid strench of decay hangs heavily around the right lever.",
        "sound": "The ominous groaning of tortured metal echo in the vicinity.",
        "taste": "The bitter, coppery tang of blood coats the tongue.",
    },
}

# Weapons
NAUTILUS_EMBERWISP_BLADE = {
    "key": "blade",
    "display_name": "|rEmberwisp Blade|n",
    "aliases": ["emberwisp", "emberwisp blade"],
    "typeclass": "world.nautilus.weapons.EmberwispBlade",
    "desc": "This sword is a union of lethality and enchantment, its metal forged in the breath of a dragon's smoldering heart. While dormant within its scabbard, the appearance of the weapon is unassuming, its potential for inferno veiled. However, at the moment of unsheathing, a marvel unfolds: silent flames awaken and run along the blade's edge, a visual serenade of fire. The steel surface alights with an ethereal blaze that mimics the auroras in the night sky - crimson, gold, and scarlet coalescing into a visual choir.",
    "prototype_tags": [("nautilus", "zone")],
    "senses": {
        "feel": "One feels a curious warmth suffuse the hand, the sensation of power harnessed and awaiting command.",
        "smell": "The air around the drawn sword fills with the scent of embers rekindled, the fragrance of a hearth without the sting of smoke.",
        "sound": "Silence enshrouds the flaming spectacle; the blaze dances without the crackle and spit of true fire, a sorcery wrought in quietude.",
        "taste": "A taste akin to the warmth of spiced wine teases the senses when the sword is bared, a savor of comfort and might intertwined.",
    },
}

# Armor

# Clothing
NAUTILUS_ASCETIC_ROBES = {
    "key": "robes",
    "display_name": "|#654321Ascetic Robes|n",
    "typeclass": "typeclasses.clothing.Clothing",
    "clothing_type": ClothingType.FULLBODY,
    "desc": "A striking ensemble that blends the austerity of a monastic lifestyle with the grace of a trained killer. The form-fitting bodysuit is of a deep, earthy brown that seems to absorb the light around it. Across the chest, a series of crisscrossing straps in a darker shade of brown create a harness-like effect. The straps draw the eye to the outfit's centerpiece: a plunging V-neckline that dips daringly low, revealing an unexpected touch of allure to an otherwise austere garb. The sleeves are long and fitted. Around the waist, a belt of the same dark brown material cinches the garment, creating an hourglass silhouette to emphasize the wearer's build. The lower half of the outfit is no less intriguing, with the bodysuit continuing in its sleek, uninterrupted lines. The legs are encased in the same rich, chocolate-hued fabric which clings to every curge and muscle.",
    "prototype_tags": [("nautilus", "zone")],
    "senses": {
        "feel": "The bodysuit feels smooth and supple, like a second skin that moves with every breath and gesture, while the straps and belt provide a reassuring sense of structure and support.",
        "smell": "A faint whiff of lime and the crisp, clean scent of soap linger about the outfit, mingling with the earthy aroma of well-worn leather.",
        "sound": "The soft whisper of fabric against fabric.",
        "taste": "The robes carry a hint of the astringent taste of lime.",
    },
}

# Objects
NAUTILUS_WOODEN_CHEST = {
    "key": "chest",
    "display_name": "|YWooden Chest|n",
    "typeclass": "typeclasses.objects.Object",
    "desc": "Crafted from the heartwood of ancient trees, the chest's exterior is sheathed in grain patterns that swirl and weave across its surface like tales told in timber. The chest's sturdy form invites touch, the solid wood yielding ever so slightly to the caress of a curious hand. Stout, hand-carved legs support it, resembling the strong limbs of the very trees from whence it came. Its lid, hinged gracefully, appears to beckon one to witness the secrets nested within its hollow.",
    "locks": "get:pperm(Admin)",
    "prototype_tags": [("nautilus", "zone")],
    "senses": {
        "feel": "The chest's surface carries the subtle roughness of grain.",
        "smell": "It exudes a wholesome aroma of wood and resin, reminiscent of a forest at dawn.",
        "sound": "A soft creak accompanies the lifting of the lid.",
        "taste": "The air around it is laced with the faint, tannic flavor of bark and the earthiness of fallen leaves.",
    },
}

NAUTILUS_GOBLIN_CORPSE = {
    "typeclass": "typeclasses.objects.Object",
    "key": "goblin corpse",
    "display_name": "|GGoblin corpse|n",
    "aliases": ["corpse"],
    "desc": "His skin, a palette of greens and yellows mottled like the underbelly of a sickly toad, is stretched taut over sharp, protruding bones. His twisted face betrays the final pang of treachery or fear that had seized his heart at the moment of his demise.",
    "locks": "get:pperm(Admin)",
    "prototype_tags": [("nautilus", "zone")],
    "senses": {
        "feel": "The clammy, leathery texture of his skin, cool and unnerving to the touch, feels almost like damp walls of a cave.",
        "smell": "A pungent aroma of decay, mingled with the earthy scent of moss and mold, fills the air.",
        "sound": "Silence pervades, broken only by the occasional drip of water from stalactites, a mournful dirge for the fallen creature.",
        "taste": "The air is thick with the taste of mildew and the metallic tang of blood, a flavor that clings to the back of the throat and refuses to be forgotten.",
    },
}

NAUTILUS_SAILOR_CORPSE = {
    "key": "sailor corpse",
    "display_name": "|CSailor's corpse|n",
    "aliases": ["corpse", "body"],
    "typeclass": "typeclasses.objects.Object",
    "desc": "The sailor's hands, calloused and gnarled from years of wrestling with the ropes that bound his destiny to the sea, lay clasped atop his chest as if in prayer, a silent plea to the celestial guardians he had often gazed upon through the tempestuous nights. His countenance bore the indelible marks of a life spent in ceaseless wanderlust, each line a story, each scar a battle with nature's fury. Yet, amidst the solemn stillness of his eternal rest, a semblance of a grin played upon his lifeless lips, as though recounting tales of camaraderie and adventure that would now be consigned to the depths of oblivion.",
    "locks": "get:pperm(Admin)",
    "prototype_tags": [("nautilus", "zone")],
    "senses": {
        "feel": "The dry, rough texture of his salt-encrusted garments contrasts sharply with the eerie smoothness of his sun-baked skin.",
        "smell": "An overpowering blend of sea brine mingled with the decay of once-vigorous flesh, underlain by the faint, melancholic scent of weathered wood.",
        "sound": "A haunting silence envelops the scene, save for the occasional creak of the weary ship and the soft, mournful whispers of the sea breeze.",
        "taste": "The air carries the harsh tang of salt, reminiscent of the briny depths that claimed his vitality, mingling with the bitter taste of loss and forgotten dreams.",
    },
}

NAUTILUS_CULTIST_CORPSE = {
    "key": "cultist corpse",
    "aliases": ["corpse"],
    "display_name": "|xCultist corpse|n",
    "typeclass": "typeclasses.objects.Object",
    "desc": "The corpse before you is that of a man, his once vibrant flesh now pallid and lifeless, drained of the vital essence that once animated his being. His skin, a sickly grayish-white, clings tightly to the contours of his skeletal frame, as if the very life had been sucked out of him, leaving behind a mere husk of his former self. The face, frozen in an expression of eternal repose, bears the marks of a life lived - deep linned etched into the forehead and around the eyes.",
    "locks": "get:pperm(Admin)",
    "prototype_tags": [("nautilus", "zone")],
    "senses": {
        "feel": "The skin is cold and clammy to the touch, the flesh beneath unyielding, as if all warmth has been leached away by an icy hand.",
        "smell": "The air is heavy with the sickly-sweet odor of decay, a cloying, pervasive scent.",
        "sound": "An eerie silence hangs over the corpse.",
        "taste": "A bitter taste coats the tongue and the back of the throat.",
    },
}

NAUTILUS_ELVISH_CORPSE = {
    "key": "elvish corpse",
    "aliases": ["corpse"],
    "display_name": "|GElvish corpse|n",
    "typeclass": "typeclasses.objects.Object",
    "desc": "In the stillness of eternal repose, a once-vibrant soul now forever stilled by the inexorable hand of death. Her skin, once a rich, warm bbrown that seemed to radiate life itself, now bears the pallor of the grave. Her eyes were once alight with fierce intelligence, but life has abandoned them, their depths forever darkening. Braids frame her face like a crown of midnight. Her features are sharp and angular, but seem softened by the gentle touch of death.",
    "locks": "get:pperm(Admin)",
    "prototype_tags": [("nautilus", "zone")],
    "senses": {
        "feel": "The air around her is heavy.",
        "smell": "The scent of death hangs in the air.",
        "sound": "The silence that surrounds her is a deafening void.",
        "taste": "The bitter taste of loss lingers on the tongue.",
    },
}

PROTOTYPES = [
    NAUTILUS_FIEND,
    NAUTILUS_ENCHANTRESS,
    NAUTILUS_CULTIST,
    NAUTILUS_BEHEMOTH,
    NAUTILUS_COMMANDER,
    NAUTILUS_BROKEN_BODY,
    NAUTILUS_LEFT_LEVER,
    NAUTILUS_RIGHT_LEVER,
    NAUTILUS_EMBERWISP_BLADE,
    NAUTILUS_ASCETIC_ROBES,
    NAUTILUS_WOODEN_CHEST,
    NAUTILUS_GOBLIN_CORPSE,
    NAUTILUS_SAILOR_CORPSE,
]
