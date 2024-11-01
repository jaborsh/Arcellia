from evennia.commands.default import system


class CmdShutdown(system.CmdShutdown):
    """
    Syntax: shutdown [announcement]

    Gracefully shut down both Server and Portal.
    """

    key = "shutdown"
    help_category = "System"
