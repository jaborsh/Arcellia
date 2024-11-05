from world.xyzgrid import xyzmap_legend
from world.zones.emberlyn.emberlyn_catacombs.mob_prototypes import (
    EMBERLYN_CATACOMB_MOBS,
)
from world.zones.emberlyn.emberlyn_catacombs.room_prototypes import (
    EMBERLYN_CATACOMB_ROOMS,
)

EMBERLYN_CATACOMB_MAP = r"""
 + 0 1 2 3 4 5

 7 #-#-#-#-#
   |       |
 6 #       #
   |       |
 5 #       #
   |       |
 4 #       #
   |       |
 3 #       #
   |       |
 2 #       #-C
   |
 1 #
   |
 0 #
 
 + 0 1 2 3 4 5
"""


class EntranceToEmberlynBeach(xyzmap_legend.MapTransitionNode):
    target_map_xyz = (1, 3, "emberlyn beach")


LEGEND = {"C": EntranceToEmberlynBeach}

XYMAP_DATA_EMBERLYN_CATACOMBS = {
    "zcoord": "emberlyn catacombs",
    "map": EMBERLYN_CATACOMB_MAP,
    "legend": LEGEND,
    "prototypes": EMBERLYN_CATACOMB_ROOMS,
    "mob_prototypes": EMBERLYN_CATACOMB_MOBS,
}

XYMAP_DATA_LIST = [XYMAP_DATA_EMBERLYN_CATACOMBS]
