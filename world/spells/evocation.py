from evennia.utils import delay

from . import spells


class OrbofLight(spells.Spell):
    key = "orboflight"
    name = "Orb of Light"
    desc = "Evoke a magical orb of light that brightens an area."
    level = 0
    cost = 0

    school = spells.SpellSchool.EVOCATION
    delivery = spells.SpellDelivery.SELF

    def cast(self, caster, **kwargs):
        location = caster.location

        if location.tags.get("magical_dark"):
            location.msg_contents(
                "|C$You() $conj(evokes) an orb of light, but the darkness swallows it.|n",
            )
            return

        if not location.brighten():
            return caster.msg("The area is already bright.")

        location.msg_contents(
            "|c$You() $conj(evokes) an orb of light that brightens the area.|n",
            from_obj=caster,
        )

        delay(
            600,
            location.darken,
            "|CAn orb of light fades away.|n",
            persistent=True,
        )


class Darkness(spells.Spell):
    key = "darkness"
    name = "Darkness"
    desc = "Evoke a magical darkness that darkens an area."
    level = 0
    cost = 0

    school = spells.SpellSchool.EVOCATION
    delivery = spells.SpellDelivery.SELF

    def cast(self, caster, **kwargs):
        location = caster.location

        if not location.darken(magical=True):
            caster.msg("The area is already obscured by darkness.")
            return

        location.msg_contents(
            "|x$You() $conj(evokes) a shroud of darkness that obscures the area.|n",
            from_obj=caster,
        )

        delay(
            600,
            location.brighten,
            "|yThe heavy darkness relents, revealing the area.|n",
            True,  # Magical
            persistent=True,
        )


EVOCATION_SPELL_DATA = {
    OrbofLight.key: OrbofLight(),
    Darkness.key: Darkness(),
}
