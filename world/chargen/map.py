CREATION_ROOM_PARENT = {
    "prototype_key": "xyz_room",
    "typeclass": "world.chargen.rooms.CreationRoom",
}

CHARGEN_MAP = r"""
 + 0
   
 0 #

 + 0
"""

PROTOTYPES = {
    (0, 0): {
        "prototype_parent": CREATION_ROOM_PARENT,
        "typeclass": "world.chargen.rooms.CreationRoom",
        "key": "|wArcellia - Sanctum of Arrival|n",
        "desc": "",
    },
}

XYMAP_DATA = {
    "zcoord": "chargen",
    "map": CHARGEN_MAP,
    "prototypes": PROTOTYPES,
}

XYMAP_DATA_LIST = [XYMAP_DATA]
