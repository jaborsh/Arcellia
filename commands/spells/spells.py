class Spell:
    name = "Spell"
    desc = "A spell."
    cost = 0

    def pre_cast(self, caster, **kwargs):
        pass

    def cast(self, caster, **kwargs):
        pass

    def post_cast(self, caster, **kwargs):
        pass
