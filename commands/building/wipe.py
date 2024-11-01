"""
Wipe command module.
"""

from evennia.commands.default import building


class CmdWipe(building.CmdWipe):
    """
    Syntax: wipe <object>[/<attr>[/<attr>...]]

    Example:
        wipe box
        wipe box/colour

    Wipes all of an object's attributes, or optionally only those
    matching the given attribute-wildcard search string.
    """

    key = "wipe"
