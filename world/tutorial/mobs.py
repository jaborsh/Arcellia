from evennia.utils import delay
from typeclasses import mobs


class Enchantress(mobs.Mob):
    def greeting(self):
        def _say():
            self.execute_cmd("say You! Get me out of this damn cell!")

        delay(1, _say)
