from world.zones.nautilus.prototypes import PROTOTYPES

from evennia.prototypes import spawner

for prototype in PROTOTYPES:
    objs = spawner.batch_update_objects_with_prototype(prototype)
