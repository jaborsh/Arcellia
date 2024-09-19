from evennia.utils.utils import lazy_property

from handlers import clothing


class ClothingMixin:
    @lazy_property
    def clothing(self):
        return clothing.ClothingHandler(self, db_attribute_key="clothing")
