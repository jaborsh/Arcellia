from world.zones.emberlyn.emberlyn_catacombs import (
    clothing_prototypes,
    weapon_prototypes,
)

WANDERING_UNDEAD = {
    "prototype_parent": "xyz_mob",
    "prototype_key": "emberlyn_beach_veiled_woman",
    "typeclass": "world.xyzgrid.xyzmob.XYZMob",
    "locks": "attack:false()",
    "key": "undead",
    "display_name": "|#7D7D7DWandering Undead|n",
    "desc": "A haggard figure bent low under the invisible burden of ages past, its flesh stretched thin over jutting bones, creating an unholy gauntness that speaks of long-withered life. Its face bears a pitiful expression of forgotten sorrows, its hollow eyes alight with an unnatural glow that flickers like embers threatening to extinguish. Each slow step it takes is marked by a halting, almost pained motion, as if the very ground resists the cursed weight of its presence.",
    "senses": {
        "feel": "A chill of ancient, marrow-deep cold hangs in the air, prickling the skin like needles of forgotten frost.",
        "smell": "The faint stench of damp earth mingles with the acrid tang of long-decayed flesh, lingering in the air like a macabre perfume.",
        "sound": "A soft scraping echoes with each step, accompanied by the brittle clatter of bone, barely louder than a whisper.",
        "taste": "A taste of stale, dry air tinged with the faint bitterness of rot touches the tongue, lingering unpleasantly.",
    },
    "spawn": {
        "clothing": [
            clothing_prototypes.TATTERED_ROBE,
            clothing_prototypes.WEATHERED_LEATHER_BOOTS,
        ],
        "stats": {
            "health": {"base": 85, "min": 0, "max": 85, "trait_type": "gauge"}
        },
        "weapons": [weapon_prototypes.SLENDER_SWORD],
    },
}

WEATHERED_SOLDIER = {
    "prototype_parent": "xyz_mob",
    "prototype_key": "emberlyn_beach_weathered_soldier",
    "typeclass": "world.xyzgrid.xyzmob.XYZMob",
    "key": "soldier",
    "display_name": "|#726E5AWeathered Soldier|n",
    "desc": "A figure of solemn demeanor and timeworn vigor, the undead soldier stands encased in layers of tarnished metal that cling to him like the remnants of an ancient oath. His frame is broad yet weathered, as though both shield and sinew have borne the bite of countless battles. His face, nearly obscured beneath a battered helm, is lined and stern; a silent witness to decades of vigilance in the deep and desolate places of the world. A thin layer of dust clings to his armor, dimming its once-bright sheen, while faint scars mar the exposed edges of his skin, as if his very flesh has been cut and recast by time itself.",
    "senses": {
        "feel": "The air around him is dense with a chill, as if his armor itself emits a cold and silent endurance.",
        "smell": "There lingers a faint odor of damp stone and rusted metal, mingling with the sharper tang of old leather.",
        "sound": "A muted creak echoes as he shifts, the strained groan of ancient metal joints that refuse to break.",
        "taste": "The air tastes of cold iron and grit, as though touched by the lingering spirit of his countless battles.",
    },
    "spawn": {
        "clothing": [clothing_prototypes.FRAYED_GREEN_CAPE],
        "equipment": [],
        "stats": {
            "health": {"base": 192, "min": 0, "max": 192, "trait_type": "gauge"}
        },
        "weapons": [weapon_prototypes.IRON_SPEAR],
    },
}


EMBERLYN_CATACOMB_MOBS = {
    (4, 3): [WANDERING_UNDEAD],
    (4, 4): [WANDERING_UNDEAD],
    (4, 5): [WANDERING_UNDEAD, WANDERING_UNDEAD],
    (4, 7): [WEATHERED_SOLDIER],
    (3, 7): [WANDERING_UNDEAD, WANDERING_UNDEAD],
    (2, 7): [WEATHERED_SOLDIER],
    (1, 7): [WANDERING_UNDEAD],
    (0, 7): [WANDERING_UNDEAD, WANDERING_UNDEAD],
    (0, 6): [WANDERING_UNDEAD],
    (0, 4): [WEATHERED_SOLDIER],  # boss
}
