r"""
Evennia settings file.

The available options are found in the default settings file found
here:

/Users/jake/Evennia/evenv/lib/python3.11/site-packages/evennia/settings_default.py

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

from server.conf import secret_settings

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Arcellia"
# Short one-sentence blurb describing your game. Shown under the title
# on the website and could be used in online listings of your game etc.
GAME_SLOGAN = None

# open to the internet: 4000, 4001, 4002
# closed to the internet (internal use): 4005, 4006
TELNET_PORTS = [4000]
WEBSOCKET_CLIENT_PORT = 4002
WEBSERVER_PORTS = [(4001, 4005)]
AMP_PORT = 4006

# This needs to be set to your website address for django or you'll receive a
# CSRF error when trying to log on to the web portal
CSRF_TRUSTED_ORIGINS = ["https://arcellia.com"]

# Optional - security measures limiting interface access
# (don't set these before you know things work without them)
TELNET_INTERFACES = ["127.0.0.1"]
WEBSOCKET_CLIENT_INTERFACE = "127.0.0.1"
WEBSOCKET_CLIENT_URL = 'wss://arcellia.com:4002/'
ALLOWED_HOSTS = [".arcellia.com"]

# uncomment if you want to lock the server down for maintenance.
# LOCKDOWN_MODE = True

# Determine how many commands per second a given Session is allowed
# to send to the Portal via a connected protocol. Too high rate will
# drop the command and echo a warning. Note that this will also cap
# OOB messages so don't set it too low if you expect a lot of events
# from the client! To turn the limiter off, set to <= 0.
MAX_COMMAND_RATE = 60
# The warning to echo back to users if they send commands too fast
COMMAND_RATE_WARNING = (
    "|RYou're entering commands too fast. Wait a moment and try again.|n"
)

# Determine how large of a string can be sent to the server in number
# of characters. If they attempt to enter a string over this character
# limit, we stop them and send a message. To make unlimited, set to
# 0 or less.
MAX_CHAR_LIMIT = 1600  # 80 characters * 20 lines, previously 6000.
# The warning to echo back to users if they enter a very large string
MAX_CHAR_LIMIT_WARNING = (
    "|RYou've entered a string that is too long. "
    "Please break it up into multiple parts.|n"
)

######################################################################
# Evennia pluggable modules
######################################################################
# Plugin modules extend Evennia in various ways. In the cases with no
# existing default, there are examples of many of these modules
# in contrib/examples.

# On a multi-match when search objects or commands, the user has the
# ability to search again with an index marker that differentiates
# the results. If multiple "box" objects are found, they can by default
# can be separated as box 1, box 2.
# The regex must have one have two capturing groups:
# (?P<number>...) and (?P<name>...)
# the default parser expects this. It should also involve a number
# starting from 1. When changing this you must also update
# SEARCH_MULTIMATCH_TEMPLATE to properly describe the syntax.
SEARCH_MULTIMATCH_REGEX = r"(?P<name>[^-]*) (?P<number>[0-9]+)(?P<args>.*)"
# To display multimatch errors in various listings we must display
# the syntax in a way that matches what SEARCH_MULTIMATCH_REGEX understand.
# The template will be populated with data and expects the following markup:
# {number} - the order of the multimatch, starting from 1; {name} - the
# name (key) of the multimatched entity; {aliases} - eventual
# aliases for the entity; {info} - extra info like #dbrefs for staff. Don't
# forget a line break if you want one match per line.
SEARCH_MULTIMATCH_TEMPLATE = " {name} {number}{aliases}{info}\n"

######################################################################
# Game Time setup
######################################################################

# You don't actually have to use this, but it affects the routines in
# evennia.utils.gametime.py and allows for a convenient measure to
# determine the current in-game time. You can of course interpret
# "week", "month" etc as your own in-game time units as desired.

# The time factor dictates if the game world runs faster (timefactor>1)
# or slower (timefactor<1) than the real world.
TIME_FACTOR = 1.0
# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/8.0/interactive/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = "EST"
# The starting point of your game time (the epoch), in seconds.
# In Python a value of 0 means Jan 1 1970 (use negatives for earlier
# start date). This will affect the returns from the utils.gametime
# module. If None, the server's first start-time is used as the epoch.
TIME_GAME_EPOCH = None
# Normally, game time will only increase when the server runs. If this is True,
# game time will not pause when the server reloads or goes offline. This setting
# together with a time factor of 1 should keep the game in sync with
# the real time (add a different epoch to shift time)
TIME_IGNORE_DOWNTIMES = True

######################################################################
# Default Account setup and access
######################################################################
# Different Multisession modes allow a player (=account) to connect to the
# game simultaneously with multiple clients (=sessions).
#  0 - single session per account (if reconnecting, disconnect old session)
#  1 - multiple sessions per account, all sessions share output
#  2 - multiple sessions per account, one session allowed per puppet
#  3 - multiple sessions per account, multiple sessions per puppet (share output)
#      session getting the same data.
MULTISESSION_MODE = 3
# Whether we should create a character with the same name as the account when
# a new account is created. Together with AUTO_PUPPET_ON_LOGIN, this mimics
# a legacy MUD, where there is no difference between account and character.
AUTO_CREATE_CHARACTER_WITH_ACCOUNT = False
# Whether an account should auto-puppet the last puppeted puppet when logging in. This
# will only work if the session/puppet combination can be determined (usually
# MULTISESSION_MODE 0 or 1), otherwise, the player will end up OOC. Use
# MULTISESSION_MODE=0, AUTO_CREATE_CHARACTER_WITH_ACCOUNT=True and this value to
# mimic a legacy mud with minimal difference between Account and Character. Disable
# this and AUTO_PUPPET to get a chargen/character select screen on login.
AUTO_PUPPET_ON_LOGIN = False
# How many *different* characters an account can puppet *at the same time*. A value
# above 1 only makes a difference together with MULTISESSION_MODE > 1.
MAX_NR_SIMULTANEOUS_PUPPETS = None
# The maximum number of characters allowed by be created by the default ooc
# char-creation command. This can be seen as how big of a 'stable' of characters
# an account can have (not how many you can puppet at the same time). Set to
# None for no limit.
MAX_NR_CHARACTERS = None
# The access hierarchy, in climbing order. A higher permission in the
# hierarchy includes access of all levels below it. Used by the perm()/pperm()
# lock functions, which accepts both plural and singular (Admin & Admins)
PERMISSION_HIERARCHY = [
    "Guest",  # note-only used if GUEST_ENABLED=True
    "Player",
    "Helper",
    "Builder",
    "Admin",
    "Developer",
]

# Default sizes for client window (in number of characters), if client
# is not supplying this on its own
CLIENT_DEFAULT_WIDTH = 80

# Set rate limits per-IP on account creations and login attempts. Set limits
# to None to disable.
CREATION_THROTTLE_LIMIT = 0
# CREATION_THROTTLE_TIMEOUT = 10 * 60
LOGIN_THROTTLE_LIMIT = 0
# LOGIN_THROTTLE_TIMEOUT = 5 * 60

######################################################################
# In-game Channels created from server start
######################################################################
# New accounts will auto-sub to the default channels given below (but they can
# unsub at any time). Traditionally, at least 'public' should exist. Entries
# will be (re)created on the next reload, but removing or updating a same-key
# channel from this list will NOT automatically change/remove it in the game,
# that needs to be done manually. Note: To create other, non-auto-subbed
# channels, create them manually in server/conf/at_initial_setup.py.
DEFAULT_CHANNELS = [
    {
        "key": "Chat",
        "desc": "The casual chat channel.",
        "locks": "control:perm(Admin);listen:all();send:all()",
    },
    {
        "key": "Question",
        "desc": "The official help & question channel.",
        "locks": "control:perm(Admin);listen:all();send:all()",
    },
    {
        "key": "Staff",
        "desc": "The official staff channel.",
        "locks": "control:perm(Developer);listen:perm(Admin);send:perm(Admin)",
    },
]

######################################################################
# External Connections
######################################################################
# Discord (discord.com) is a popular communication service for many, especially
# for game communities. Evennia's channels can be connected to Discord channels
# and relay messages between Evennia and Discord. To use, you will need to create
# your own Discord application and bot.
# Discord also requires installing the pyopenssl library.
# Full step-by-step instructions are available in the official Evennia documentation.
# DISCORD_ENABLED = False

# The authentication token for the Discord bot. This should be kept secret and
# put in your secret_settings file.
# DISCORD_BOT_TOKEN = secret_settings.DISCORD_BOT_TOKEN

######################################################################
# Evennia components
######################################################################
# Password validation plugins
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    # {
    #     "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    #     "OPTIONS": {"min_length": 8},
    # },
]

# Username validation plugins
AUTH_USERNAME_VALIDATORS = [
    {"NAME": "django.contrib.auth.validators.ASCIIUsernameValidator"},
    {
        "NAME": "django.core.validators.MinLengthValidator",
        "OPTIONS": {"limit_value": 3},
    },
    {
        "NAME": "django.core.validators.MaxLengthValidator",
        "OPTIONS": {"limit_value": 16},
    },
    {"NAME": "evennia.server.validators.EvenniaUsernameAvailabilityValidator"},
]

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

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
