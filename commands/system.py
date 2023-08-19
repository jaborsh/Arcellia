from evennia.commands.default import building


class CmdObjects(building.CmdObjects):
    """
    Usage: objects [<nr>]

    Gives statictics on objects in database as well as a list of <nr> latest
    objects in database. If not given, <nr> defaults to 10.
    """

    key = "objects"
    aliases = ["objs"]
    help_category = "System"
