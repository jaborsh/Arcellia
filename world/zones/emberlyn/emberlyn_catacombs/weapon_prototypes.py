SLENDER_SWORD = {
    "prototype_key": "emberlyn_catacomb_slender_sword",
    "key": "sword",
    "typeclass": "typeclasses.equipment.weapons.Weapon",
    "display_name": "Slender sword",
    "desc": "A slender blade of refined elegance, tapering to a razor's edge with a faint, silvery gleam that dances under the dimmest light. The hilt, bound in tarnished leather, is ornamented with faintly embossed filigree, suggesting a history steeped in quiet opulence. Its crossguard arches gracefully, and the pommel bears the faint outline of a lion's head, worn smooth by countless years and countless hands.",
    "senses": {
        "feel": "The sword feels cold and perfectly balanced, with a solidity that hints at a storied past.",
        "smell": "A faint metallic tang lingers, mingling with the musty scent of old leather.",
        "sound": "It hums a soft, metallic note when moved, like a whispered promise of swift justice.",
        "taste": "A faint, bitter taste of iron lingers on the tongue, a reminder of battles past.",
    },
    "attack_desc": "\$You() \$conj(lunge) deftly, \$your() slender blade slipping through the air with a whispering hiss, finding \$you(target).",
    "powers": {"physical": 101},
    "scale": {
        "strength": 12,
        "dexterity": 70,
    },
    "reqs": {
        "strength": 8,
        "dexterity": 11,
    },
    "weight": 3,
}

IRON_SPEAR = {
    "prototype_key": "emberlyn_catacomb_iron_spear",
    "key": "spear",
    "typeclass": "typeclasses.equipment.weapons.Weapon",
    "display_name": "|#6F6050Iron spear|n",
    "desc": "A long spear of solid iron, its shaft slightly tarnished and its point still sharp enough to pierce the bravest of foes. The weapon is unadorned, a simple tool meant solely for function over form.",
    "senses": {
        "feel": "The shaft is firm, with a slight chill, each grip mark worn into it by hands long accustomed to battle.",
        "smell": "A faint smell of oil lingers on the shaft, as though it has been tended to despite its age.",
        "sound": "A soft, steely ring hums faintly when struck, echoing a resonance of lethal intent.",
        "taste": "The taste is of iron, pure and simple, a cold reminder of unyielding resolve.",
    },
    "attack_desc": "\$You() \$conj(thrust) forward, \$your() spear's point cutting through the air towards \$you(target).",
    "powers": {"physical": 114},
    "scale": {
        "strength": 44,
        "dexterity": 33,
    },
    "reqs": {
        "strength": 13,
        "dexterity": 11,
    },
}

ORNAMENTAL_LONGSWORD = {
    "prototype_key": "emberlyn_catacomb_ornamental_longsword",
    "key": "longsword",
    "aliases": ["sword"],
    "typeclass": "typeclasses.equipment.weapons.Weapon",
    "display_name": "|#8A5E3BOrnamental Longsword|n",
    "desc": "The sword is a long, slender blade tarnished by time, with an intricate hilt of faded gold, swirling in patterns long lost to history. The metal bears the marks of ages, worn yet sharp, glinting dully in dim light as if murmuring tales of ancient glories. The guard is unusually ornate, with curving flourishes that lend the sword an air of forgotten regality, while the grip shows the weathered grooves of countless battles.",
    "senses": {
        "feel": "The hilt feels cold and unyielding, with a hint of roughness where the gold has worn away.",
        "smell": "A faint metallic tang, mingled with a musty scent of age and dust, lingers around it.",
        "sound": "When swung, it whistles lowly, a mournful sound as if the air itself remembers the battles long past.",
        "taste": "An acrid bitterness clings to the blade, like the taste of iron and old blood.",
    },
    "attack_desc": "\$You() \$conj(slash) \$you(target) gracefully.",
    "powers": {"physical": 101},
    "scale": {
        "strength": 20,
        "dexterity": 55,
    },
    "reqs": {
        "strength": 10,
        "dexterity": 14,
    },
}
