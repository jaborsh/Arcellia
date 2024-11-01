"""
Command module containing CmdQuit.
"""

from commands.command import Command


class CmdQuit(Command):
    """
    Command class for quitting the game.

    This command allows the player to quit the game. It provides options to quit
    the current session or all sessions associated with the player's account.

    Usage:
      quit [all]

    Switches:
      all - Quit all sessions

    Example usage:
      quit        - Quit the current session
      quit all    - Quit all sessions
    """

    key = "quit"
    switch_options = ("all",)
    locks = "cmd:all()"
    help_category = "Account"
    account_caller = True

    def func(self):
        """Hook function"""
        account = self.account
        session = self.session

        if "all" in self.switches:
            self.quit_all_sessions(account, session)
        else:
            self.quit_current_session(account, session)

    def quit_all_sessions(self, account, session):
        """Quit all sessions"""
        account.msg(
            "|RQuitting|n all sessions. Hope to see you soon again.",
            session=session,
        )
        reason = "quit/all"
        for session in account.sessions.all():
            account.disconnect_session_from_account(session, reason)

    def quit_current_session(self, account, session):
        """Quit the current session"""
        nsess = account.sessions.count()
        reason = "quit"

        if nsess == 2:
            message = "|RQuitting|n. One session is still connected."
        elif nsess > 2:
            message = f"|RQuitting|n. {nsess - 1} sessions are still connected."
        else:
            message = "|RQuitting|n. Hope to see you again, soon."

        account.msg(message, session=session)
        account.disconnect_session_from_account(session, reason)
