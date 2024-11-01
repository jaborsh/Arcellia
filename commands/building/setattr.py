"""
Set attribute command module.
"""

from evennia.commands.default import building


class CmdSetAttribute(building.CmdSetAttribute):
    """
    Syntax: set[/switch] <obj>/<attr>[:category] = <value>
            set[/switch] <obj>/<attr>[:category] =            # delete attribute
            set[/switch] <obj>/<attr>[:category]              # view attribute
            set[/switch] *<account>/<attr>[:category] = <value>

    Switch:
        edit: Open the line editor (string values only)
        script: If we're trying to set an attribute on a script
        channel: If we're trying to set an attribute on a channel
        account: If we're trying to set an attribute on an account
        room: Setting an attribute on a room (global search)
        exit: Setting an attribute on an exit (global search)
        char: Setting an attribute on a character (global search)
        character: Alias for char, as above.

    Example:
        set self/foo = "bar"
        set/delete self/foo
        set self/foo = $dbref(#53)

    Sets attributes on objects. The second example form above clears a
    previously set attribute while the third form inspects the current value of
    the attribute (if any). The last one (with the star) is a shortcut for
    operating on a player Account rather than an Object.

    If you want <value> to be an object, use $dbef(#dbref) or
    $search(key) to assign it. You need control or edit access to
    the object you are adding.

    The most common data to save with this command are strings and
    numbers. You can however also set Python primitives such as lists,
    dictionaries and tuples on objects (this might be important for
    the functionality of certain custom objects).  This is indicated
    by you starting your value with one of |c'|n, |c"|n, |c(|n, |c[|n
    or |c{ |n.

    Once you have stored a Python primitive as noted above, you can include
    |c[<key>]|n in <attr> to reference nested values in e.g. a list or dict.

    Remember that if you use Python primitives like this, you must
    write proper Python syntax too - notably you must include quotes
    around your strings or you will get an error.
    """

    key = "set"
    aliases = ["setattribute", "setattrib", "setattr"]
