from evennia.prototypes import spawner
from world.xyzgrid.xyzroom import XYZRoom


def spawn(spawns=None):
    for spawn_data in spawns:
        spawn_entity(
            spawn_data["prototype"],
            spawn_data["room_coords"],
            clothing=spawn_data.get("clothing", None),
            contents=spawn_data.get("contents", None),
            equipment=spawn_data.get("equipment", None),
        )


def spawn_entity(proto, room_coords, clothing=None, contents=None, equipment=None):
    entity = spawner.spawn(proto)[0]
    entity_room = XYZRoom.objects.get_xyz(room_coords)
    entity.location = entity_room
    entity.home = entity_room

    if contents:
        for content in contents:
            if isinstance(content, tuple):
                content_proto = spawner.spawn(content[0])[0]
                for key, value in content[1].items():
                    content_proto.attributes.add(key, value)
            else:
                content_proto = spawner.spawn(content)[0]

            content_proto.location = entity
            content_proto.home = entity

    if clothing:
        for article in clothing:
            item = spawner.spawn(article)[0]
            item.location = entity
            item.home = entity
            entity.clothing.wear(item)

    if equipment:
        for equip in equipment:
            item = spawner.spawn(equip)[0]
            item.location = entity
            item.home = entity
            entity.equipment.wear(item)
