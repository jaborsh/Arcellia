import random

from evennia.utils.utils import lazy_property

from typeclasses.objects import Object


class Book(Object):
    @lazy_property
    def stories(self):
        return self.attributes.get("stories", [])

    def at_read(self, reader):
        if not self.stories:
            return reader.msg("The book is empty.")

        if len(self.stories) == 1:
            return reader.msg(self.stories[0])

        reader.msg(random.choice(self.stories))

    def get_numbered_name(self, count, looker=None, **kwargs):
        return self.appearance.get_numbered_name(
            count, looker, no_article=True, **kwargs
        )
