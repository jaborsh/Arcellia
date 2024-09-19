from commands.command import Command


class Spell(Command):
    def pre_cast(self):
        return True

    def cast(self):
        pass

    def post_cast(self):
        pass

    def func(self):
        if not self.pre_cast():
            return self.caller.msg("Your casting fails.")

        self.cast()
