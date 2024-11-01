"""
Command module containing CmdSessions.
"""

from commands.command import Command


class CmdSessions(Command):
    """
    Command to display the current sessions of the account.

    Usage:
      sessions

    This command displays information about the current sessions of the account.
    It shows the session ID, protocol, host, puppet/character, and location for each session.

    Returns:
        A styled table containing the session information.
    """

    key = "sessions"
    locks = "cmd:all()"
    help_category = "Account"
    account_caller = True

    def func(self):
        """Implement function"""
        account = self.account
        sessions = sorted(account.sessions.all(), key=lambda x: x.sessid)

        table = self.styled_table(
            "|wsessid",
            "|wprotocol",
            "|whost",
            "|wcharacter",
            "|wlocation",
            maxwidth=80,
        )

        for sess in sessions:
            table.add_row(*self.get_session_info(sess))

        self.msg(f"|wYour current session(s):|n\n{table}")

    def get_session_info(self, session):
        """
        Retrieve information about a session.

        Args:
            session: The session to retrieve information for.

        Returns:
            A tuple containing the session ID, protocol, host, puppet/character, and location.
        """
        char = session.get_puppet()
        host = getattr(session.address, "0", session.address)
        return (
            str(session.sessid),
            str(session.protocol_key),
            host,
            str(char) if char else "None",
            str(char.location) if char else "N/A",
        )
