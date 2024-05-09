from commands.default_cmdsets import MobCmdSet

from .entities import Entity
from .objects import Object


class Mob(Entity, Object):
    _content_types = ("mob",)

    def at_object_creation(self):
        super().at_object_creation()
        self.cmdset.add(MobCmdSet, persistent=True)

    def basetype_setup(self):
        """
        This sets up the default properties of an Object, just before
        the more general at_object_creation.

        You normally don't need to change this unless you change some
        fundamental things like names of permission groups.

        the default security setup fallback for a generic
        object. Overload in child for a custom setup. Also creation
        commands may set this (create an item and you should be its
        controller, for example)
        """

        self.locks.add(
            ";".join(
                [
                    "control:perm(Admin)",  # edit locks/permissions, delete
                    "examine:perm(Admin)",  # examine properties
                    "view:all()",  # look at object (visibility)
                    "edit:pperm(Admin)",  # edit properties/attributes
                    "delete:pperm(Admin)",  # delete object
                    "get:pperm(Admin)",  # pick up object
                    "drop:pperm(Admin)",  # drop only that which you hold
                    "call:false()",  # allow to call commands on this object
                    "tell:all()",  # allow emits to this object
                    "puppet:pperm(Developer)",
                    "teleport:pperm(Admin)",
                    "teleport_here:pperm(Admin)",
                ]
            )
        )  # lock down puppeting only to staff by default
