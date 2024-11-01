"""
Command module containing the CmdAccess command.
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
        """Load the permission groups and display the caller's access."""
        caller = self.caller

        # Validate that the caller has an associated account
        account = getattr(caller, "account", None)
        if account is None:
            self._send_error("Caller does not have an associated account.")
            return

        # Retrieve the permission hierarchy from settings
        hierarchy_full = getattr(settings, "PERMISSION_HIERARCHY", [])
        if not hierarchy_full:
            self._send_error("Permission hierarchy is not defined in settings.")
            return

        # Determine permissions based on superuser status
        if account.is_superuser:
            character_permissions = account_permissions = "<Superuser>"
        else:
            character_permissions = self._get_permissions(
                caller.permissions.all()
            )
            account_permissions = self._get_permissions(
                account.permissions.all()
            )

        # Build the permission hierarchy string
        permission_hierarchy = ", ".join(hierarchy_full)

        # Construct the access message
        access_message = (
            f"\n|wPermission Hierarchy|n (climbing):\n {permission_hierarchy}\n"
            f"\n|wYour Access|n:"
            f"\n  Character |c{caller.key}|n: {character_permissions}"
        )

        # Append account permissions if available
        access_message += (
            f"\n  Account |c{account.key}|n: {account_permissions}"
        )

        # Send the constructed message to the caller
        caller.msg(access_message)

    def _get_permissions(self, permissions_queryset):
        """
        Convert a queryset of permissions into a comma-separated string.

        Args:
            permissions_queryset (QuerySet): A Django QuerySet of permission objects.

        Returns:
            str: Comma-separated permission names or "<None>" if empty.
        """
        permissions = [perm.name for perm in permissions_queryset]
        return ", ".join(permissions) if permissions else "<None>"

    def _send_error(self, message):
        """
        Send an error message to the caller.

        Args:
            message (str): The error message to send.
        """
        self.caller.msg(f"|rError: {message}|n")
