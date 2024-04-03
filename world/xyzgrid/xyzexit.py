from typeclasses.exits import Exit as DefaultExit

from world.xyzgrid.xyzmanager import XYZExitManager
from world.xyzgrid.xyzroom import XYZRoom

MAP_X_TAG_CATEGORY = "room_x_coordinate"
MAP_Y_TAG_CATEGORY = "room_y_coordinate"
MAP_Z_TAG_CATEGORY = "room_z_coordinate"

MAP_XDEST_TAG_CATEGORY = "exit_dest_x_coordinate"
MAP_YDEST_TAG_CATEGORY = "exit_dest_y_coordinate"
MAP_ZDEST_TAG_CATEGORY = "exit_dest_z_coordinate"


class XYZExit(DefaultExit):
    """
    An exit that is aware of the XYZ coordinate system.

    """

    objects = XYZExitManager()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        x, y, z = self.xyz
        xd, yd, zd = self.xyz_destination
        return f"<XYZExit '{self.db_key}', XYZ=({x},{y},{z})->({xd},{yd},{zd})>"

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
                # don't cache yet unfinished coordinate
                return (x, y, z)
            # cache result
            self._xyz = (x, y, z)
        return self._xyz

    @property
    def xyz_destination(self):
        if not hasattr(self, "_xyz_destination"):
            xd = self.tags.get(category=MAP_XDEST_TAG_CATEGORY, return_list=False)
            yd = self.tags.get(category=MAP_YDEST_TAG_CATEGORY, return_list=False)
            zd = self.tags.get(category=MAP_ZDEST_TAG_CATEGORY, return_list=False)
            if xd is None or yd is None or zd is None:
                # don't cache unfinished coordinate
                return (xd, yd, zd)
            # cache result
            self._xyz_destination = (xd, yd, zd)
        return self._xyz_destination

    @classmethod
    def create(
        cls,
        key,
        account=None,
        xyz=(0, 0, "map"),
        xyz_destination=(0, 0, "map"),
        location=None,
        destination=None,
        **kwargs,
    ):
        """
        Creation method aware of coordinates.

        Args:
            key (str): New name of object to create.
            account (Account, optional): Any Account to tie to this entity (unused for exits).
            xyz (tuple or None, optional): A 3D coordinate (X, Y, Z) for this room's location
                on a map grid.  Each element can theoretically be either `int` or `str`, but for the
                XYZgrid contrib, the X, Y are always integers while the `Z` coordinate is used for
                the map's name. Set to `None` if instead using a direct room reference with
                `location`.
            xyz_destination (tuple, optional): The XYZ coordinate of the place the exit
                leads to. Will be ignored if `destination` is given directly.
            location (Object, optional): If given, overrides `xyz` coordinate. This can be used
                to place this exit in any room, including non-XYRoom type rooms.
            destination (Object, optional): If given, overrides `xyz_destination`. This can
                be any room (including non-XYRooms) and is not checked for XYZ coordinates.
            **kwargs: Will be passed into the normal `DefaultRoom.create` method.

        Returns:
            tuple: A tuple `(exit, errors)`, where the errors is a list containing all found
                errors (in which case the returned exit will be `None`).

        """
        tags = []
        if location:
            source = location
        else:
            try:
                x, y, z = xyz
            except ValueError:
                return None, [
                    "XYExit.create need either `xyz=(X,Y,Z)` coordinate or a `location`."
                ]
            else:
                source = XYZRoom.objects.get_xyz(xyz=(x, y, z))
                tags.extend(
                    (
                        (str(x), MAP_X_TAG_CATEGORY),
                        (str(y), MAP_Y_TAG_CATEGORY),
                        (str(z), MAP_Z_TAG_CATEGORY),
                    )
                )
        if destination:
            dest = destination
        else:
            try:
                xdest, ydest, zdest = xyz_destination
            except ValueError:
                return None, [
                    "XYExit.create need either `xyz_destination=(X,Y,Z)` coordinate "
                    "or a `destination`."
                ]
            else:
                dest = XYZRoom.objects.get_xyz(xyz=(xdest, ydest, zdest))
                tags.extend(
                    (
                        (str(xdest), MAP_XDEST_TAG_CATEGORY),
                        (str(ydest), MAP_YDEST_TAG_CATEGORY),
                        (str(zdest), MAP_ZDEST_TAG_CATEGORY),
                    )
                )

        return DefaultExit.create(
            key, source, dest, account=account, tags=tags, typeclass=cls, **kwargs
        )
