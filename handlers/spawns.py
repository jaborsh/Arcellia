from evennia.prototypes import spawner
from evennia.prototypes.prototypes import search_objects_with_prototype
from evennia.utils import dbserialize
from evennia.utils.utils import lazy_property


class SpawnHandler:
    def __init__(self, obj, db_attribute="spawns", db_category=None):
        self.obj = obj
        self._db_attribute = db_attribute
        self._db_category = db_category
        self.data = {}
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

    def at_post_spawn(self, prototype=None):
        """Handle post-spawn operations like inventory and senses."""

        # Handle inventory spawning
        if inventory := self.attributes.get("inventory"):
            self.data = inventory
            self.spawn_inventory(inventory.deserialize())
            self._save()
            self.attributes.remove("inventory")

        # Handle senses
        if senses := self.attributes.get("senses"):
            self.appearance.senses = senses
            self.appearance._save()
            self.attributes.remove("senses")

    def spawn_inventory(self, inventory_data):
        """
        Spawn or update inventory items.

        Args:
            inventory_data (dict): Dictionary containing inventory information
        """
        for prototype in (
            inventory_data.get("clothing", [])
            + inventory_data.get("equipment", [])
            + inventory_data.get("objects", [])
            + inventory_data.get("weapons", [])
        ):
            # Check for existing matching objects
            existing_objects = [
                obj
                for obj in search_objects_with_prototype(
                    prototype["prototype_key"]
                )
                if obj in self.obj.contents
            ]

            if existing_objects:
                # Update existing objects
                spawner.batch_update_objects_with_prototype(
                    prototype,
                    objects=existing_objects,
                    exact=False,
                )
            else:
                from typeclasses.clothing import Clothing
                from typeclasses.equipment.equipment import Equipment
                from typeclasses.equipment.weapons import Weapon

                # Spawn new object
                prototype.update({"home": self.obj, "location": self.obj})
                new_obj = spawner.spawn(prototype)[0]

                # Handle equipping
                if isinstance(new_obj, Clothing):
                    self.obj.clothing.wear(new_obj)
                elif isinstance(new_obj, (Equipment, Weapon)):
                    self.obj.equipment.wear(new_obj)
