from evennia.prototypes import spawner
from evennia.prototypes.prototypes import search_objects_with_prototype

OTHER_THING = {
    "prototype_key": "other_thing",
    "key": "other thing",
    "a": ["b", "c", "d"],
}
OTHER_UPDATE = {
    "prototype_key": "other_thing",
    "key": "other update",
    "a": ["b", "c", "d", "e"],
}
SPECIAL_THING = {"key": "special_thing", "spawn": [OTHER_THING]}


def test_spawn():
    obj = spawner.spawn(SPECIAL_THING)[0]
    obj2 = spawner.spawn(SPECIAL_THING["spawn"][0])[0]
    print(obj2.db.a)

    for prot in [OTHER_UPDATE]:
        obj2 = search_objects_with_prototype(OTHER_UPDATE["prototype_key"])[0]
        spawner.batch_update_objects_with_prototype(
            prot, objects=[obj2], exact=False
        )
        print(obj2.db.a)
