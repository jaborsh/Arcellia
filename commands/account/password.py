"""
Command module containing CmdPassword.
"""

from commands.command import Command
from server.conf import logger


class CmdPassword(Command):
    """
    Command to change the password of an account.

    Usage:
      password

    This command allows the player to change their account password.
    """

    key = "password"
    locks = "cmd:pperm(Player)"
    help_category = "Account"
    account_caller = True

    def _get_input(self, prompt):
        return (yield prompt)

    def _validate_input(self, password, is_new=False):
        if not password:
            self.msg("Password change aborted.")
            return False

        if is_new:
            validated, error = self.account.validate_password(password)
            if not validated:
                self.msg(
                    "\n".join(
                        [
                            e
                            for suberror in error.messages
                            for e in error.messages
                        ]
                    )
                )
                return False
        return True

    def func(self):
        account = self.account

        # Get and validate current password
        oldpass = yield from self._get_input("Enter your password:")
        if not self._validate_input(oldpass):
            return

        if not account.check_password(oldpass):
            self.msg("The specified password is incorrect.")
            return

        # Get and validate new password
        newpass = yield from self._get_input("Enter your new password:")
        if not self._validate_input(newpass, is_new=True):
            return

        # Confirm new password
        confirm_pass = yield from self._get_input("Confirm your new password:")
        if not self._validate_input(confirm_pass):
            return

        if newpass != confirm_pass:
            self.msg("Passwords do not match. Password change aborted.")
            return

        # Update password
        account.set_password(newpass)
        account.save()
        self.msg("Password changed.")
        logger.log_sec(
            f"Password Changed: {account} (IP: {self.session.address})."
        )
