"""
Set alias command module.
"""

from evennia.commands.default import building


class CmdSetAlias(building.CmdSetObjAlias):
    """
    Syntax: setalias <obj> [= [alias[,alias,alias,...]]]
            setalias <obj> =
            setalias/category <obj> = [alias[,alias,...]]:<category>

    Switches:
        category - requires ending input with :category, to store the
                 given aliases with the given category.

    Assigns aliases to an object so it can be referenced by more
    than one name. Assign empty to remove all aliases from object. If
    assigning a category, all aliases given will be using this category.

    Observe that this is not the same thing as personal aliases
    created with the 'nick' command! Aliases set with alias are
    changing the object in question, making those aliases usable
    by everyone.
    """

    key = "setalias"
    aliases = []
