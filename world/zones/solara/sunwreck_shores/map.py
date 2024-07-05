from world.zones.solara.sunwreck_shores.mob_prototypes import MOB_PROTOTYPES
from world.zones.solara.sunwreck_shores.room_prototypes import ROOM_PROTOTYPES

SUNWRECK_SHORES_MAP = r"""
 + 0 1 2 3 4 5
 
 9       #
         |
 8       #
         |
 7       #
         |
 6 # #-#-#
   | |   
 5 #-#-#-#-#
           |
 4         #-# 
           | |   
 3       #-#-#
           |
 2         #
           |
 1         #
           |
 0         #

 + 0 1 2 3 4 5
"""

XYMAP_DATA = {
    "zcoord": "sunwreck_shores",
    "map": SUNWRECK_SHORES_MAP,
    "prototypes": ROOM_PROTOTYPES,
    "mob_prototypes": MOB_PROTOTYPES,
}
