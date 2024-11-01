from commands.command import Command


class CmdSetPassword(Command):
    """
    Syntax: setpass <account> <password>

    Set an account's password.
    """

    key = "setpass"
    aliases = ["setpassword"]
    locks = "cmd:perm(Developer)"
    help_category = "Developer"
