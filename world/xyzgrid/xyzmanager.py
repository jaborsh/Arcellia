from django.conf import settings
from django.db.models import Q
from evennia.objects.manager import ObjectManager

# name of all tag categories. Note that the Z-coordinate is
# the `map_name` of the XYZgrid
MAP_X_TAG_CATEGORY = "room_x_coordinate"
MAP_Y_TAG_CATEGORY = "room_y_coordinate"
MAP_Z_TAG_CATEGORY = "room_z_coordinate"

MAP_XDEST_TAG_CATEGORY = "exit_dest_x_coordinate"
MAP_YDEST_TAG_CATEGORY = "exit_dest_y_coordinate"
MAP_ZDEST_TAG_CATEGORY = "exit_dest_z_coordinate"

GET_XYZGRID = None

CLIENT_DEFAULT_WIDTH = settings.CLIENT_DEFAULT_WIDTH


class XYZManager(ObjectManager):
    """
    This is accessed as `.objects` on the coordinate-aware typeclasses (`XYZRoom`, `XYZExit`). It
    has all the normal Object/Room manager methods (filter/get etc) but also special helpers for
    efficiently querying the room in the database based on XY coordinates.

    """

    def filter_xyz(self, xyz=("*", "*", "*"), **kwargs):
        """
        Filter queryset based on XYZ position on the grid. The Z-position is the name of the XYMap
        Set a coordinate to `'*'` to act as a wildcard (setting all coords to `*` will thus find
        *all* XYZ rooms). This will also find children of XYZRooms on the given coordinates.

        Kwargs:
            xyz (tuple, optional): A coordinate tuple (X, Y, Z) where each element is either
                an `int` or `str`. The character `'*'` acts as a wild card. Note that
                the `Z`-coordinate is the name of the map (case-sensitive) in the XYZgrid contrib.
            **kwargs: All other kwargs are passed on to the query.

        Returns:
            django.db.queryset.Queryset: A queryset that can be combined
            with further filtering.

        """
        x, y, z = xyz
        wildcard = "*"

        return (
            self.filter_family(**kwargs)
            .filter(
                Q()
                if x == wildcard
                else Q(db_tags__db_key=str(x), db_tags__db_category=MAP_X_TAG_CATEGORY)
            )
            .filter(
                Q()
                if y == wildcard
                else Q(db_tags__db_key=str(y), db_tags__db_category=MAP_Y_TAG_CATEGORY)
            )
            .filter(
                Q()
                if z == wildcard
                else Q(
                    db_tags__db_key__iexact=str(z),
                    db_tags__db_category=MAP_Z_TAG_CATEGORY,
                )
            )
        )

    def get_xyz(self, xyz=(0, 0, "map"), **kwargs):
        """
        Always return a single matched entity directly. This accepts no `*`-wildcards.
        This will also find children of XYZRooms on the given coordinates.

        Kwargs:
            xyz (tuple): A coordinate tuple of `int` or `str` (not `'*'`, no wildcards are
                allowed in get).  The `Z`-coordinate acts as the name (case-sensitive) of the map in
                the XYZgrid contrib.
            **kwargs: All other kwargs are passed on to the query.

        Returns:
            XYRoom: A single room instance found at the combination of x, y and z given.

        Raises:
            XYZRoom.DoesNotExist: If no matching query was found.
            XYZRoom.MultipleObjectsReturned: If more than one match was found (which should not
                possible with a unique combination of x,y,z).

        """
        # filter by tags, then figure out of we got a single match or not
        query = self.filter_xyz(xyz=xyz, **kwargs)
        ncount = query.count()
        if ncount == 1:
            return query.first()

        # error - mimic default get() behavior but with a little more info
        x, y, z = xyz
        inp = f"Query: xyz=({x},{y},{z}), " + ",".join(
            f"{key}={val}" for key, val in kwargs.items()
        )
        if ncount > 1:
            raise self.model.MultipleObjectsReturned(inp)
        else:
            raise self.model.DoesNotExist(inp)


