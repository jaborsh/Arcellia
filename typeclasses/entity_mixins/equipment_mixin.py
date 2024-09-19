from evennia.utils.utils import lazy_property

from handlers import equipment


class EquipmentMixin:
    @lazy_property
    def equipment(self):
        return equipment.EquipmentHandler(
            self,
            db_attribute_key="equipment",
        )
