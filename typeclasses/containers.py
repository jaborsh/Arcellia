from collections import defaultdict

from typeclasses.items import Item


class Container(Item):
    """
    A container object. Implements a size component.
    """

    appearance_template = """
{desc}
{contains}
    """

    def at_object_creation(self):
        self.locks.add("get_from:true()")

    def at_post_spawn(self):
        super().at_post_spawn()
        capacity = self.attributes.get("capacity", 9999)
        self.traits.add(
            "capacity",
            "Capacity",
            trait_type="counter",
            base=0,
            min=0,
            max=capacity,
        )
        self.attributes.remove("capacity")

    @property
    def capacity(self):
        return self.traits.get("capacity")

    def at_pre_get_from(self, getter, target, **kwargs):
        """
        Called when something attempts to get another object from this object.

        Args:
            getter (Object): The object attempting to get something.
            target (Object): The object being removed.

        Returns:
            boolean: Whether the target should be retrieved or not.
        """
        self.capacity.base -= target.weight.value

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
        if self.capacity.value + target.weight.value > self.capacity.max:
            putter.msg("It won't fit.")
            return False

        self.capacity.base += target.weight.value

        return True

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
