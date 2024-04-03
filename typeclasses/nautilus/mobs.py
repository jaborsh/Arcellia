from evennia.utils import delay

from typeclasses.mobs import Mob


class Enchantress(Mob):
    def greeting(self):
        def _say():
            self.execute_cmd("say You! Get me out of this damn cell!")

        delay(1, _say)
