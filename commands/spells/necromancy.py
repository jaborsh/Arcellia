from evennia.utils.utils import delay

from commands.spells import spells


class GhostlyTouch(spells.Spell):
    key = "ghostlytouch"
    name = "Ghostly Touch"
    desc = "Assail a creature with the chill of the grave."
    level = 0
    cost = 0

    def cast(self, caster, **kwargs):
        target = kwargs.get("target", None)

        if not target:
            return caster.msg("You must specify a target.")

        caster.location.msg_contents(
            "|c$You() $conj(reach) towards $you(target) with a ghostly hand.|n",
            from_obj=caster,
            mapping={"target": target},
        )

        delay(0.5, self.post_cast, caster, target)

    def post_cast(self, caster, target):
        caster.location.msg_contents(
            "|c$You() $conj(assail) $you(target) with a grave chill!|n",
            from_obj=caster,
            mapping={"target": target},
        )


NECROMANCY_SPELL_DATA = {
    GhostlyTouch.key: GhostlyTouch(),
}
