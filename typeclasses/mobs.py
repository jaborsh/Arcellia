from commands.default_cmdsets import MobCmdSet
from typeclasses.objects import Object


class Mob(Object):
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
        super().basetype_setup()
        self.locks.add(
            ";".join(
                [
                    "attack:true()",
                    "get:pperm(Admin)",
                    "puppet:pperm(Admin)",
                ]
            )
        )  # lock down puppeting only to staff by default

    def at_die(self):
        self.location.msg_contents("$You() $conj(die)!", from_obj=self)
        for char in self.location.contents_get(content_type="character"):
            char.experience.current += self.experience.current
            char.msg(f"You gain {self.experience.current} experience.")

        for item in self.contents:
            item.move_to(self.location, quiet=True)
        self.clothing.reset()
        self.equipment.reset()
        self.locks.add("view:pperm(Admin)")

    def at_restore(self):
        super().at_restore()
        self.locks.add("view:true()")

    def get_numbered_name(self, count, looker=None, **kwargs):
        return self.appearance.get_numbered_name(
            count, looker, no_article=True, **kwargs
        )
