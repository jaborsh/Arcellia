from typeclasses.mobs import Mob as DefaultMob
from typeclasses.mobs import Monster as DefaultMonster

from world.xyzgrid.xyzmanager import XYZMobManager
from world.xyzgrid.xyzroom import (
    MAP_X_TAG_CATEGORY,
    MAP_Y_TAG_CATEGORY,
    MAP_Z_TAG_CATEGORY,
)


class XYZMob(DefaultMob):
    objects = XYZMobManager()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        x, y, z = self.xyz
        return f"<XYZMob '{self.db_key}', XYZ=({x},{y},{z})>"

    @property
    def xyzgrid(self):
        global GET_XYZGRID
        if not GET_XYZGRID:
            from world.xyzgrid.xyzgrid import get_xyzgrid as GET_XYZGRID
        return GET_XYZGRID()

    @property
    def xyz(self):
        if not hasattr(self, "_xyz"):
            x = self.tags.get(category=MAP_X_TAG_CATEGORY, return_list=False)
            y = self.tags.get(category=MAP_Y_TAG_CATEGORY, return_list=False)
            z = self.tags.get(category=MAP_Z_TAG_CATEGORY, return_list=False)
            if x is None or y is None or z is None:
                return (x, y, z)
            self._xyz = (x, y, z)
        return self._xyz


class XYZMonster(DefaultMonster):
    objects = XYZMobManager()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        x, y, z = self.xyz
        return f"<XYZMob '{self.db_key}', XYZ=({x},{y},{z})>"

    @property
    def xyzgrid(self):
        global GET_XYZGRID
        if not GET_XYZGRID:
            from world.xyzgrid.xyzgrid import get_xyzgrid as GET_XYZGRID
        return GET_XYZGRID()

    @property
    def xyz(self):
        if not hasattr(self, "_xyz"):
            x = self.tags.get(category=MAP_X_TAG_CATEGORY, return_list=False)
            y = self.tags.get(category=MAP_Y_TAG_CATEGORY, return_list=False)
            z = self.tags.get(category=MAP_Z_TAG_CATEGORY, return_list=False)
            if x is None or y is None or z is None:
                return (x, y, z)
            self._xyz = (x, y, z)
        return self._xyz
