from world.xyzgrid import xyzmap_legend
from world.zones.grovena.room_prototypes import GROVENA_ROOMS

GROVENA_MAP = r"""
 + 0

 1 #
   |
 0 T

 + 0
"""


class AncientGateToMiredBeach(xyzmap_legend.MapTransitionNode):
    target_map_xyz = (0, 5, "mired beach")


LEGEND = {"T": AncientGateToMiredBeach}

XYMAP_DATA_MIRED_BEACH = {
    "zcoord": "grovena",
    "map": GROVENA_MAP,
    "legend": LEGEND,
    "prototypes": GROVENA_ROOMS,
}

XYMAP_DATA_LIST = [XYMAP_DATA_MIRED_BEACH]
