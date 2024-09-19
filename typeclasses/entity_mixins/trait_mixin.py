from evennia.utils.utils import lazy_property

from handlers import traits


class TraitMixin:
    @lazy_property
    def traits(self):
        return traits.TraitHandler(self, db_attribute_key="traits")

    @property
    def gender(self):
        return self.traits.get("gender")

    @property
    def cls(self):
        return self.traits.get("cls")

    @property
    def race(self):
        return self.traits.get("race")
