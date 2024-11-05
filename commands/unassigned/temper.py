from typing import Callable, Dict

from evennia.utils import delay, inherits_from

from commands.command import Command
from server.conf.at_search import SearchReturnType
from typeclasses.equipment.weapons import Weapon, WeaponType


class CmdTemper(Command):
    """
    Modify a weapon's properties.

    Usage:
        temper <weapon> <modification>

    Available modifications:
        standard, heavy, keen, quality
    """

    key = "temper"
    locks = "cmd:pperm(Admin)"
    help_category = "Unassigned"

    def __init__(self):
        super().__init__()
        self.modifications: Dict[str, Callable] = {
            "standard": self._standard_modification,
            "heavy": self._heavy_modification,
            "keen": self._keen_modification,
            "quality": self._quality_modification,
        }

    def _standard_modification(self, caller, weapon: Weapon) -> None:
        if weapon.weapon_type == WeaponType.STANDARD:
            caller.msg(
                "To restore this weapon to its unremarkable, thoroughly ordinary self would be the work of a visionary if it were not already as plain as it appears."
            )
            return

        caller.location.msg_contents(
            "|#708090With a resigned nod, $you() begin $pron(your,pa) $conj(work), stripping away refinement from a $you(weapon). Each stroke brings the blade closer to simplicity.|n",
            from_obj=caller,
            mapping={"weapon": weapon},
        )

        delay(
            5,
            self._success,
            caller,
            weapon,
            "|#696969The $you(weapon) $conj(rest,weapon), returned to its humble, functional state.|n",
        )

        weapon.weapon_type = WeaponType.STANDARD

    def _heavy_modification(self, caller, weapon: Weapon) -> None:
        if weapon.weapon_type == WeaponType.HEAVY:
            caller.msg(
                "To make heavy that which is already weighed down will render the weaopn unwieldly."
            )
            return

        caller.location.msg_contents(
            "|#7B3F00$You() $conj(take) hammer to steel, each strike resonating with purpose. Sparks fly and sweat mingles with smoke as a $you(weapon) begins to reluctantly yield into a form of greater heft and might|n.",
            mapping={"weapon": weapon},
            from_obj=caller,
        )

        delay(
            5,
            self._success,
            caller,
            weapon,
            "|#355E3BAt last, $you() $conj(step) back and a $you(weapon) $conj(rest,weapon) before $pron(them,pa). It now bears a heavy edge capable of sundering armor and bone.|n",
        )

        weapon.weapon_type = WeaponType.HEAVY

    def _keen_modification(self, caller, weapon: Weapon) -> None:
        if weapon.weapon_type == WeaponType.KEEN:
            caller.msg("You cannot sharpen an already razor-sharp weapon.")
            return

        caller.location.msg_contents(
            "|#8B4513$You() $conj(lean) in and $conj(coax) a $you(weapon), each movement sharpening the weapon to draw out its latent potential.|n",
            from_obj=caller,
            mapping={"weapon": weapon},
        )

        delay(
            5,
            self._success,
            caller,
            weapon,
            "|#4682B4The work is complete: the $you(weapon) $conj(glitter,weapon) with a keen edge, light as air.|n",
        )

        weapon.weapon_type = WeaponType.KEEN

    def _quality_modification(self, caller, weapon: Weapon) -> None:
        if weapon.weapon_type == WeaponType.QUALITY:
            caller.msg(
                "To seek quality in a blade already refined to the standards of the finest artisans is to demand the sun shine a little brighter or ask a mountain to grow a little taller."
            )
            return

        caller.location.msg_contents(
            "|#556B2F$You() $conj(study) a $you(weapon) with a discerning eye, assessing every inch before beginning the work of tempering the weapon to a higher standard. With precision, $you() strike a balance between strength and grace.|n",
            from_obj=caller,
            mapping={"weapon": weapon},
        )

        delay(
            5,
            self._success,
            caller,
            weapon,
            "|#2F4F4FWith a final, confident strike, $you() $conj(step) back, admiring $your() work. The $you(weapon) $conj(gleam,weapon) with a new vigor.",
        )
        weapon.weapon_type = WeaponType.QUALITY

    def _success(self, caller, weapon: Weapon, message: str) -> None:
        caller.location.msg_contents(
            message, mapping={"weapon": weapon}, from_obj=caller
        )

    def func(self) -> None:
        if not self.args:
            self.caller.msg(
                "To temper neither a weapon nor quality is a feat reserved for only the most abstract of weaponsmiths. (Syntax: temper <weapon> <modification>)"
            )
            return

        args = self.args.strip().split()
        if len(args) < 2:
            self.caller.msg(
                "An admirable attempt at minimalism, but tempering the weapon with nothing yields precisely nothing. (Syntax: temper <weapon> <modification>)"
            )
            return

        weapon_name, modification = args[0], args[1].lower()
        weapon = self.caller.search(
            weapon_name,
            candidates=self.caller.contents,
            quiet=True,
            return_quantity=1,
            return_type=SearchReturnType.ONE,
        )

        if not weapon:
            self.caller.msg(
                "One seeks to temper a weapon that is, regrettably, unfound. Perhaps try tempering something tangible first. (Syntax: temper <weapon> <modification>)"
            )
            return

        weapon = weapon[0]
        if not inherits_from(weapon, Weapon):
            self.caller.msg(
                "A noble pursuit, though perhaps a weapon might respond with a bit more enthusiasm."
            )
            return

        modification_method = self.modifications.get(modification)
        if not modification_method:
            self.caller.msg(
                f"An inspired choice - if only '{modification}' were a quality this weapon could embrace; perhaps something else would suffice? (Syntax: temper <weapon> <modification>)"
            )
            return

        modification_method(self.caller, weapon)
