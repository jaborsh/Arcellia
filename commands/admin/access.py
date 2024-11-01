"""
Command module containing CmdAccess.
"""

from django.conf import settings

from commands.command import Command


class CmdAccess(Command):
    """
    Command class for displaying the caller's access and permission groups.

    Usage:
      access

    This command displays the permission groups and the caller's access level.
    If the caller is a superuser, it displays "<Superuser>". Otherwise, it
    displays the caller's permissions for both the character and the account.
    """

    key = "access"
    aliases = ["groups", "hierarchy"]
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        """Load the permission groups and display the caller's access"""
        caller = self.caller
        hierarchy_full = settings.PERMISSION_HIERARCHY

        if caller.account.is_superuser:
            cperms = pperms = "<Superuser>"
        else:
            cperms = ", ".join(caller.permissions.all())
            pperms = ", ".join(caller.account.permissions.all())

        string = (
            "\n|wPermission Hierarchy|n (climbing):\n %s\n"
            "\n|wYour access|n:"
            "\n  Character |c%s|n: %s"
            % (", ".join(hierarchy_full), caller.key, cperms)
        )

        if hasattr(caller, "account"):
            string += "\n  Account |c%s|n: %s" % (caller.account.key, pperms)

        caller.msg(string)
