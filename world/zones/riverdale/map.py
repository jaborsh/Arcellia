from world.zones.riverdale.room_prototypes import RIVERDALE_ROOMS

RIVERDALE = r"""
 + 0 1 2 3 4
 
 3 #-#-#
     | |
 2   | #
     |
 1 #-#-#-#-#
       |     
 0     #

 + 0 1 2 3 4
"""


XYMAP_DATA_OOC = {
    "zcoord": "riverdale",
    "map": RIVERDALE,
    "prototypes": RIVERDALE_ROOMS,
}

XYMAP_DATA_LIST = [XYMAP_DATA_OOC]
