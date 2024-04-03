from evennia.prototypes import spawner

from world import common_prototypes
from world.nautilus import prototypes
from world.xyzgrid.xyzroom import XYZRoom

z = "nautilus"

mobs = [
    {
        "prototype": prototypes.NAUTILUS_FIEND,
        "room_coords": (1, 3),
    },
    {
        "prototype": prototypes.NAUTILUS_FIEND,
        "room_coords": (1, 3),
    },
    {
        "prototype": prototypes.NAUTILUS_FIEND,
        "room_coords": (1, 3),
    },
    {
        "prototype": prototypes.NAUTILUS_ENCHANTRESS,
        "room_coords": (4, 2),
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
        "room_coords": (3, 2),
    },
    {
        "prototype": prototypes.NAUTILUS_COMMANDER,
        "room_coords": (3, 4),
        "equipment": [
            prototypes.NAUTILUS_EMBERWISP_BLADE,
            common_prototypes.SCALE_MAIL,
        ],
    },
]

objects = [
    {
        "prototype": prototypes.NAUTILUS_CULTIST_CORPSE,
        "room_coords": (0, 1),
    },
    {
        "prototype": prototypes.NAUTILUS_BROKEN_BODY,
        "room_coords": (1, 2),
    },
    {
        "prototype": prototypes.NAUTILUS_WOODEN_CHEST,
        "room_coords": (1, 0),
    },
    {
        "prototype": prototypes.NAUTILUS_WOODEN_CHEST,
        "room_coords": (4, 3),
    },
    {
        "prototype": prototypes.NAUTILUS_LEFT_LEVER,
        "room_coords": (4, 2),
    },
    {
        "prototype": prototypes.NAUTILUS_RIGHT_LEVER,
        "room_coords": (4, 2),
    },
    {
        "prototype": prototypes.NAUTILUS_CULTIST_CORPSE,
        "room_coords": (4, 2),
    },
    {
        "prototype": prototypes.NAUTILUS_ELVISH_CORPSE,
        "room_coords": (4, 2),
    },
    {
        "prototype": prototypes.NAUTILUS_WOODEN_CHEST,
        "room_coords": (4, 2),
    },
    {
        "prototype": prototypes.NAUTILUS_WOODEN_CHEST,
        "room_coords": (4, 1),
    },
    {
        "prototype": prototypes.NAUTILUS_GOBLIN_CORPSE,
        "room_coords": (2, 2),
    },
    {
        "prototype": prototypes.NAUTILUS_SAILOR_CORPSE,
        "room_coords": (2, 1),
    },
]


def spawn_and_equip(proto, room_coords, equipment=None, clothing=None):
    mob = spawner.spawn(proto)[0]
    mob_room = XYZRoom.objects.get_xyz((*room_coords, z))
    mob.location = mob_room
    mob.home = mob_room

    if equipment:
        for equip in equipment:
            item = spawner.spawn(equip)[0]
            item.location = mob
            item.home = mob
            mob.equipment.wear(item)

    if clothing:
        for article in clothing:
            item = spawner.spawn(article)[0]
            item.location = mob
            item.home = mob
            mob.clothing.wear(item)


def spawn_and_fill(proto, room_coords, contents=None):
    item = spawner.spawn(proto)[0]
    item_room = XYZRoom.objects.get_xyz((*room_coords, z))
    item.location = item_room
    item.home = item_room

    if contents:
        for content in contents:
            content_item = spawner.spawn(content)[0]
            content_item.location = item
            content_item.home = item


for mob_data in mobs:
    spawn_and_equip(
        mob_data["prototype"],
        mob_data["room_coords"],
        mob_data.get("equipment", None),
        mob_data.get("clothing", None),
    )

for obj_data in objects:
    spawn_and_fill(
        obj_data["prototype"], obj_data["room_coords"], obj_data.get("contents", None)
    )
