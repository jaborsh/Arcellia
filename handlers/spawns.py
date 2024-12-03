from evennia.prototypes import spawner
from evennia.prototypes.prototypes import search_objects_with_prototype
from evennia.utils import dbserialize
from evennia.utils.utils import lazy_property


class SpawnHandler:
    def __init__(self, obj, db_attribute="spawns", db_category=None):
        self.obj = obj
        self._db_attribute = db_attribute
        self._db_category = db_category
        self.clothing = []
        self._load()

    def _load(self):
        if data := self.obj.attributes.get(
            self._db_attribute, category=self._db_category
        ):
            data = dbserialize.deserialize(data)
            self.clothing = data.get("clothing", [])

    def _save(self):
        self.obj.attributes.add(
            self._db_attribute,
            {
                "clothing": self.clothing,
            },
            category=self._db_category,
        )

    @lazy_property
    def appearance(self):
        return self.obj.appearance

    @lazy_property
    def attributes(self):
        return self.obj.attributes

    def at_post_spawn(self, prototype=None):
        if self.attributes.get("senses"):
            self.appearance.senses = self.attributes.get("senses")
            self.appearance._save()
            self.attributes.remove("senses")
        if self.attributes.get("spawns"):
            spawns = self.attributes.get("spawns")
            self.spawn_clothing(spawns.get("clothing", []))
            self._save()
            self.attributes.remove("spawns")
        if self.attributes.get("stories"):
            self.attributes.add("stories", self.attributes.get("stories"))

    def spawn_clothing(self, clothing):
        for clothing_prototype in clothing:
            all_matching = search_objects_with_prototype(
                clothing_prototype["prototype_key"]
            )
            matching_clothes = [
                obj for obj in all_matching if obj in self.obj.contents
            ]

            if matching_clothes:
                spawner.batch_update_objects_with_prototype(
                    clothing_prototype.deserialize(),
                    objects=matching_clothes,
                    exact=False,
                )
            else:
                clothing_prototype["home"] = self.obj
                clothing_prototype["location"] = self.obj
                article = spawner.spawn(clothing_prototype)[0]
                self.obj.clothing.wear(article)
