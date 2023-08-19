from evennia.commands.default import account, admin, building

from commands.command import Command

__all__ = (
    "CmdBan",
    "CmdUnban",
    "CmdBoot",
    "CmdListCmdSets",
    "CmdQuell",
    "CmdScripts",
    "CmdSetPassword",
    "CmdSetPerm",
)


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


class CmdListCmdSets(building.CmdListCmdSets):
    """
    Usage: cmdsets <obj>

    This displays all cmdsets assigned to a user. Defaults to yourself.
    """

    key = "cmdsets"
    locks = "cmd:perm(Developer)"
    help_category = "Admin"


class CmdQuell(account.CmdQuell):
    """
    Usage: quell
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
    help_category = "Admin"


class CmdScripts(building.CmdScripts):
    """
    Usage: script[/switches] [script-#dbref, key, script.path]
           script[/start||stop] <obj> = [<script.path or script-key>]

    Switches:
        start - start/unpause an existing script's timer.
        stop - stops an existing script's timer
        pause - pause a script's timer
        delete - deletes script. This will also stop the timer as needed

    Examples:
        script                            - list all scripts
        script foo.bar.Script             - create a new global Script
        script/pause foo.bar.Script       - pause global script
        script scriptname|#dbref          - examine named existing global script
        script/delete #dbref[-#dbref]     - delete script or range by #dbref

        script myobj =                    - list all scripts on object
        script myobj = foo.bar.Script     - create and assign script to object
        script/stop myobj = name|#dbref   - stop named script on object
        script/delete myobj = name|#dbref - delete script on object
        script/delete myobj =             - delete ALL scripts on object

    When given with an `<obj>` as left-hand-side, this creates and
    assigns a new script to that object. Without an `<obj>`, this
    manages and inspects global scripts.

    If no switches are given, this command just views all active
    scripts. The argument can be either an object, at which point it
    will be searched for all scripts defined on it, or a script name
    or #dbref. For using the /stop switch, a unique script #dbref is
    required since whole classes of scripts often have the same name.

    Use the `script` build-level command for managing scripts attached to
    objects.
    """

    key = "scripts"
    aliases = ["script"]
    locks = "cmd:perm(Developer)"
    help_category = "Admin"


class CmdSetPassword(Command):
    """
    Usage: setpass <account> <password>

    Set an account's password.
    """

    key = "setpass"
    aliases = ["setpassword"]
    locks = "cmd:perm(Developer)"
    help_category = "Admin"


class CmdSetPerm(admin.CmdPerm):
    """
    Usage: setperm[/switch] <object> [=<permission>[,<permission>,...]]
           setperm[/switch] *<account> [=<permission>[,<permission>,...]]

    Switches: account - set the permission on an account
              del     - delete the permission from the object

    This command manages individual permission strings on an object or account.
    If no permission is given, list all permissions.
    """

    key = "setperm"
    aliases = ["perm"]
    locks = "cmd:perm(Developer)"
