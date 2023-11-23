"""
At_initial_setup module template

Custom at_initial_setup method. This allows you to hook special
modifications to the initial server startup process. Note that this
will only be run once - when the server starts up for the very first
time! It is called last in the startup process and can thus be used to
overload things that happened before it.

The module must contain a global function at_initial_setup().  This
will be called without arguments. Note that tracebacks in this module
will be QUIETLY ignored, so make sure to check it well to make sure it
does what you expect it to.

"""

from evennia.contrib.grid.xyzgrid.launchcmd import (
    _option_add,
    _option_init,
)
from evennia.contrib.grid.xyzgrid.xyzgrid import get_xyzgrid


def at_initial_setup():
    _option_init()  # xyzgrid init
    _option_add("world.valaria.castle.map")
    grid = get_xyzgrid()
    grid.spawn(xyz=("*", "*", "*"))
