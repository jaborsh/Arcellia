"""
Command module containing the CmdAnnounce command.
"""

from django.conf import settings
from evennia.server.sessionhandler import SESSIONS

from commands.command import Command
from utils.text import wrap


class CmdAnnounce(Command):
    """
    Command to announce a message to all connected players.

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
    TEXT_WIDTH = 63
    PRE_TEXT = "  "
    ANNOUNCEMENT_TEMPLATE = (
        "\n|C  .:*~*:._.:*~*:._.:*~ |r{server_name} Announcement |C~*:._.:*~*:._.:*~*:.|n"
        "\n\n|Y{message}|n"
        "\n\n|C  .:*~*:._.:*~*:._.:*~                       ~*:._.:*~*:._.:*~*:.|n\n"
    )

    def func(self):
        """Process the announce command and send the announcement to all players."""
        if not self.args.strip():
            self._send_syntax_error()
            return

        message = self._format_message(self.args)
        announcement = self._build_announcement(message)

        if not self._validate_announcement(announcement):
            return

        self._send_announcement(announcement)

    def _format_message(self, raw_message: str) -> str:
        """
        Format the raw message using the wrap utility.

        Args:
            raw_message (str): The message provided by the administrator.

        Returns:
            str: The formatted message.
        """
        return wrap(
            raw_message,
            text_width=self.TEXT_WIDTH,
            align="c",
            pre_text=self.PRE_TEXT,
        )

    def _build_announcement(self, formatted_message: str) -> str:
        """
        Construct the full announcement string using the template.

        Args:
            formatted_message (str): The formatted message to include in the announcement.

        Returns:
            str: The complete announcement string.
        """
        server_name = getattr(settings, "SERVERNAME", "Server")
        return self.ANNOUNCEMENT_TEMPLATE.format(
            server_name=server_name, message=formatted_message
        )

    def _validate_announcement(self, announcement: str) -> bool:
        """
        Validate that the announcement can be sent.

        Args:
            announcement (str): The announcement string to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        if not SESSIONS:
            self._send_error("No active sessions to send the announcement.")
            return False
        if not announcement.strip():
            self._send_error("Announcement message is empty.")
            return False
        return True

    def _send_announcement(self, announcement: str):
        """
        Send the announcement to all connected sessions.

        Args:
            announcement (str): The announcement string to send.
        """
        try:
            SESSIONS.announce_all(announcement)
            self.caller.msg("|gAnnouncement sent successfully.|n")
        except Exception as e:
            self._send_error(f"Failed to send announcement: {e}")

    def _send_syntax_error(self):
        """Send a syntax error message to the caller."""
        self.caller.msg("|rSyntax: announce <message>|n")

    def _send_error(self, message: str):
        """
        Send an error message to the caller.

        Args:
            message (str): The error message to send.
        """
        self.caller.msg(f"|rError: {message}|n")
