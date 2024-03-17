CREATION_ROOM_PARENT = {"typeclass": "world.chargen.rooms.CreationRoom"}
CREATION_EXIT_PARENT = {"typeclass": "world.xyzgrid.xyzexit.XYZExit"}

CHARGEN_MAP = r"""
 + 0
   
 0 #

 + 0
"""

PROTOTYPES = {
    (0, 0): {
        "key": "|wArcellia - Sanctum of Arrival|n",
        "desc": "",
    },
}


for key, prot in PROTOTYPES.items():
    if len(key) == 2:
        prot["prototype_parent"] = CREATION_ROOM_PARENT
    else:
        prot["prototype_parent"] = CREATION_EXIT_PARENT

XYMAP_DATA = {
    "zcoord": "chargen",
    "map": CHARGEN_MAP,
    "prototypes": PROTOTYPES,
}

XYMAP_DATA_LIST = [XYMAP_DATA]
