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
            "|wpuppet/character",
            "|wlocation",
        )

        for sess in sessions:
            char = account.get_puppet(sess)
            host = (
                sess.address[0]
                if isinstance(sess.address, tuple)
                else sess.address
            )

            table.add_row(
                str(sess.sessid),
                str(sess.protocol_key),
                host,
                str(char) if char else "None",
                str(char.location) if char else "N/A",
            )

        self.msg(f"|wYour current session(s):|n\n{table}")
