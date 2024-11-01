"""
Copy attribute command module.
"""

from evennia.commands.default import building


class CmdCpAttr(building.CmdCpAttr):
    """
    Syntax: cpattr[/switch] <obj>/<attr> = <obj1>/<attr1> [,<obj2>/<attr2>,<obj3>/<attr3>,...]
            cpattr[/switch] <obj>/<attr> = <obj1> [,<obj2>,<obj3>,...]
            cpattr[/switch] <attr> = <obj1>/<attr1> [,<obj2>/<attr2>,<obj3>/<attr3>,...]
            cpattr[/switch] <attr> = <obj1>[,<obj2>,<obj3>,...]

    Switches:
        move - delete the attribute from the source object after copying.

    Example:
      - cpattr coolness = Anna/chillout, Anna/nicety, Tom/nicety
            copies the coolness attribute (defined on yourself), to attributes
            on Anna and Tom.

    Copy the attribute one object to one or more attributes on another object.
    If you don't supply a source object, yourself is used.
    """

    key = "cpattr"
    aliases = ["copyattribute", "copyattr"]
