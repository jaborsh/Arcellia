from prototypes.consumables import potions
from prototypes.miscellaneous import currency, gems

GOLD = currency.GOLD
GOLD["price"] = 25

SAILOR_CORPSE = {
    "key": "corpse",
    "display_name": "|CSailor's Corpse|n",
    "typeclass": "typeclasses.containers.ImmovableContainer",
    "desc": "The sailor's hands, calloused and gnarled from years of wrestling with the ropes that bound his destiny to the sea, lay clasped atop his chest as if in prayer, a silent plea to the celestial guardians he had often gazed upon through the tempestuous nights. His countenance bore the indelible marks of a life spent in ceaseless wanderlust, each line a story, each scar a battle with nature's fury. Yet, amidst the solemn stillness of his eternal rest, a semblance of a grin played upon his lifeless lips, as though recounting tales of camaraderie and adventure that would now be consigned to the depths of oblivion.",
    "senses": {
        "feel": "The dry, rough texture of his salt-encrusted garments contrasts sharply with the eerie smoothness of his sun-baked skin.",
        "smell": "An overpowering blend of sea brine mingled with the decay of once-vigorous flesh, underlain by the faint, melancholic scent of weathered wood.",
        "sound": "A haunting silence envelops the scene, save for the occasional creak of the weary ship and the soft, mournful whispers of the sea breeze.",
        "taste": "The air carries the harsh tang of salt, reminiscent of the briny depths that claimed his vitality, mingling with the bitter taste of loss and forgotten dreams.",
    },
    "spawns": [potions.HEALING_POTION],
    "weight": 100,
}

GOBLIN_CORPSE = {
    "key": "corpse",
    "display_name": "|GGoblin's Corpse|n",
    "typeclass": "typeclasses.containers.ImmovableContainer",
    "desc": "His skin, a palette of greens and yellows mottled like the underbelly of a sickly toad, was stretched taut over sharp, protruding bones. His face, twisted in an eternal grimace, betrayed the final pang of treachery or fear that had seized his heart at the moment of his demise.",
    "senses": {
        "feel": "The clammy, leathery texture of his skin, cool and unnerving to the touch, feels almost like damp walls of a cave.",
        "smell": "A pungent aroma of decay, mingled with the earthy scent of moss and mold, fills the air.",
        "sound": "Silence pervades, broken only by the occasional drip of water from stalactites, a mournful dirge for the fallen creature.",
        "taste": "The air is thick with the taste of mildew and the metallic tang of blood, a flavor that clings to the back of the throat and refuses to be forgotten.",
    },
    "spawns": [GOLD],
}

WOODEN_CHEST = {
    "key": "chest",
    "display_name": "|YWooden Chest|n",
    "typeclass": "typeclasses.containers.ImmovableContainer",
    "desc": "Crafted from the heartwood of ancient trees, the chest's exterior is sheathed in grain patterns that swirl and weave across its surface like tales told in timber. The chest's sturdy form invites touch, the solid wood yielding ever so slightly to the caress of a curious hand. Stout, hand-carved legs support it, resembling the strong limbs of the very trees from whence it came. Its lid, hinged gracefully, appears to beckon one to witness the secrets nested within its hollow.",
    "senses": {
        "feel": "The chest's surface carries the subtle roughness of grain.",
        "smell": "It exudes a wholesome aroma of wood and resin, reminiscent of a forest at dawn.",
        "sound": "A soft creak accompanies the lifting of the lid.",
        "taste": "The air around it is laced with the faint, tannic flavor of bark and the earthiness of fallen leaves.",
    },
    "spawns": [gems.ONYX, GOLD],
    "weight": 40,
}

WOODEN_CHEST_2 = WOODEN_CHEST.copy()
WOODEN_CHEST_2["spawns"] = [potions.HEALING_POTION, potions.HEALING_POTION]
