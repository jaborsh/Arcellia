from world.zones.emberlyn.emberlyn_catacombs import (
    clothing_prototypes,
    weapon_prototypes,
)

WANDERING_UNDEAD = {
    "prototype_parent": "xyz_mob",
    "prototype_key": "emberlyn_undead_wanderer",
    "typeclass": "world.xyzgrid.xyzmob.XYZMob",
    "key": "undead",
    "aliases": ["wanderer"],
    "display_name": "|#7D7D7DUndead Wanderer|n",
    "desc": "A haggard figure bent low under the invisible burden of ages past, its flesh stretched thin over jutting bones, creating an unholy gauntness that speaks of long-withered life. Its face bears a pitiful expression of forgotten sorrows, its hollow eyes alight with an unnatural glow that flickers like embers threatening to extinguish. Each slow step it takes is marked by a halting, almost pained motion, as if the very ground resists the cursed weight of its presence.",
    "senses": {
        "feel": "A chill of ancient, marrow-deep cold hangs in the air, prickling the skin like needles of forgotten frost.",
        "smell": "The faint stench of damp earth mingles with the acrid tang of long-decayed flesh, lingering in the air like a macabre perfume.",
        "sound": "A soft scraping echoes with each step, accompanied by the brittle clatter of bone, barely louder than a whisper.",
        "taste": "A taste of stale, dry air tinged with the faint bitterness of rot touches the tongue, lingering unpleasantly.",
    },
    "inventory": {
        "clothing": [
            clothing_prototypes.TATTERED_ROBE,
            clothing_prototypes.WEATHERED_LEATHER_BOOTS,
        ],
        "weapons": [weapon_prototypes.SLENDER_SWORD],
    },
    "stats": {
        "health": {"base": 96, "min": 0, "max": 96, "trait_type": "gauge"},
        "experience": {"base": 11, "trait_type": "static"},
    },
}

UNDEAD_SOLDIER = {
    "prototype_parent": "xyz_mob",
    "prototype_key": "emberlyn_catacomb_undead_soldier",
    "typeclass": "world.xyzgrid.xyzmob.XYZMob",
    "key": "soldier",
    "aliases": ["undead"],
    "display_name": "|#726E5AUndead Soldier|n",
    "desc": "A figure of solemn demeanor and timeworn vigor, the undead soldier stands encased in layers of tarnished metal that cling to him like the remnants of an ancient oath. His frame is broad yet weathered, as though both shield and sinew have borne the bite of countless battles. His face, nearly obscured beneath a battered helm, is lined and stern; a silent witness to decades of vigilance in the deep and desolate places of the world. A thin layer of dust clings to his armor, dimming its once-bright sheen, while faint scars mar the exposed edges of his skin, as if his very flesh has been cut and recast by time itself.",
    "senses": {
        "feel": "The air around him is dense with a chill, as if his armor itself emits a cold and silent endurance.",
        "smell": "There lingers a faint odor of damp stone and rusted metal, mingling with the sharper tang of old leather.",
        "sound": "A muted creak echoes as he shifts, the strained groan of ancient metal joints that refuse to break.",
        "taste": "The air tastes of cold iron and grit, as though touched by the lingering spirit of his countless battles.",
    },
    "inventory": {
        "clothing": [clothing_prototypes.FRAYED_GREEN_CAPE],
        "weapons": [weapon_prototypes.IRON_SPEAR],
    },
    "stats": {
        "health": {"base": 192, "min": 0, "max": 192, "trait_type": "gauge"},
        "experience": {"base": 38, "trait_type": "static"},
    },
}

UNDEAD_SOLDIER_BOSS = {
    "prototype_parent": "xyz_mob",
    "prototype_key": "emberlyn_catacomb_undead_soldier_boss",
    "typeclass": "world.xyzgrid.xyzmob.XYZMob",
    "key": "soldier",
    "aliases": ["undead"],
    "display_name": "|#8B4F2AUndead Soldier of Emberlyn|n",
    "desc": "This soldier stands as a stout bulwark of faded grandeur, his face partially hidden beneath the shadow of a dented helm and the rough lineaments of hard-fought campaigns. His expression is stern, with a jaw that seems chiseled from stone, lips pressed in a grim line beneath his visor. His eyes peer forth with an unyielding gaze, a hint of weary resolve lingering in their depths. Upon his armor rests a faded crest, a lion rampant emblazoned upon a field split by age-worn green and orange cloth. Though the colors are dull, the soldier's stance exudes a fierce loyalty, as if he is the last bastion of a once-proud order.",
    "senses": {
        "feel": "The air around him bears a quiet, heavy presence, as though he is accompanied by the unseen weight of ancient vows.",
        "smell": "A faint odor of sweat, iron, and old leather lingers around him, the scent of a soldier long accustomed to the rigors of duty.",
        "sound": "The soft clink of metal accompanies his every movement, a rhythm like a dirge from an ancient, forgotten battlefield.",
        "taste": "The air holds a bitter tang, the taste of steel and leather mingling with a hint of dust from the past.",
    },
    "inventory": {
        "clothing": [clothing_prototypes.HERALDIC_TABARD],
        "weapons": [weapon_prototypes.ORNAMENTAL_LONGSWORD],
    },
    "stats": {
        "health": {"base": 384, "min": 0, "max": 394, "trait_type": "gauge"},
        "experience": {"base": 400, "trait_type": "static"},
    },
}


EMBERLYN_CATACOMB_MOBS = {
    (4, 3): [WANDERING_UNDEAD],
    (4, 4): [WANDERING_UNDEAD],
    (4, 5): [WANDERING_UNDEAD, WANDERING_UNDEAD],
    (4, 7): [UNDEAD_SOLDIER],
    (3, 7): [WANDERING_UNDEAD, WANDERING_UNDEAD],
    (2, 7): [UNDEAD_SOLDIER],
    (1, 7): [WANDERING_UNDEAD],
    (0, 7): [WANDERING_UNDEAD, WANDERING_UNDEAD],
    (0, 6): [WANDERING_UNDEAD],
    (0, 4): [UNDEAD_SOLDIER_BOSS],  # boss
}
