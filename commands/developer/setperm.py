from evennia.commands.default.admin import CmdPerm as EvenniaCmdPerm


class CmdSetPerm(EvenniaCmdPerm):
    """
    Syntax: setperm[/switch] <object> [=<permission>[,<permission>,...]]
            setperm[/switch] *<account> [=<permission>[,<permission>,...]]

    Switches: account - set the permission on an account
              del     - delete the permission from the object

    This command manages individual permission strings on an object or account.
    If no permission is given, list all permissions.
    """

    key = "setperm"
    aliases = ["perm"]
    locks = "cmd:perm(Developer)"
    help_category = "Developer"
