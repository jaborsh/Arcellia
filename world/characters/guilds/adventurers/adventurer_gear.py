STARTING_BATTLE_AXE = {
    "key": "battle axe",
    "aliases": ["axe"],
    "display_name": "Battle axe",
    "typeclass": "typeclasses.equipment.weapons.Weapon",
    "desc": (
        "The blade curves outward in a wicked arc, its edge honed to a gleam that "
        "hungers for the bite of flesh and bone. The metal bears the scars of its "
        "forging. At its apex, the axe flares into a vicious point."
    ),
    "senses": {
        "feel": "The haft sits heavy and unyielding in the hand.",
        "smell": (
            "A faint metallic odor mingles with the earthy scent of oiled leather and "
            "aged wood."
        ),
        "sound": "When swung, the axe cleaves the air with a menacing whistle.",
        "taste": "You taste nothing interesting.",
    },
    "attack_desc": "\$You() \$conj(cleave) \$you(target) with a fierce arc of \$pron(your,pa) battle axe.",
    "powers": {"physical": 112},
    "scale": {
        "strength": 48,
        "dexterity": 33,
    },
    "reqs": {
        "strength": 12,
        "dexterity": 8,
    },
    "weight": 4,
}
