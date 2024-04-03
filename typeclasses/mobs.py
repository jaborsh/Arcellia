from commands.default_cmdsets import MobCmdSet

from .mixins.living import LivingMixin
from .objects import Object


class Mob(LivingMixin, Object):
    _content_types = ("mob",)

    def at_object_creation(self):
        self.cmdset.add(MobCmdSet, persistent=True)

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
                    "examine:perm(Admin)",  # examine properties
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
