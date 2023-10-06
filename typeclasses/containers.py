from typeclasses.objects import Object


class Container(Object):
    """
    A container object. Implements a size component.
    """

    @property
    def capacity(self):
        return self.attributes.get("capacity", default=0)

    @capacity.setter
    def capacity(self, value):
        self.attributes.add("capacity", value)

    @property
    def weight(self):
        return self.attributes.get("weight", default=0)

    @weight.setter
    def weight(self, value):
        self.attributes.add("weight", self.weight + value)

    def at_object_creation(self):
        self.locks.add("get_from:true()")
        self.db.capacity = 30
        self.db.weight = 0

    def at_pre_get_from(self, getter, target, **kwargs):
        """
        Called when something attempts to get another object from this object.

        Args:
            getter (Object): The object attempting to get something.
            target (Object): The object being removed.

        Returns:
            boolean: Whether the target should be retrieved or not.
        """
        return True

    def at_pre_put_in(self, putter, target, **kwargs):
        """
        Called when something attempts to put another object inside.

        Args:
            putter (Object): Actor putting something in.
            target (Object): Object being put in.

        Returns:
            boolean: Whether the target should be put in or not.
        """
        if self.capacity < self.weight + target.weight:
            singular, _ = self.get_numbered_name(1, putter)
            putter.msg(f"You can't fit {target.get_display_name()} in {singular}.")
            return False

        return True
