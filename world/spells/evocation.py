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
        location.brighten()
        location.msg_contents(
            "|c$You() $conj(evokes) an orb of light that brightens the area.|n",
            from_obj=caster,
        )

        delay(
            60,
            location.darken,
            "|CAn orb of light fades away.|n",
            persistent=True,
        )


EVOCATION_SPELL_DATA = {
    OrbofLight.key: OrbofLight(),
}
