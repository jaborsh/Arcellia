from evennia.utils.utils import lazy_property

from typeclasses.objects import Object


class Book(Object):
    @lazy_property
    def story(self):
        return self.attributes.get("story", "There is nothing written here.")

    def at_read(self, reader):
        reader.msg(self.story)
