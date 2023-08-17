from evennia.server.portal import amp
from evennia.server.sessionhandler import ServerSessionHandler as BaseSessionHandler
from evennia.server.signals import (
    SIGNAL_ACCOUNT_POST_LAST_LOGOUT,
    SIGNAL_ACCOUNT_POST_LOGOUT,
)


class ServerSessionHandler(BaseSessionHandler):
    def disconnect(self, session, reason="", sync_portal=True):
        """
        Called from server side to remove session and inform portal
        of this fact.

        Args:
            session (Session): The Session to disconnect.
            reason (str, optional): A motivation for the disconnect.
            sync_portal (bool, optional): Sync the disconnect to
                Portal side. This should be done unless this was
                called by self.portal_disconnect().

        """
        session = self.get(session.sessid)
        if not session:
            return

        if hasattr(session, "account") and session.account:
            # only log accounts logging off
            nsess = len(self.sessions_from_account(session.account)) - 1
            sreason = " ({})".format(reason) if reason else ""
            string = "Logged out: {account} {address} ({nsessions} sessions(s) remaining){reason}"
            string = string.format(
                reason=sreason,
                account=session.account,
                address=session.address,
                nsessions=nsess,
            )
            session.log(string)

            if nsess == 0:
                SIGNAL_ACCOUNT_POST_LAST_LOGOUT.send(
                    sender=session.account, session=session
                )

        session.at_disconnect(reason)
        SIGNAL_ACCOUNT_POST_LOGOUT.send(sender=session.account, session=session)
        sessid = session.sessid
        if sessid in self and not hasattr(self, "_disconnect_all"):
            del self[sessid]
        if sync_portal:
            # inform portal that session should be closed.
            self.server.amp_protocol.send_AdminServer2Portal(
                session,
                operation=amp.SDISCONN,
                reason=reason if reason != "quit" else "",
            )

    def account_player_count(self):
        """
        Get the number of connected accounts (not sessions since a
        account may have more than one session depending on settings).
        Only logged-in accounts are counted here.

        Returns:
            naccount (int): Number of connected accounts

        """
        return len(
            set(
                session.uid
                for session in self.values()
                if session.logged_in and not session.account.permissions.check("Admin")
            )
        )
