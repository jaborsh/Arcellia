from django.conf import settings
from evennia.server.portal import mccp, mssp, mxp, suppress_ga, telnet_oob, ttype
from evennia.server.portal.telnet import TelnetProtocol as DefaultTelnetProtocol
from twisted.conch.telnet import ECHO, LINEMODE, LINEMODE_EDIT, LINEMODE_TRAPSIG, MODE

from server.conf import naws


class TelnetProtocol(DefaultTelnetProtocol):
    """
    Each player connecting over telnet (ie using most traditional mud clients)
    gets a telnet protocol instance assigned to them. All communication between
    game and player goes through here.

    In this fork, we are overriding the default screenwidth options to ensure
    game adherence to PEP8 standards of 80characters/line.
    """

    def connectionMade(self):
        """
        This is called when the connection is first established.

        """
        # important in order to work normally with standard telnet
        self.do(LINEMODE).addErrback(self._wont_linemode)
        # initialize the session
        self.line_buffer = b""
        client_address = self.transport.client
        client_address = client_address[0] if client_address else None
        # this number is counted down for every handshake that completes.
        # when it reaches 0 the portal/server syncs their data
        self.handshakes = (
            8  # suppress-go-ahead, naws, ttype, mccp, mssp, msdp, gmcp, mxp
        )

        self.init_session(
            self.protocol_key, client_address, self.factory.sessionhandler
        )
        self.protocol_flags["ENCODING"] = (
            settings.ENCODINGS[0] if settings.ENCODINGS else "utf-8"
        )
        # add this new connection to sessionhandler so
        # the Server becomes aware of it.
        self.sessionhandler.connect(self)
        # change encoding to ENCODINGS[0] which reflects Telnet default encoding

        # suppress go-ahead
        self.sga = suppress_ga.SuppressGA(self)
        # negotiate client size
        self.naws = naws.Naws(self)
        # negotiate ttype (client info)
        # Obs: mudlet ttype does not seem to work if we start mccp before ttype. /Griatch
        self.ttype = ttype.Ttype(self)
        # negotiate mccp (data compression) - turn this off for wireshark analysis
        self.mccp = mccp.Mccp(self)
        # negotiate mssp (crawler communication)
        self.mssp = mssp.Mssp(self)
        # oob communication (MSDP, GMCP) - two handshake calls!
        self.oob = telnet_oob.TelnetOOB(self)
        # mxp support
        self.mxp = mxp.Mxp(self)

        from evennia.utils.utils import delay

        # timeout the handshakes in case the client doesn't reply at all
        self._handshake_delay = delay(2, callback=self.handshake_done, timeout=True)

        # TCP/IP keepalive watches for dead links
        self.transport.setTcpKeepAlive(1)
        # The TCP/IP keepalive is not enough for some networks;
        # we have to complement it with a NOP keep-alive.
        self.protocol_flags["NOPKEEPALIVE"] = True
        self.nop_keep_alive = None
        self.toggle_nop_keepalive()

    def enableRemote(self, option):
        """
        This sets up the remote-activated options we allow for this protocol.

        Args:
            option (char): The telnet option to enable.

        Returns:
            enable (bool): If this option should be enabled.

        """
        if option == LINEMODE:
            # make sure to activate line mode with local editing for all clients
            self.requestNegotiation(
                LINEMODE,
                MODE + bytes(chr(ord(LINEMODE_EDIT) + ord(LINEMODE_TRAPSIG)), "ascii"),
            )
            return True
        else:
            return (
                option == ttype.TTYPE
                or option == naws.NAWS
                or option == mccp.MCCP
                or option == mssp.MSSP
                or option == ECHO
                or option == suppress_ga.SUPPRESS_GA
            )

    def disableRemote(self, option):
        return (
            option == LINEMODE
            or option == ttype.TTYPE
            or option == naws.NAWS
            or option == mccp.MCCP
            or option == mssp.MSSP
            or option == ECHO
            or option == suppress_ga.SUPPRESS_GA
        )
