from typeclasses import objects


class Mob(objects.Object):
    """
    This Mobile defaults to reimplementing some of the base Object's hook
    methods with the following functionality:
    """

    _content_types = ("mob",)

    def basetype_setup(self):
        """
        This sets up the default properties of an Object, just before
        the more general at_object_creation.

        You normally don't need to change this unless you change some
        fundamental things like names of permission groups.

        """
        # the default security setup fallback for a generic
        # object. Overload in child for a custom setup. Also creation
        # commands may set this (create an item and you should be its
        # controller, for example)

        self.locks.add(
            ";".join(
                [
                    "control:perm(Admin)",  # edit locks/permissions, delete
                    "examine:perm(Builder)",  # examine properties
                    "view:all()",  # look at object (visibility)
                    "edit:perm(Admin)",  # edit properties/attributes
                    "delete:perm(Admin)",  # delete object
                    "get:superuser()",  # pick up object
                    "drop:superuser()",  # drop only that which you hold
                    "call:false()",  # allow to call commands on this object
                    "tell:perm(Admin)",  # allow emits to this object
                    "puppet:pperm(Developer)",
                    "teleport:perm(Admin)",
                    "teleport_here:perm(Admin)",
                ]
            )
        )  # lock down puppeting only to staff by default
