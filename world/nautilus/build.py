from prototypes import common_prototypes, currencies, gemstones
from utils.random import randint

from world.nautilus import prototypes
from world.xyzgrid import xyzspawner

z = "nautilus"

mobs = [
    {
        "prototype": prototypes.NAUTILUS_FIEND,
        "room_coords": (1, 3, z),
    },
    {
        "prototype": prototypes.NAUTILUS_FIEND,
        "room_coords": (1, 3, z),
    },
    {
        "prototype": prototypes.NAUTILUS_FIEND,
        "room_coords": (1, 3, z),
    },
    {
        "prototype": prototypes.NAUTILUS_ENCHANTRESS,
        "room_coords": (4, 2, z),
        "equipment": [
            common_prototypes.CIRCLET,
            common_prototypes.CHAIN_SHIRT,
            common_prototypes.LEATHER_BOOTS,
        ],
        "clothing": [
            prototypes.NAUTILUS_ASCETIC_ROBES,
        ],
    },
    {
        "prototype": prototypes.NAUTILUS_BEHEMOTH,
        "room_coords": (3, 2, z),
    },
    {
        "prototype": prototypes.NAUTILUS_COMMANDER,
        "room_coords": (3, 4, z),
        "equipment": [
            prototypes.NAUTILUS_EMBERWISP_BLADE,
            common_prototypes.SCALE_MAIL,
        ],
    },
]

objects = [
    {
        "prototype": prototypes.NAUTILUS_BROKEN_BODY,
        "room_coords": (1, 2, z),
    },
    {
        "prototype": prototypes.NAUTILUS_WOODEN_CHEST,
        "room_coords": (1, 0, z),
        "contents": [
            (currencies.GOLD, {"price": randint(1, 25)}),
            gemstones.ONYX,
        ],
    },
    {
        "prototype": prototypes.NAUTILUS_WOODEN_CHEST,
        "room_coords": (4, 3, z),
        "contents": [(currencies.GOLD, {"price": randint(1, 25)})],
    },
    {
        "prototype": prototypes.NAUTILUS_LEFT_LEVER,
        "room_coords": (4, 2, z),
    },
    {
        "prototype": prototypes.NAUTILUS_RIGHT_LEVER,
        "room_coords": (4, 2, z),
    },
    {
        "prototype": prototypes.NAUTILUS_WOODEN_CHEST,
        "room_coords": (4, 2, z),
        "contents": [(currencies.GOLD, {"price": randint(1, 25)})],
    },
    {
        "prototype": prototypes.NAUTILUS_WOODEN_CHEST,
        "room_coords": (4, 1, z),
        "contents": [(currencies.GOLD, {"price": randint(1, 25)})],
    },
    {
        "prototype": prototypes.NAUTILUS_GOBLIN_CORPSE,
        "room_coords": (2, 2, z),
    },
    {
        "prototype": prototypes.NAUTILUS_SAILOR_CORPSE,
        "room_coords": (2, 1, z),
    },
]

spawns = mobs + objects
xyzspawner.spawn(spawns)
