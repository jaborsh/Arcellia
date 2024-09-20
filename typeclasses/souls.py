from evennia.utils.utils import lazy_property

from handlers import traits
from typeclasses.objects import Object


class Soul(Object):
    def at_object_creation(self):
        self.traits.add("experience", "Experience", trait_type="static", base=0)
        self.traits.add("owner", "Owner", trait_type="trait", value=None)

    @property
    def display_name(self):
        if self.owner.value.display_name.endswith("s"):
            possession = "'"
        else:
            possession = "'s"
        return self.owner.value.display_name + f"{possession} " + self.key

    @lazy_property
    def traits(self):
        return traits.TraitHandler(self, db_attribute_key="traits")

    @property
    def experience(self):
        return self.traits.get("experience")

    @property
    def owner(self):
        return self.traits.get("owner")

    def at_pre_get(self, getter, **kwargs):
        getter.experience.current += self.experience.current
        self.owner.value.location.msg_contents(
            "|C$You(getter) $conj(absorb) your soul!|n",
            exclude=[
                c
                for c in self.owner.value.location.contents
                if c != self.owner.value
            ],
            mapping={"getter": getter},
        )
        getter.location.msg_contents(
            "|C$You() $conj(absorb) $you(soul)!|n",
            from_obj=getter,
            mapping={"owner": self.owner.value, "soul": self},
            exclude=[self.owner.value],
        )

        self.delete()  # Soul is consumed when retrieved

        return False  # Prevent default get behavior
