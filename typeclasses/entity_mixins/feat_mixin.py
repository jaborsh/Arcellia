from evennia.utils.utils import lazy_property

from handlers import buffs


class FeatMixin:
    @lazy_property
    def feats(self):
        return buffs.BuffHandler(self, db_attribute_key="feats")
