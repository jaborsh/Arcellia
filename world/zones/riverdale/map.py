from world.zones.riverdale.mob_prototypes import RIVERDALE_MOBS
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


XYMAP_DATA_RIVERDALE = {
    "zcoord": "riverdale",
    "map": RIVERDALE,
    "prototypes": RIVERDALE_ROOMS,
    "mob_prototypes": RIVERDALE_MOBS,
}

XYMAP_DATA_LIST = [XYMAP_DATA_RIVERDALE]