class XYZExitManager(XYZManager):
    """
    Used by Exits.
    Manager that also allows searching for destinations based on XY coordinates.

    """

    def filter_xyz_exit(
        self, xyz=("*", "*", "*"), xyz_destination=("*", "*", "*"), **kwargs
    ):
        """
        Used by exits (objects with a source and -destination property).
        Find all exits out of a source or to a particular destination. This will also find
        children of XYZExit on the given coords..

        Kwargs:
            xyz (tuple, optional): A coordinate (X, Y, Z) for the source location. Each
                element is either an `int` or `str`. The character `'*'` is used as a wildcard -
                so setting all coordinates to the wildcard will return *all* XYZExits.
                the `Z`-coordinate is the name of the map (case-sensitive) in the XYZgrid contrib.
            xyz_destination (tuple, optional): Same as `xyz` but for the destination of the
                exit.
            **kwargs: All other kwargs are passed on to the query.

        Returns:
            django.db.queryset.Queryset: A queryset that can be combined
            with further filtering.

        Notes:
            Depending on what coordinates are set to `*`, this can be used to
            e.g. find all exits in a room, or leading to a room or even to rooms
            in a particular X/Y row/column.

            In the XYZgrid, `z_source != z_destination` means a _transit_ between different maps.

        """
        x, y, z = xyz
        xdest, ydest, zdest = xyz_destination
        wildcard = "*"

        return (
            self.filter_family(**kwargs)
            .filter(
                Q()
                if x == wildcard
                else Q(db_tags__db_key=str(x), db_tags__db_category=MAP_X_TAG_CATEGORY)
            )
            .filter(
                Q()
                if y == wildcard
                else Q(db_tags__db_key=str(y), db_tags__db_category=MAP_Y_TAG_CATEGORY)
            )
            .filter(
                Q()
                if z == wildcard
                else Q(
                    db_tags__db_key__iexact=str(z),
                    db_tags__db_category=MAP_Z_TAG_CATEGORY,
                )
            )
            .filter(
                Q()
                if xdest == wildcard
                else Q(
                    db_tags__db_key=str(xdest),
                    db_tags__db_category=MAP_XDEST_TAG_CATEGORY,
                )
            )
            .filter(
                Q()
                if ydest == wildcard
                else Q(
                    db_tags__db_key=str(ydest),
                    db_tags__db_category=MAP_YDEST_TAG_CATEGORY,
                )
            )
            .filter(
                Q()
                if zdest == wildcard
                else Q(
                    db_tags__db_key__iexact=str(zdest),
                    db_tags__db_category=MAP_ZDEST_TAG_CATEGORY,
                )
            )
        )

    def get_xyz_exit(self, xyz=(0, 0, "map"), xyz_destination=(0, 0, "map"), **kwargs):
        """
        Used by exits (objects with a source and -destination property). Get a single
        exit. All source/destination coordinates (as well as the map's name) are required.
        This will also find children of XYZExits on the given coords.

        Kwargs:
            xyz (tuple, optional): A coordinate (X, Y, Z) for the source location. Each
                element is either an `int` or `str` (not `*`, no wildcards are allowed for get).
                the `Z`-coordinate is the name of the map (case-sensitive) in the XYZgrid contrib.
            xyz_destination_coord (tuple, optional): Same as the `xyz` but for the destination of
                the exit.
            **kwargs: All other kwargs are passed on to the query.

        Returns:
            XYZExit: A single exit instance found at the combination of x, y and xgiven.

        Raises:
            XYZExit.DoesNotExist: If no matching query was found.
            XYZExit.MultipleObjectsReturned: If more than one match was found (which should not
                be possible with a unique combination of x,y,x).

        Notes:
            All coordinates are required.

        """
        x, y, z = xyz
        xdest, ydest, zdest = xyz_destination
        # mimic get_family
        paths = [self.model.path] + [
            "%s.%s" % (cls.__module__, cls.__name__)
            for cls in self._get_subclasses(self.model)
        ]
        kwargs["db_typeclass_path__in"] = paths

        try:
            return (
                self.filter(
                    db_tags__db_key__iexact=str(z),
                    db_tags__db_category=MAP_Z_TAG_CATEGORY,
                )
                .filter(db_tags__db_key=str(x), db_tags__db_category=MAP_X_TAG_CATEGORY)
                .filter(db_tags__db_key=str(y), db_tags__db_category=MAP_Y_TAG_CATEGORY)
                .filter(
                    db_tags__db_key=str(xdest),
                    db_tags__db_category=MAP_XDEST_TAG_CATEGORY,
                )
                .filter(
                    db_tags__db_key=str(ydest),
                    db_tags__db_category=MAP_YDEST_TAG_CATEGORY,
                )
                .filter(
                    db_tags__db_key__iexact=str(zdest),
                    db_tags__db_category=MAP_ZDEST_TAG_CATEGORY,
                )
                .get(**kwargs)
            )
        except self.model.DoesNotExist:
            inp = (
                f"xyz=({x},{y},{z}),xyz_destination=({xdest},{ydest},{zdest}),"
                + ",".join(f"{key}={val}" for key, val in kwargs.items())
            )
            raise self.model.DoesNotExist(
                f"{self.model.__name__} matching query {inp} does not exist."
            )


# class XYZMobManager(XYZManager):
#     pass
