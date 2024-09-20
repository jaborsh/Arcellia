from evennia.utils.utils import lazy_property

from handlers import cooldowns


class CooldownMixin:
    @lazy_property
    def cooldowns(self):
        return cooldowns.CooldownHandler(self, db_attribute_key="feats")
