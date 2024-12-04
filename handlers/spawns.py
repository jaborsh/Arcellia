from abc import ABC, abstractmethod

from django.conf import settings
from evennia.prototypes import spawner
from evennia.prototypes.prototypes import search_objects_with_prototype
from evennia.utils import dbserialize
from evennia.utils.utils import class_from_module, inherits_from, lazy_property

TYPECLASSES = {
    "clothing": settings.BASE_CLOTHING_TYPECLASS,
    "equipment": settings.BASE_EQUIPMENT_TYPECLASS,
    "weapon": settings.BASE_WEAPON_TYPECLASS,
}


class SpawnStrategy(ABC):
    @abstractmethod
    def equip(self, obj, item):
        pass


class ClothingSpawnStrategy(SpawnStrategy):
    def equip(self, obj, item):
        obj.clothing.wear(item)


class EquipmentSpawnStrategy(SpawnStrategy):
    def equip(self, obj, item):
        obj.equipment.wear(item)


class InventorySpawner:
    def __init__(self, owner):
        self.owner = owner
        self.strategies = {
            TYPECLASSES["clothing"]: ClothingSpawnStrategy(),
            TYPECLASSES["equipment"]: EquipmentSpawnStrategy(),
            TYPECLASSES["weapon"]: EquipmentSpawnStrategy(),
        }

    def spawn_or_update(self, prototype):
        existing_objects = [
            obj
            for obj in search_objects_with_prototype(prototype["prototype_key"])
            if obj in self.owner.contents
        ]

        if existing_objects:
            spawner.batch_update_objects_with_prototype(
                prototype, objects=existing_objects, exact=False
            )
            return existing_objects

        prototype.update({"home": self.owner, "location": self.owner})
        new_obj = spawner.spawn(prototype)[0]
        print(new_obj)

        for typeclass, strategy in self.strategies.items():
            if inherits_from(new_obj, class_from_module(typeclass)):
                strategy.equip(self.owner, new_obj)
                break

        return new_obj


class SpawnHandler:
    def __init__(self, obj, db_attribute="spawns", db_category=None):
        self.obj = obj
        self._db_attribute = db_attribute
        self._db_category = db_category
        self.data = {}
        self.inventory_spawner = InventorySpawner(obj)
        self._load()

    def _load(self):
        if data := self.obj.attributes.get(
            self._db_attribute, category=self._db_category
        ):
            self.data = dbserialize.deserialize(data)

    def _save(self):
        self.obj.attributes.add(
            self._db_attribute,
            self.data,
            category=self._db_category,
        )

    @lazy_property
    def appearance(self):
        return self.obj.appearance

    @lazy_property
    def attributes(self):
        return self.obj.attributes

    @lazy_property
    def stats(self):
        return self.obj.stats

    def at_post_spawn(self, prototype=None):
        appearance_attrs = {
            "desc": "desc",
            "display_name": "display_name",
            "senses": "senses",
        }

        for attr, key in appearance_attrs.items():
            if value := self.attributes.get(key):
                setattr(self.appearance, attr, value)
                self.appearance._save()
                self.attributes.remove(key)

        if inventory := self.attributes.get("inventory"):
            for k, v in inventory.items():
                self.data[k] = v.deserialize()
                self.spawn_inventory(v.deserialize())
            self._save()
            self.attributes.remove("inventory")

        if stats := self.attributes.get("stats"):
            for k, v in stats.items():
                if v["trait_type"] in ("counter", "gauge"):
                    self.stats.add(
                        k,
                        k.capitalize(),
                        base=v["base"],
                        min=v["min"],
                        max=v["max"],
                        trait_type=v["trait_type"],
                    )
                else:
                    self.stats.add(
                        k,
                        k.capitalize(),
                        base=v["base"],
                        trait_type=v["trait_type"],
                    )

    def spawn_inventory(self, inventory_data):
        for prototype in inventory_data:
            self.inventory_spawner.spawn_or_update(prototype)
