"""
ServerSession

The serversession is the Server-side in-memory representation of a
user connecting to the game.  Evennia manages one Session per
connection to the game. So a user logged into the game with multiple
clients (if Evennia is configured to allow that) will have multiple
sessions tied to one Account object. All communication between Evennia
and the real-world user goes through the Session(s) associated with that user.

It should be noted that modifying the Session object is not usually
necessary except for the most custom and exotic designs - and even
then it might be enough to just add custom session-level commands to
the SessionCmdSet instead.

This module is not normally called. To tell Evennia to use the class
in this module instead of the default one, add the following to your
settings file:

    SERVER_SESSION_CLASS = "server.conf.serversession.ServerSession"

"""
from evennia.server.serversession import ServerSession as BaseServerSession
from utils.colors import hex_to_xterm


class ServerSession(BaseServerSession):
    """
    This class represents a player's session and is a template for
    individual protocols to communicate with Evennia.

    Each account gets one or more sessions assigned to them whenever they connect
    to the game server. All communication between game and account goes
    through their session(s).
    """

    def data_out(self, **kwargs):
        """
        Sending data from Evennia->Client

        Keyword Args:
            text (str or tuple)
            any (str or tuple): Send-commands identified
                by their keys. Or "options", carrying options
                for the protocol(s).

        """
        try:
            kwargs["text"] = (
                hex_to_xterm(kwargs["text"][0])
                if type(kwargs["text"]) == tuple
                else hex_to_xterm(kwargs["text"])
            )
        except KeyError:
            pass

        self.sessionhandler.data_out(self, **kwargs)

    pass
