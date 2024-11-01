"""
Examine command module.
"""

from evennia.commands.default import building


class CmdExamine(building.CmdExamine):
    """
    Syntax: examine [<object>[/attrname]]
            examine [*<account>[/attrname]]

    Switch:
        account - examine an Account (same as adding *)
        object - examine an Object (useful when OOC)
        script - examine a Script
        channel - examine a Channel

    The examine command shows detailed game info about an
    object and optionally a specific attribute on it.
    If object is not specified, the current location is examined.
    """

    key = "examine"
    aliases = ["ex", "exam"]
