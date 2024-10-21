from world.xyzgrid import xyzmap_legend
from world.zones.grovena.mired_beach.mob_prototypes import MIRED_BEACH_MOBS
from world.zones.grovena.mired_beach.room_prototypes import MIRED_BEACH_ROOMS

MIRED_BEACH = r"""
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


class AncientGateToGrovena(xyzmap_legend.MapTransitionNode):
    target_map_xyz = (0, 1, "grovena")


LEGEND = {"T": AncientGateToGrovena}

XYMAP_DATA_MIRED_BEACH = {
    "zcoord": "mired beach",
    "map": MIRED_BEACH,
    "legend": LEGEND,
    "prototypes": MIRED_BEACH_ROOMS,
    "mob_prototypes": MIRED_BEACH_MOBS,
}

XYMAP_DATA_LIST = [XYMAP_DATA_MIRED_BEACH]
