"""
XYZ-aware rooms and exits.

These are intended to be used with the XYZgrid - which interprets the `Z` 'coordinate' as
different (named) 2D XY  maps. But if not wanting to use the XYZgrid gridding, these can also be
used as stand-alone XYZ-coordinate-aware rooms.

"""

from django.conf import settings
from typeclasses.rooms import Room as DefaultRoom

from world.xyzgrid.xyzmanager import XYZManager

# name of all tag categories. Note that the Z-coordinate is
# the `map_name` of the XYZgrid
MAP_X_TAG_CATEGORY = "room_x_coordinate"
MAP_Y_TAG_CATEGORY = "room_y_coordinate"
MAP_Z_TAG_CATEGORY = "room_z_coordinate"

GET_XYZGRID = None

CLIENT_DEFAULT_WIDTH = settings.CLIENT_DEFAULT_WIDTH


class XYZRoom(DefaultRoom):
    """
    A game location aware of its XYZ-position.

    Special properties:
        map_display (bool): If the return_appearance of the room should
            show the map or not.
        map_mode (str): One of 'nodes' or 'scan'. See `return_apperance`
            for examples of how they differ.
        map_visual_range (int): How far on the map one can see. This is a
            fixed value here, but could also be dynamic based on skills,
            light etc.
        map_character_symbol (str): The character symbol to use to show
            the character position. Can contain color info. Default is
            the @-character.
        map_area_client (bool): If True, map area will always fill the entire
            client width. If False, the map area's width will vary with the
            width of the currently displayed location description.
        map_fill_all (bool): I the map area should fill the client width or not.
        map_separator_char (str): The char to use to separate the map area from
            the room description.

    """

    # makes the `room.objects.filter_xymap` available
    objects = XYZManager()

    # default settings for map visualization
    map_display = True
    map_mode = "nodes"  # or 'scan'
    map_visual_range = 2
    map_character_symbol = "|g@|n"
    map_align = "c"
    map_target_path_style = "|y{display_symbol}|n"
    map_fill_all = True
    map_separator_char = "|x~|n"

    def __str__(self):
        return repr(self)

    def __repr__(self):
        x, y, z = self.xyz
        return f"<XYZRoom '{self.db_key}', XYZ=({x},{y},{z})>"

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
        """
        Creation method aware of XYZ coordinates.

        Args:
            key (str): New name of object to create.
            account (Account, optional): Any Account to tie to this entity (usually not used for
                rooms).
            xyz (tuple, optional): A 3D coordinate (X, Y, Z) for this room's location on a
                map grid. Each element can theoretically be either `int` or `str`, but for the
                XYZgrid, the X, Y are always integers while the `Z` coordinate is used for the
                map's name.
            **kwargs: Will be passed into the normal `DefaultRoom.create` method.

        Returns:
            room (Object): A newly created Room of the given typeclass.
            errors (list): A list of errors in string form, if any.

        Notes:
            The (X, Y, Z) coordinate must be unique across the game. If trying to create
            a room at a coordinate that already exists, an error will be returned.

        """
        try:
            x, y, z = xyz
        except ValueError:
            return None, [
                f"XYRroom.create got `xyz={xyz}` - needs a valid (X,Y,Z) "
                "coordinate of ints/strings."
            ]

        existing_query = cls.objects.filter_xyz(xyz=(x, y, z))
        if existing_query.exists():
            existing_room = existing_query.first()
            return None, [
                f"XYRoom XYZ=({x},{y},{z}) already exists "
                f"(existing room is named '{existing_room.db_key}')!"
            ]

        tags = (
            (str(x), MAP_X_TAG_CATEGORY),
            (str(y), MAP_Y_TAG_CATEGORY),
            (str(z), MAP_Z_TAG_CATEGORY),
        )

        return DefaultRoom.create(
            key, account=account, tags=tags, typeclass=cls, **kwargs
        )

    def get_display_name(self, looker, **kwargs):
        """
        Shows both the #dbref and the xyz coord to staff.

        Args:
            looker (TypedObject): The object or account that is looking
                at/getting inforamtion for this object.

        Returns:
            name (str): A string containing the name of the object,
                including the DBREF and XYZ coord if this user is
                privileged to control the room.

        """
        if self.locks.check_lockstring(looker, "perm(Builder)"):
            x, y, z = self.xyz
            return f"{self.name}[#{self.id}({x},{y},{z})]"
        return self.name
