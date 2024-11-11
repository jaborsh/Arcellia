from evennia.utils.utils import dedent

from handlers.appearance.appearance import AppearanceHandler

LIVING_APPEARANCE_TEMPLATE = dedent(
    """
    {desc}
    {condition}
    
    {equipment}{clothing}
    """
)

EQUIPMENT_HEADER = "|wEquipment:|n"
CLOTHING_HEADER = "|wClothing:|n"
HIDDEN_SUFFIX = " |x(hidden)|n"

CONDITION_MAP = {
    0: "They are |xlifeless|n.",
    1: "They are |#ff0000barely clinging to life|n.",
    10: "They are |#ff3300critically wounded|n.",
    20: "They are |#ff6600severely injured|n.",
    30: "They are |#ff9933gravely hurt|n.",
    40: "They are |#ffcc00injured|n.",
    50: "They are |#ffff00wounded|n.",
    60: "They are |#ccff00hurt|n.",
    70: "They have |#99ff00some small cuts|n.",
    80: "They are |#66ff00bruised and scraped|n.",
    90: "They are |#33ff00lightly scuffed|n.",
    99: "They have |#1aff00a few scratches|n.",
    100: "They are |#00ff00in perfect condition|n.",
}


class LivingAppearanceHandler(AppearanceHandler):
    def get_display_condition(self, looker, **kwargs):
        percentage = self.obj.health.percent(formatting=None)
        for threshold, display in CONDITION_MAP.items():
            if percentage <= threshold:
                return display
        return "They appear |xunknown|n."

    def _format_worn_items(self, looker, items, header):
        if not items:
            return ""

        max_pos = max(len(item.position) for item in items)
        lines = [header]

        for item in items:
            if getattr(item, "covered_by", None) and looker is not self:
                continue

            pos_display = (
                f"worn {item.position}"
                if header == CLOTHING_HEADER
                else item.position
            )
            spaces = " " * (max_pos - len(pos_display))
            line = f" |x<{pos_display}>|n{spaces} {item.appearance.get_display_name(looker)}"

            if getattr(item, "covered_by", None):
                line += HIDDEN_SUFFIX

            lines.append(line)

        return "\n".join(lines)

    def get_display_equipment(self, looker, **kwargs):
        equipment = self._filter_visible(looker, self.obj.equipment.all())
        result = self._format_worn_items(looker, equipment, EQUIPMENT_HEADER)
        return f"{result}" if result else ""

    def get_display_clothing(self, looker, **kwargs):
        clothing = self._filter_visible(looker, self.obj.clothing.all())
        result = self._format_worn_items(looker, clothing, CLOTHING_HEADER)
        has_equipment = bool(self.obj.equipment.all())
        prefix = "\n\n" if has_equipment else ""
        return f"{prefix}{result}" if result else ""

    def return_appearance(self, looker, **kwargs):
        if not looker:
            return ""

        return LIVING_APPEARANCE_TEMPLATE.format(
            desc=self.get_display_desc(looker, **kwargs),
            condition=self.get_display_condition(looker, **kwargs),
            equipment=self.get_display_equipment(looker, **kwargs),
            clothing=self.get_display_clothing(looker, **kwargs),
        ).strip()
