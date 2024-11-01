"""
Tag command module.
"""

from evennia.commands.default import building


class CmdTag(building.CmdTag):
    """
    Syntax: tag[/del] <obj> [= <tag>[:<category>]]
            tag/search <tag>[:<category]

    Switches:
        search - return all objects with a given Tag
        del - remove the given tag. If no tag is specified,
              clear all tags on object.

    Manipulates and lists tags on objects. Tags allow for quick
    grouping of and searching for objects.  If only <obj> is given, list all
    tags on the object.  If /search is used, list objects with the given tag.
    The category can be used for grouping tags themselves, but it should be
    used with restrain - tags on their own are usually enough to for most
    grouping schemes.
    """

    key = "tag"
    aliases = ["tags"]
