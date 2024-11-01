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

    This command allows the player to change their account password. It prompts the player
    to enter their current password, then their new password. The new password is validated
    to ensure it meets the account's password requirements. If the password change is
    successful, the account's password is updated and saved.
    """

    key = "password"
    locks = "cmd:pperm(Player)"
    help_category = "Account"
    account_caller = True

    def func(self):
        account = self.account

        def get_input(prompt):
            return (yield prompt)

        def validate_password(password):
            if not password:
                self.msg("Password change aborted.")
                return False
            return True

        def change_password():
            oldpass = yield from get_input("Enter your password:")
            if not validate_password(oldpass):
                return

            if not account.check_password(oldpass):
                self.msg("The specified password is incorrect.")
                return

            newpass = yield from get_input("Enter your new password:")
            if not validate_password(newpass):
                return

            validated, error = account.validate_password(newpass)
            if not validated:
                errors = [
                    e for suberror in error.messages for e in error.messages
                ]
                self.msg("\n".join(errors))
                return

            account.set_password(newpass)
            account.save()
            self.msg("Password changed.")
            logger.log_sec(
                f"Password Changed: {account} (IP: {self.session.address})."
            )

        yield from change_password()
