from world.zones.ooc.room_prototypes import ROOM_PROTOTYPES

OOC_MAP = r"""
 + 0 1 2 3 4

 4      
    
 3 

 2 
 
 1 
     
 0 #

 + 0 1 2 3 4
"""


XYMAP_DATA_OOC = {
    "zcoord": "ooc",
    "map": OOC_MAP,
    "prototypes": ROOM_PROTOTYPES,
}

XYMAP_DATA_LIST = [XYMAP_DATA_OOC]
