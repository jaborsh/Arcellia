from typeclasses.rooms import MapNode

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

CREATION_ROOM_PARENT = {"typeclass": "world.chargen.rooms.CreationRoom"}
CREATION_EXIT_PARENT = {"typeclass": "typeclasses.exits.XYExit"}

for key, prot in PROTOTYPES.items():
    if len(key) == 2:
        prot["prototype_parent"] = CREATION_ROOM_PARENT
    else:
        prot["prototype_parent"] = CREATION_EXIT_PARENT

LEGEND = {"#": MapNode}

XYMAP_DATA = {
    "zcoord": "chargen",
    "legend": LEGEND,
    "map": CHARGEN_MAP,
    "prototypes": PROTOTYPES,
}
