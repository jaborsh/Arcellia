from evennia.commands.default import admin


class CmdBan(admin.CmdBan):
    """
    Usage: ban [<name or ip> [:reason]]

    Ban an account from the server.

    Without any arguments, this shows a list of active bans.

    This command bans a user from accessing the game. Supply an optional reason
    to be able to later remember why the ban was put in place.

    It is often preferable to ban an account from the server than to delete an
    account with accounts/delete. If banned by name, that account can no longer
    be logged into.

    IP address banning allows blocking all access from a specific address or
    subnet. Use an asterisk (*) as a wildcard.

    Examples:
      ban thomas
      ban/ip 127.0.0.1
      ban/ip 127.0.0.*
      ban/ip 127.0.*.*

    A single IP filter can be easy to circumvent by changing computers or
    requesting a new IP address. Setting a wide IP block filter with wildcards
    might be tempting, but remember that it may also accidentally block
    innocent users.
    """

    locks = "cmd:perm(Developer)"


class CmdUnban(admin.CmdUnban):
    """
    Usage: unban <banid>

    This will clear an account name/ip ban previously set with the ban command.
    Use this command without an argument to view a numbered list of bans. Use
    the numbers in this list to select which one to unban.
    """

    locks = "cmd:perm(Developer)"


class CmdBoot(admin.CmdBoot):
    """
    Usage: boot[/switches] <target> [:reason]

    Switches:
      quiet - Silently boot without informing the account.
      sid   - Boot by session id instead of name or dbref.

    Boot an object from the server. If a reason is supplied, it will be echoed
    to the user unless /quiet is set.
    """

    locks = "cmd:perm(Developer)"
