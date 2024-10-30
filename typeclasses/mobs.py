from commands.default_cmdsets import MobCmdSet

from .entities import Entity
from .objects import Object


class Mob(Entity, Object):
    _content_types = ("mob",)

    def at_object_creation(self):
        super().at_object_creation()
        self.cmdset.add(MobCmdSet, persistent=True)

        lockstring = "attack:true()"
        self.locks.add(lockstring)

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
        super().basetype_setup()
        self.locks.add(
            ";".join(
                [
                    "get:pperm(Admin)",
                    "puppet:pperm(Admin)",
                ]
            )
        )  # lock down puppeting only to staff by default
