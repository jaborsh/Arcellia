from world.xyzgrid import xyzmap_legend
from world.zones.emberlyn.emberlyn_beach.mob_prototypes import (
    EMBERLYN_BEACH_MOBS,
)
from world.zones.emberlyn.emberlyn_beach.room_prototypes import (
    EMBERLYN_BEACH_ROOMS,
)

EMBERLYN_BEACH = r"""
 + 0 1
   
 6 T
   |
 5 #
   |
 4 #
   |
 3 #-#
     |
 2 #-#
   |
 1 #
   |
 0 #

 + 0 1
"""


class AncientGateToEmberlyn(xyzmap_legend.MapTransitionNode):
    target_map_xyz = (0, 1, "emberlyn")


LEGEND = {"T": AncientGateToEmberlyn}

XYMAP_DATA_EMBERLYN_BEACH = {
    "zcoord": "emberlyn beach",
    "map": EMBERLYN_BEACH,
    "legend": LEGEND,
    "prototypes": EMBERLYN_BEACH_ROOMS,
    "mob_prototypes": EMBERLYN_BEACH_MOBS,
}

XYMAP_DATA_LIST = [XYMAP_DATA_EMBERLYN_BEACH]