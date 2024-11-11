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
    """Handles the appearance and visual representation of living entities in the game.

    This handler manages how living entities (characters, NPCs, etc.) appear to others,
    implementing a comprehensive appearance system that includes:

    * Basic physical description
    * Dynamic health condition display with color-coded messages
    * Equipment display with positioning information
    * Clothing system with layering and visibility rules

    The handler uses a template-based approach to format the final appearance,
    combining all elements into a cohesive description. It respects visibility
    rules where certain items may be hidden by others or not visible to certain
    observers.

    Attributes:
        obj (Object): The game object this handler is attached to

    Example Usage:
        To get an entity's full appearance:
            appearance = entity.appearance.return_appearance(observer)
    """

    def get_display_condition(self, looker, **kwargs):
        """Get the display text for the entity's current health condition.

        Args:
            looker (Object): The entity observing this object
            **kwargs: Additional keyword arguments

        Returns:
            str: A colored text description of the entity's health condition
        """
        percentage = self.obj.health.percent(formatting=None)
        for threshold, display in CONDITION_MAP.items():
            if percentage <= threshold:
                return display
        return "They appear |xunknown|n."

    def _format_worn_items(self, looker, items, header):
        """Format a list of worn items (equipment or clothing) for display.

        Args:
            looker (Object): The entity observing the items
            items (list): List of items to display
            header (str): Header text to use for the item category

        Returns:
            str: Formatted string showing all visible worn items
        """
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
        """Get the display text for all visible equipment worn by the entity.

        Args:
            looker (Object): The entity observing the equipment
            **kwargs: Additional keyword arguments

        Returns:
            str: Formatted string showing all visible equipment
        """
        equipment = self._filter_visible(looker, self.obj.equipment.all())
        result = self._format_worn_items(looker, equipment, EQUIPMENT_HEADER)
        return f"{result}" if result else ""

    def get_display_clothing(self, looker, **kwargs):
        """Get the display text for all visible clothing worn by the entity.

        Args:
            looker (Object): The entity observing the clothing
            **kwargs: Additional keyword arguments

        Returns:
            str: Formatted string showing all visible clothing
        """
        clothing = self._filter_visible(looker, self.obj.clothing.all())
        result = self._format_worn_items(looker, clothing, CLOTHING_HEADER)
        has_equipment = bool(self.obj.equipment.all())
        prefix = "\n\n" if has_equipment else ""
        return f"{prefix}{result}" if result else ""

    def return_appearance(self, looker, **kwargs):
        """Return the complete appearance description of the entity.

        Args:
            looker (Object): The entity observing this object
            **kwargs: Additional keyword arguments

        Returns:
            str: Complete formatted description including physical appearance,
                condition, equipment, and clothing
        """
        if not looker:
            return ""

        return LIVING_APPEARANCE_TEMPLATE.format(
            desc=self.get_display_desc(looker, **kwargs),
            condition=self.get_display_condition(looker, **kwargs),
            equipment=self.get_display_equipment(looker, **kwargs),
            clothing=self.get_display_clothing(looker, **kwargs),
        ).strip()
