from world.zones.ooc.room_prototypes import ROOM_PROTOTYPES

OOC_MAP = r"""
 + 0
     
 0 #

 + 0
"""


XYMAP_DATA_OOC = {
    "zcoord": "ooc",
    "map": OOC_MAP,
    "prototypes": ROOM_PROTOTYPES,
}

XYMAP_DATA_LIST = [XYMAP_DATA_OOC]
