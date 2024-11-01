"""
Map command module.
"""

from world.xyzgrid import xyzcommands


class CmdMap(xyzcommands.CmdMap):
    """
    Syntax: map [Zcoord]
            map list

    Show a map of an area.
    """

    locks = "cmd:perm(Builder)"
    help_category = "Building"
