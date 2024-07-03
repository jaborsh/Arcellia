"""
Default prototypes for building the XYZ-grid into actual game-rooms.

Add this to mygame/conf/settings/settings.py:

    PROTOTYPE_MODULES += ['evennia.contrib.grid.xyzgrid.prototypes']

The prototypes can then be used in mapping prototypes as

    {'prototype_parent': 'xyz_room', ...}

and/or

    {'prototype_parent': 'xyz_exit', ...}

"""

from django.conf import settings

try:
    room_override = settings.XYZROOM_PROTOTYPE_OVERRIDE
except AttributeError:
    room_override = {}

try:
    exit_override = settings.XYZEXIT_PROTOTYPE_OVERRIDE
except AttributeError:
    exit_override = {}

try:
    mob_override = settings.XYZMOB_PROTOTYPE_OVERRIDE
except AttributeError:
    mob_override = {}

room_prototype = {
    "prototype_key": "xyz_room",
    "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
    "prototype_tags": ("xyzroom",),
    "key": "A room",
    "desc": "An empty room.",
}
room_prototype.update(room_override)

exit_prototype = {
    "prototype_key": "xyz_exit",
    "typeclass": "world.xyzgrid.xyzexit.XYZExit",
    "prototype_tags": ("xyzexit",),
    "desc": "An exit.",
}
exit_prototype.update(exit_override)

mob_prototype = {
    "prototype_key": "xyz_mob",
    "typeclass": "world.xyzgrid.xyzmob.XYZMob",
    "prototype_tags": ("xyzmob",),
    "key": "A mob",
    "desc": "A nondescript mob.",
}
mob_prototype.update(mob_override)

# accessed by the prototype importer
PROTOTYPE_LIST = [room_prototype, exit_prototype, mob_prototype]
