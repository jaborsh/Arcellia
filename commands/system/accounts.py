from evennia.commands.default import system


class CmdAccounts(system.CmdAccounts):
    """
    Syntax: accounts [nr]
            accounts/delete <name or #id> [: reason]

    Switches:
      delete    - delete an account from the server

    By default, lists statistics about the Accounts registered with the game.
    It will list the <nr> amount of latest registered accounts
    If not given, <nr> defaults to 10.
    """

    key = "accounts"
    aliases = ["account"]
    help_category = "System"
