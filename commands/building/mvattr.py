"""
Move attribute command module.
"""

from evennia.commands.default import building


class CmdMvAttr(building.CmdMvAttr):
    """
    Syntax: mvattr[/switch] <obj>/<attr> = <obj1>/<attr1> [,<obj2>/<attr2>,<obj3>/<attr3>,...]
            mvattr[/switch] <obj>/<attr> = <obj1> [,<obj2>,<obj3>,...]
            mvattr[/switch] <attr> = <obj1>/<attr1> [,<obj2>/<attr2>,<obj3>/<attr3>,...]
            mvattr[/switch] <attr> = <obj1>[,<obj2>,<obj3>,...]

    Switches:
      copy - Don't delete the original after moving.

    Move an attribute from one object to one or more attributes on another
    object. If you don't supply a source object, yourself is used.
    """

    key = "mvattr"
    aliases = ["moveattr"]
