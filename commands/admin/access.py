"""
Command module containing the CmdAccess command.
"""

from django.conf import settings

from commands.command import Command


class CmdAccess(Command):
    """
    Display caller's access and permission groups.

    Usage:
        access

    Shows permission groups and caller's access level, including
    both character and account permissions.

    Returns:
        None: Sends formatted message to caller.
    """

    key = "access"
    aliases = ["groups", "hierarchy"]
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        """Execute the access command logic."""
        caller = self.caller
        account = getattr(caller, "account", None)

        if not self._validate_requirements(account):
            return

        hierarchy = self._get_hierarchy()
        char_perms, acc_perms = self._get_permission_strings(caller, account)

        self.caller.msg(
            f"\n|wPermission Hierarchy|n (climbing):\n {hierarchy}\n"
            f"\n|wYour Access|n:"
            f"\n  Character |c{caller.key}|n: {char_perms}"
            f"\n  Account |c{account.key}|n: {acc_perms}"
        )

    def _validate_requirements(self, account):
        """
        Validate command requirements.

        Args:
            account: The account object to validate

        Returns:
            bool: True if valid, False otherwise
        """
        if account is None:
            self._send_error("Caller does not have an associated account.")
            return False
        return True

    def _get_hierarchy(self):
        """Get the permission hierarchy string."""
        hierarchy = getattr(settings, "PERMISSION_HIERARCHY", [])
        if not hierarchy:
            self._send_error("Permission hierarchy is not defined in settings.")
            return ""
        return ", ".join(hierarchy)

    def _get_permission_strings(self, caller, account):
        """
        Get formatted permission strings for character and account.

        Args:
            caller: The character object
            account: The account object

        Returns:
            tuple: Character and account permission strings
        """
        if account.is_superuser:
            return "<Superuser>", "<Superuser>"

        return (
            self._get_permissions(caller.permissions.all()),
            self._get_permissions(account.permissions.all()),
        )

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
