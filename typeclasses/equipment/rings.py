from .equipment import Equipment, EquipmentType


class Ring(Equipment):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.equipment_type = EquipmentType.RING
