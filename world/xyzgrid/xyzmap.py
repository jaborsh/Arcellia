from os import mkdir
from os.path import isdir
from os.path import join as pathjoin

from django.conf import settings
from evennia.contrib.grid.xyzgrid import xymap, xymap_legend
from evennia.contrib.grid.xyzgrid.utils import MapError
from evennia.prototypes import prototypes as protlib
from evennia.utils.utils import is_iter, mod_import, variable_from_module

_LOADED_PROTOTYPES = None
_NO_DB_PROTOTYPES = True
if hasattr(settings, "XYZGRID_USE_DB_PROTOTYPES"):
    _NO_DB_PROTOTYPES = not settings.XYZGRID_USE_DB_PROTOTYPES
_CACHE_DIR = settings.CACHE_DIR

DEFAULT_LEGEND = xymap_legend.LEGEND
MAP_DATA_KEYS = [
    "zcoord",
    "map",
    "legend",
    "prototypes",
    "mobile_prototypes",
    "item_prototypes",
    "options",
    "module_path",
]


class XYZMap(xymap.XYMap):
    def __init__(self, map_module_or_dict, Z="map", xyzgrid=None):
        """
        Initialize the map parser by feeding it the map.

        Args:
            map_module_or_dict (str, module or dict): Path or module pointing to a map. If a dict,
                this should be a dict with a MAP_DATA key 'map' and optionally a 'legend'
                dicts to specify the map structure.
            Z (int or str, optional): Name or Z-coord for for this map. Needed if the game uses
                more than one map. If not given, it can also be embedded in the
                `map_module_or_dict`. Used when referencing this map during map transitions,
                baking of pathfinding matrices etc.
            xyzgrid (.xyzgrid.XYZgrid): A top-level grid this map is a part of.

        Notes:
            Interally, the map deals with two sets of coordinate systems:
            - grid-coordinates x,y are the character positions in the map string.
            - world-coordinates X,Y are the in-world coordinates of nodes/rooms.
              There are fewer of these since they ignore the 'link' spaces between
              the nodes in the grid, s

                  X = x // 2
                  Y = y // 2

            - The Z-coordinate, if given, is only used when transitioning between maps
              on the supplied `grid`.

        """
        global _LOADED_PROTOTYPES
        if not _LOADED_PROTOTYPES:
            # inject default prototypes, but don't override prototype-keys loaded from
            # settings, if they exist (that means the user wants to replace the defaults)
            protlib.load_module_prototypes(
                "evennia.contrib.grid.xyzgrid.prototypes", override=False
            )
            _LOADED_PROTOTYPES = True

        self.Z = Z
        self.xyzgrid = xyzgrid

        self.mapstring = ""
        self.raw_mapstring = ""

        # store so we can reload
        self.map_module_or_dict = map_module_or_dict

        self.prototypes = None
        self.options = None

        # transitional mapping
        self.symbol_map = None

        # map setup
        self.xygrid = None
        self.XYgrid = None
        self.display_map = None
        self.max_x = 0
        self.max_y = 0
        self.max_X = 0
        self.max_Y = 0

        # Dijkstra algorithm variables
        self.node_index_map = None
        self.dist_matrix = None
        self.pathfinding_routes = None

        self.pathfinder_baked_filename = None
        if Z:
            if not isdir(_CACHE_DIR):
                mkdir(_CACHE_DIR)
            self.pathfinder_baked_filename = pathjoin(_CACHE_DIR, f"{Z}.P")

        # load data and parse it
        self.reload()

    def reload(self, map_module_or_dict=None):
        """
        (Re)Load a map.

        Args:
            map_module_or_dict (str, module or dict, optional): See description for the variable
                in the class' `__init__` function. If given, replace the already loaded
                map with a new one. If not given, the existing one given on class creation
                will be reloaded.
            parse (bool, optional): If set, auto-run `.parse()` on the newly loaded data.

        Notes:
            This will both (re)load the data and parse it into a new map structure, replacing any
            existing one. The valid mapstructure is:
            ::

                {
                    "map": <str>,
                    "zcoord": <int or str>, # optional
                    "legend": <dict>,       # optional
                    "prototypes": <dict>    # optional
                    "options": <dict>       # optional
                }

        """
        if not map_module_or_dict:
            map_module_or_dict = self.map_module_or_dict

        mapdata = {}
        if isinstance(map_module_or_dict, dict):
            # map-structure provided directly
            mapdata = map_module_or_dict
        else:
            # read from contents of module
            mod = mod_import(map_module_or_dict)
            mapdata_list = variable_from_module(mod, "XYMAP_DATA_LIST")
            if mapdata_list and self.Z:
                # use the stored Z value to figure out which map data we want
                mapping = {mapdata.get("zcoord") for mapdata in mapdata_list}
                mapdata = mapping.get(self.Z, {})

            if not mapdata:
                mapdata = variable_from_module(mod, "XYMAP_DATA")

        if not mapdata:
            raise MapError(
                "No valid XYMAP_DATA or XYMAP_DATA_LIST could be found from "
                f"{map_module_or_dict}."
            )

        # validate
        if any(key for key in mapdata if key not in MAP_DATA_KEYS):
            raise MapError(
                f"Mapdata has keys {list(mapdata)}, but only "
                f"keys {MAP_DATA_KEYS} are allowed."
            )

        for key in mapdata.get("legend", DEFAULT_LEGEND):
            if not key or len(key) > 1:
                if key not in self.legend_key_exceptions:
                    raise MapError(
                        f"Map-legend key '{key}' is invalid: All keys must "
                        "be exactly one character long. Use the node/link's "
                        "`.display_symbol` property to change how it is "
                        "displayed."
                    )
        if "map" not in mapdata or not mapdata["map"]:
            raise MapError("No map found. Add 'map' key to map-data dict.")
        for key, prototype in mapdata.get("prototypes", {}).items():
            if not (is_iter(key) and (2 <= len(key) <= 3)):
                raise MapError(
                    f"Prototype override key {key} is malformed: It must be a "
                    "coordinate (X, Y) for nodes or (X, Y, direction) for links; "
                    "where direction is a supported direction string ('n', 'ne', etc)."
                )

        # store/update result
        self.Z = mapdata.get("zcoord", self.Z)
        self.mapstring = mapdata["map"]
        self.prototypes = mapdata.get("prototypes", {})
        self.mobile_prototypes = mapdata.get("mobile_prototypes", {})
        self.item_prototypes = mapdata.get("item_prototypes", {})
        self.options = mapdata.get("options", {})

        # merge the custom legend onto the default legend to allow easily
        # overriding only parts of it
        self.legend = {
            **DEFAULT_LEGEND,
            **map_module_or_dict.get("legend", DEFAULT_LEGEND),
        }

        # initialize any prototypes on the legend entities
        for char, node_or_link_class in self.legend.items():
            prototype = node_or_link_class.prototype
            if not prototype or isinstance(prototype, dict):
                # nothing more to do
                continue
            # we need to load the prototype dict onto each for ease of access. Note that
            proto = protlib.search_prototype(
                prototype, require_single=True, no_db=_NO_DB_PROTOTYPES
            )[0]
            node_or_link_class.prototype = proto

    def spawn_mobiles(self, xy=("*", "*"), nodes=None):
        """
        Convert mobiles of this XYMap into actual in-game mobiles by spawning their related
        prototypes. It's possible to only spawn a specific mobile by specifying the node.

        Args:
            xy (tuple, optional): An (X,Y) coordinate. `'*'` acts as a wildcard.
        """
        x, y = xy
        wildcard = "*"
        if not nodes:
            nodes = sorted(self.node_index_map.values(), key=lambda n: (n.Z, n.Y, n.X))

        for node in nodes:
            if (x in (wildcard, node.X)) and (y in (wildcard, node.Y)):
                filtered_mobs = {
                    key: value
                    for key, value in self.mobile_prototypes.items()
                    if value["location"] == (node.X, node.Y)
                }
                node.spawn_mobiles(filtered_mobs)
