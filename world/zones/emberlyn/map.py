from world.xyzgrid import xyzmap_legend
from world.zones.emberlyn.room_prototypes import EMBERLYN_ROOMS

EMBERLYN_MAP = r"""
 + 0

 1 #
   |
 0 T

 + 0
"""


class AncientGateToEmberlynBeach(xyzmap_legend.MapTransitionNode):
    target_map_xyz = (1, 5, "emberlyn beach")


LEGEND = {"T": AncientGateToEmberlynBeach}

XYMAP_DATA_EMBERLYN = {
    "zcoord": "emberlyn",
    "map": EMBERLYN_MAP,
    "legend": LEGEND,
    "prototypes": EMBERLYN_ROOMS,
}

XYMAP_DATA_LIST = [XYMAP_DATA_EMBERLYN]
