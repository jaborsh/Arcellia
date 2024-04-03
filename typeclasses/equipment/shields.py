from .equipment import Equipment, EquipmentType


class Shield(Equipment):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.equipment_type = EquipmentType.SHIELD
