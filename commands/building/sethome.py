"""
Set home command module.
"""

from evennia.commands.default import building


class CmdSetHome(building.CmdSetHome):
    """
    Syntax: sethome <obj> [= <home_location>]
            sethome <obj>

    The "home" location is a "safety" location for objects; they
    will be moved there if their current location ceases to exist. All
    objects should always have a home location for this reason.
    It is also a convenient target of the "home" command.

    If no location is given, just view the object's home location.
    """

    key = "sethome"
