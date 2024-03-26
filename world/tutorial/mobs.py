from evennia.utils import delay

from world.xyzgrid.xyzmob import XYZMob


class Enchantress(XYZMob):
    def greeting(self):
        def _say():
            self.execute_cmd("say You! Get me out of this damn cell!")

        delay(1, _say)
