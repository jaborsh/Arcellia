from commands.command import Command


class Spell(Command):
    cost = 0

    def pre_cast(self, caller):
        if caller.mana.current < self.cost:
            return False

        if not self.caller.cooldowns.ready(self.key):
            return False

        caller.mana.current -= self.cost
        return True

    def cast(self, **kwargs):
        pass

    def post_cast(self, caller, cooldown):
        caller.cooldowns.add(self.key, cooldown)

    def func(self):
        pass
