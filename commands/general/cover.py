from evennia.utils import inherits_from

from commands.command import Command
from handlers.config.clothing_config import ClothingConfig
from handlers.equipment import EQUIPMENT_TYPE_COVER
from typeclasses.clothing import Clothing
from typeclasses.equipment.equipment import Equipment


class CmdCover(Command):
    """
    Syntax: cover <clothing> with <clothing>

    This command allows a character to cover one clothing object with another.
    Both the clothing objects must be in the character's inventory. The command
    takes two arguments: the first argument is the clothing object to be
    covered, and the second argument is the clothing object to be used as a
    cover.
    """

    key = "cover"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            return caller.msg("Cover what?")

        args = args.split(" with ")

        if len(args) != 2:
            return caller.msg("Cover what with what?")

        obj = caller.search(args[0], candidates=caller.contents)
        if not obj:
            return

        if not inherits_from(obj, Clothing):
            return caller.msg("You can't cover that.")

        if obj not in caller.clothing.all():
            return caller.msg("You cannot cover something you aren't wearing.")

        cover = caller.search(args[1], candidates=caller.contents)
        if not cover:
            return

        if not inherits_from(cover, Clothing) and not inherits_from(
            cover, Equipment
        ):
            return caller.msg("You can't use that to cover something.")

        if inherits_from(cover, Clothing):
            if cover not in caller.clothing.all():
                return caller.msg(
                    "You cannot use something you aren't wearing to cover something."
                )

            if (
                obj.clothing_type
                not in ClothingConfig.CLOTHING_TYPE_COVER[cover.clothing_type]
            ):
                return caller.msg("You can't cover that with that.")

        elif inherits_from(cover, Equipment):
            if cover not in caller.equipment.all():
                return caller.msg(
                    "You cannot use something you aren't wearing to cover something."
                )

            if (
                obj.clothing_type
                not in EQUIPMENT_TYPE_COVER[cover.equipment_type]
            ):
                return caller.msg("You can't cover that with that.")

        if cover in obj.covered_by:
            return caller.msg(
                f"{cover.get_display_name(caller)} is already covering {obj.get_display_name(caller)}."
            )

        obj.covered_by.append(cover)
        cover.covering.append(obj)
        caller.location.msg_contents(
            f"$You() $conj(cover) {obj.get_display_name(caller)} with {cover.get_display_name(caller)}.",
            from_obj=caller,
        )
