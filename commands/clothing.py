from evennia.utils import create
from parsing.colors import strip_ansi
from typeclasses.clothing import Clothing, ClothingType

from commands.command import Command

__all__ = ["CmdTailor"]


class CmdTailor(Command):
    """
    Syntax: tailor <item>

    Example: tailor purple cotton tunic

    Tailor an article of clothing. You will be asked to describe the item,
    provide aliases if you wish for alternative identifiers, and declare the
    clothing type. The clothing type is used to determine where the item is
    worn on the body.

    The following clothing types are available:
        - headwear (worn on head)
        - eyewear (worn on eyes)
        - earring (worn on ears)
        - neckwear (worn around neck)
        - undershirt (worn on torso)
        - top (worn about torso)
        - fullbody (worn on body)
        - wristwear (worn around wrists)
        - handwear (worn on hands)
        - ring (worn on finger)
        - belt (worn around waist)
        - underwear (worn on hips)
        - bottom (worn on legs)
        - footwear (worn on feet)

    """

    key = "tailor"
    locks = "cmd:all()"
    help_category = "Merchant"
    new_obj_lockstring = (
        "control:id({id}) or perm(Admin);delete:id({id}) or perm(Admin)"
    )

    def _type_list(self):
        return "\n ".join(
            [f"{idx + 1}. {t.value}" for idx, t in enumerate(ClothingType)]
        )

    def map_type(self, clothing_type):
        type_map = {
            "headwear": ClothingType.HEADWEAR,
            "eyewear": ClothingType.EYEWEAR,
            "earring": ClothingType.EARRING,
            "neckwear": ClothingType.NECKWEAR,
            "undershirt": ClothingType.UNDERSHIRT,
            "top": ClothingType.TOP,
            "fullbody": ClothingType.FULLBODY,
            "wristwear": ClothingType.WRISTWEAR,
            "handwear": ClothingType.HANDWEAR,
            "ring": ClothingType.RING,
            "belt": ClothingType.BELT,
            "underwear": ClothingType.UNDERWEAR,
            "bottom": ClothingType.BOTTOM,
            "footwear": ClothingType.FOOTWEAR,
        }

        clothing_type = type_map.get(clothing_type.lower(), None)
        return clothing_type

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            caller.msg("What would you like to tailor?")
            return

        key = strip_ansi(args)
        caller.msg("|YYou begin to tailor some clothing...|n")
        caller.location.msg_contents(
            f"|Y{caller} begins to tailor some clothing.|n", exclude=caller
        )

        description = yield (f"Describe the {args}|n:")

        aliases = yield ("Enter any aliases for the item separated by commas:")
        if aliases:
            aliases = [strip_ansi(alias.strip()) for alias in aliases.split(",")]

        clothing_type = yield ("What type of clothing is it? (top, bottom, etc.)")
        clothing_type = self.map_type(clothing_type)
        if not clothing_type:
            caller.msg("|rAborting|n: You must specify a valid clothing type.")
            return

        lockstring = self.new_obj_lockstring.format(id=caller.id)
        clothing = create.create_object(
            Clothing,
            key,
            caller,
            home=None,
            aliases=aliases,
            locks=lockstring,
            report_to=caller,
        )

        if not clothing:
            return

        clothing.clothing_type = clothing_type

        if description:
            clothing.db.desc = description + "|n"
        else:
            clothing.db.desc = "You see nothing special."

        clothing.display_name = args + "|n"

        caller.msg(
            "|YYou tie off a final stitch and step back to admire your handiwork.|n"
        )
        caller.location.msg_contents(
            f"|Y{caller} ties off a final stitch and steps back.|n", exclude=caller
        )
