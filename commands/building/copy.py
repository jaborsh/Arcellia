"""
Copy command module.
"""

from evennia.commands.default import building


class CmdCopy(building.CmdCopy):
    """
    Syntax: copy <original obj> [= <new name>][;alias;alias...]
            [:<new location>] [,<new name2> ...]

    Create one or more copies of an object. If you don't supply any targets,
    one exact copy of the original object will be created with the name *_copy.
    """

    key = "copy"
