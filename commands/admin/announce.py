"""
Command module containing CmdAnnounce.
"""

from django.conf import settings
from evennia.server.sessionhandler import SESSIONS

from commands.command import Command
from utils.text import wrap


class CmdAnnounce(Command):
    """
    Command to announce a message to all players.

    Usage:
        announce <message>

    This command allows administrators to send an announcement to all players
    currently connected to the game. The message should be provided as an argument
    after the command. The announcement will be displayed to all players in a
    formatted manner.

    Example:
        > announce Welcome to the game!

    This will send the message "Welcome to the game!" as an announcement to all
    connected players.
    """

    key = "announce"
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        if not self.args:
            self.caller.msg("Syntax: announce <message>")
            return

        message = wrap(self.args, text_width=63, align="c", pre_text="  ")
        announcement = (
            "\n|C  .:*~*:._.:*~*:._.:*~ |r{SERVERNAME} Announcement |C~*:._.:*~*:._.:*~*:.|n"
            "\n\n|Y{message}|n"
            "\n\n|C  .:*~*:._.:*~*:._.:*~                       ~*:._.:*~*:._.:*~*:.|n"
        ).format(SERVERNAME=settings.SERVERNAME, message=message)

        SESSIONS.announce_all(announcement)
