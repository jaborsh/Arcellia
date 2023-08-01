from codecs import encode as codecs_encode

from evennia.server.portal.naws import Naws as DefaultNaws

NAWS = bytes([31])


class Naws(DefaultNaws):
    """
    Implements the NAWS protocol. Add this to a variable on the telne protocol
    to set it up.

    This rewrite ensures game-side adherence to PEP8 characters per line.
    """

    def negotiate_sizes(self, options):
        """
        Step through the NAWS handshake.

        Args:
            option (list): The incoming NAWS options.
        """
        if len(options) == 4:
            # NAWS is negotiated with 16-bit words
            width = int(codecs_encode(options[0] + options[1], "hex"), 16)
            height = int(codecs_encode(options[2] + options[3], "hex"), 16)
            self.protocol.protocol_flags["SCREENWIDTH"][0] = (
                width if width <= 80 else 80
            )
            self.protocol.protocol_flags["SCREENHEIGHT"][0] = height
