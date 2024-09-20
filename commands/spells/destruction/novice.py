from commands.spells.spells import Spell
from server.conf.at_search import SearchReturnType

__all__ = ("SpellPebble",)


class SpellPebble(Spell):
    """
    Syntax: pebble <target>

    The pebble spell is a fundamental cantrip taught to aspiring wizards and sorcerers. Drawing upon one's own essence, the caster conjures a small, crystalline stone infused with raw magical energy. When released, this enchanted pebble hurls forward. Though humble, the pebble is revered as a critical step in mastering the manipulation of magical forces.

    Scholars speak of the Pebble as the simplest, yet most profound spell, representing the transition from raw untapped talent to disciplined control over magic. Many an archmage began their journey with the conjuration of this small stone.
    """

    key = "pebble"
    locks = "cmd:stat_ge(intelligence, 2)"
    help_category = "Destruction"

    cost = 7
    error = "|CThe pebble fizzles, leaving only a faint shimmer of light before dissipating into nothingness.|n"

    def func(self):
        caller = self.caller
        args = self.args

        target = caller.search(
            args,
            quiet=True,
            return_quantity=1,
            return_type=SearchReturnType.ONE,
        )
        if not self.pre_cast(caller) or not target:
            return caller.msg(self.error)

        target = target[0]
        self.cast(caller, target)
        self.post_cast(caller, 1)

    def cast(self, caller, target):
        caller.location.msg_contents(
            "|c$Your() magic pebble shoots forward with a sharp, crystalline glint, striking $you(target).|n",
            from_obj=caller,
            mapping={"target": target},
        )

        damage = caller.intelligence.current * 1.52
        target.at_damage(damage)
