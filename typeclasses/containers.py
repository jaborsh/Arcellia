from collections import defaultdict

from typeclasses.objects import Object


class Container(Object):
    """
    A container object. Implements a size component.
    """

    appearance_template = """
{desc}
{contains}
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
        self.db.description = "A generic container."
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

    def get_display_desc(self, looker, **kwargs):
        """
        Get the 'desc' component of the object description.

        Args:
            looker (Object): Object doing the looking.
            **kwargs: Arbitrary data for overriding.

        Returns:
            str: The description display string.
        """
        return self.db.desc or ""

    def get_display_things(self, looker, **kwargs):
        """
        Get the 'things' component of the object description. Called by `return_appearance`.

        Args:
            looker (Object): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.

        Returns:
            str: The things display data.
        """

        def _filter_visible(obj_list):
            return (
                obj for obj in obj_list if obj != looker and obj.access(looker, "view")
            )

        things = _filter_visible(self.contents_get(content_type="object"))

        grouped_things = defaultdict(list)
        for thing in things:
            grouped_things[thing.get_display_name(looker, **kwargs)].append(thing)

        thing_names = []
        for thingname, thinglist in sorted(grouped_things.items()):
            nthings = len(thinglist)
            thing = thinglist[0]
            singular, plural = thing.get_numbered_name(nthings, looker, key=thingname)
            thing_names.append(" " + singular if nthings == 1 else " " + plural)
        return "\n".join(thing_names)

    def return_appearance(self, looker, **kwargs):
        if not looker:
            return ""

        return self.format_appearance(
            self.appearance_template.format(
                desc=self.get_display_desc(looker, **kwargs),
                contains="\n"
                + self.get_display_name(looker, **kwargs)
                + " contains:\n"
                + self.get_display_things(looker, **kwargs)
                if self.contents
                else "",
            ),
            looker,
            **kwargs,
        )


class ImmovableContainer(Container):
    """
    A copy of Container that cannot be moved.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.locks.add("get:false()")
