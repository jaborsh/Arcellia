from evennia.commands.default.account import CmdQuell as EvenniaCmdQuell


class CmdQuell(EvenniaCmdQuell):
    """
    Syntax: quell
            unquell

    Normally the permission level of the account is used when puppeting a
    character/object to determine access. Queeling will switch the lock system
    to make use of the puppeted object's permissions instead. This is useful
    mainly for testing.

    Hierarchical permission quelling only works downwards, thus an account
    cannot use a higher-permission character to escalate their permission
    level.

    Use 'unquell' to revert to normal permissions.
    """

    locks = "cmd:pperm(Developer)"
    help_category = "Developer"
