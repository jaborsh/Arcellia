from .equipment import Equipment, EquipmentType


class Footwear(Equipment):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.equipment_type = EquipmentType.FOOTWEAR
