from evennia.commands.default.admin import CmdBoot as EvenniaCmdBoot


class CmdBoot(EvenniaCmdBoot):
    """
    Syntax: boot[/switches] <target> [:reason]

    Switches:
      quiet - Silently boot without informing the account.
      sid   - Boot by session id instead of name or dbref.

    Boot an object from the server. If a reason is supplied, it will be echoed
    to the user unless /quiet is set.
    """

    locks = "cmd:pperm(Developer)"
    help_category = "Developer"
