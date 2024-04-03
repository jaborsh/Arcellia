from evennia.prototypes import spawner

from world.nautilus.prototypes import PROTOTYPES

for prototype in PROTOTYPES:
    spawner.batch_update_objects_with_prototype(prototype)
