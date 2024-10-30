"""
XYZ-aware mobs.

These are intended to be used with the XYZgrid - which interprets the `Z` 'coordinate' as
different (named) 2D XY maps. But if not wanting to use the XYZgrid gridding, these can also be
used as stand-alone XYZ-coordinate-aware mobs.
"""

from django.conf import settings

from typeclasses.mobs import Mob as DefaultMob
from world.xyzgrid.xyzmanager import XYZMobManager
from world.xyzgrid.xyzroom import XYZRoom

# name of all tag categories. Note that the Z-coordinate is
# the `map_name` of the XYZgrid
MAP_X_TAG_CATEGORY = "room_x_coordinate"
MAP_Y_TAG_CATEGORY = "room_y_coordinate"
MAP_Z_TAG_CATEGORY = "room_z_coordinate"

GET_XYZGRID = None

CLIENT_DEFAULT_WIDTH = settings.CLIENT_DEFAULT_WIDTH


class XYZMob(DefaultMob):
    objects = XYZMobManager()

    @property
    def xyz(self):
        if not hasattr(self, "_xyz"):
            x = self.tags.get(category=MAP_X_TAG_CATEGORY, return_list=False)
            y = self.tags.get(category=MAP_Y_TAG_CATEGORY, return_list=False)
            z = self.tags.get(category=MAP_Z_TAG_CATEGORY, return_list=False)
            if x is None or y is None or z is None:
                # don't cache unfinished coordinate (probably tags have not finished saving)
                return tuple(
                    int(coord)
                    if coord is not None and coord.lstrip("-").isdigit()
                    else coord
                    for coord in (x, y, z)
                )
            # cache result, convert to correct types (tags are strings)
            self._xyz = tuple(
                int(coord) if coord.lstrip("-").isdigit() else coord
                for coord in (x, y, z)
            )

        return self._xyz

    @property
    def xyzgrid(self):
        global GET_XYZGRID
        if not GET_XYZGRID:
            from world.xyzgrid.xyzgrid import get_xyzgrid as GET_XYZGRID
        return GET_XYZGRID()

    @property
    def xymap(self):
        if not hasattr(self, "_xymap"):
            xyzgrid = self.xyzgrid
            _, _, Z = self.xyz
            self._xymap = xyzgrid.get_map(Z)
        return self._xymap

    @classmethod
    def create(cls, key, account=None, xyz=(0, 0, "map"), **kwargs):
        try:
            x, y, z = xyz
        except ValueError:
            return None, [
                f"XYZMob.create got `xyz={xyz}` - needs a valid (X,Y,Z) coordinate of ints/strings."
            ]

        location = XYZRoom.objects.get_xyz(xyz=(x, y, z))
        kwargs["location"] = location
        kwargs["home"] = location
        tags = (
            (str(x), MAP_X_TAG_CATEGORY),
            (str(y), MAP_Y_TAG_CATEGORY),
            (str(z), MAP_Z_TAG_CATEGORY),
        )

        return DefaultMob.create(
            key, account=account, tags=tags, typeclass=cls, **kwargs
        )
