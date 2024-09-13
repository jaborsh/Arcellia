from evennia.utils.utils import delay

from world.spells import spells


class Darkness(spells.Spell):
    key = "darkness"
    name = "Darkness"
    desc = "Evoke a magical darkness that darkens an area."
    level = 0
    cost = 0

    def cast(self, caster, **kwargs):
        location = caster.location

        if not location.darken(magical=True):
            caster.msg("The area is already obscured by darkness.")
            return

        location.msg_contents(
            "|x$You() $conj(evoke) a shroud of darkness that obscures the area.|n",
            from_obj=caster,
        )

        delay(
            600,
            location.brighten,
            "|yThe heavy darkness relents, revealing the area.|n",
            True,  # Magical
            persistent=True,
        )


class Firebolt(spells.Spell):
    key = "firebolt"
    name = "Fire Bolt"
    desc = "Hurl a bolt of fire."
    level = 0
    cost = 0

    def cast(self, caster, **kwargs):
        target = kwargs.get("target", None)

        if not target:
            return caster.msg("You must specify a target.")

        caster.location.msg_contents(
            "|#ffa500$You() $conj(hurl) a bolt of fire at $you(target).|n",
            from_obj=caster,
            mapping={"target": target},
        )

        delay(0.5, self.post_cast, caster, target)

    def post_cast(self, caster, target):
        caster.location.msg_contents(
            "|#ffa500The mote of fire strikes $you(target) and burns them!|n",
            mapping={"target": target},
        )


class OrbofLight(spells.Spell):
    key = "orboflight"
    name = "Orb of Light"
    desc = "Evoke a magical orb of light that brightens an area."
    level = 0
    cost = 0

    def cast(self, caster, **kwargs):
        location = caster.location

        if location.tags.has("magical_dark"):
            location.msg_contents(
                "|C$You() $conj(evoke) an orb of light, but the darkness swallows it.|n",
            )
            return

        if not location.brighten():
            return caster.msg("The area is already bright.")

        location.msg_contents(
            "|c$You() $conj(evoke) an orb of light that brightens the area.|n",
            from_obj=caster,
        )

        delay(
            600,
            location.darken,
            "|CAn orb of light fades away.|n",
            persistent=True,
        )


EVOCATION_SPELL_DATA = {
    Darkness.key: Darkness(),
    Firebolt.key: Firebolt(),
    OrbofLight.key: OrbofLight(),
}
