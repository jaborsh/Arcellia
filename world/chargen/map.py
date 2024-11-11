CHARGEN_MAP = r"""
 + 0
   
 0 #

 + 0
"""

PROTOTYPES = {
    (0, 0): {
        "key": "|wArcellia - Sanctum of Arrival|n",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "desc": "",
        "locks": "appearance:false()",
    },
}

XYMAP_DATA = {
    "zcoord": "chargen",
    "map": CHARGEN_MAP,
    "prototypes": PROTOTYPES,
}

XYMAP_DATA_LIST = [XYMAP_DATA]
