r"""
Evennia settings file.

The available options are found in the default settings file found
here:

https://www.evennia.com/docs/latest/Setup/Settings-Default.html

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Arcellia"

######################################################################
# Networking Replaceables
######################################################################
# Telnet Protocol inherits from whatever above BASE_SESSION_CLASS is specified.
# It is used for all telnet connections, and is also inherited by the SSL Protocol
# (which is just TLS + Telnet).
TELNET_PROTOCOL_CLASS = "server.conf.telnet.TelnetProtocol"

# Server-side session class used. This will inherit from BASE_SESSION_CLASS.
# This one isn't as dangerous to replace.
SERVER_SESSION_CLASS = "server.conf.serversession.ServerSession"

# The Server SessionHandler manages all ServerSessions, handling logins,
# ensuring the login process happens smoothly, handling expected and
# unexpected disconnects. You shouldn't need to touch it, but you can.
# Replace it to implement altered game logic.
SERVER_SESSION_HANDLER_CLASS = "server.conf.sessionhandler.ServerSessionHandler"

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
