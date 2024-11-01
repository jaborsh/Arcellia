from evennia.commands.default import system


class CmdReload(system.CmdReload):
    """
    Syntax: reload [reason]

    This restarts the server. The Portal is not
    affected. Non-persistent scripts will survive a reload (use
    reset to purge) and at_reload() hooks will be called.
    """

    key = "reload"
    aliases = ["restart"]
    help_category = "System"
