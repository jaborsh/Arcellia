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

import os

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Arcellia"
# Short one-sentence blurb describing your game. Shown under the title
# on the website and could be used in online listings of your game etc.
GAME_SLOGAN = ""
# Interface addresses to listen to. If 0.0.0.0, listen to all. Use :: for IPv6.
WEBSOCKET_CLIENT_INTERFACE = "127.0.0.1"

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

# Place to put log files, how often to rotate the log and how big each log file
# may become before rotating.
LOG_DIR = os.path.join(GAME_DIR, "server", "logs")
SERVER_LOG_FILE = os.path.join(LOG_DIR, "server", "server.log")
PORTAL_LOG_FILE = os.path.join(LOG_DIR, "portal", "portal.log")
HTTP_LOG_FILE = os.path.join(LOG_DIR, "http", "http_requests.log")
LOCKWARNING_LOG_FILE = os.path.join(LOG_DIR, "lockwarning", "lockwarnings.log")
ACCOUNT_LOG_DIR = os.path.join(LOG_DIR, "accounts")
CHANNEL_LOG_DIR = os.path.join(LOG_DIR, "channels")

log_files = [
    SERVER_LOG_FILE,
    PORTAL_LOG_FILE,
    HTTP_LOG_FILE,
    LOCKWARNING_LOG_FILE,
    ACCOUNT_LOG_DIR,
    CHANNEL_LOG_DIR,
]
for log_file in log_files:
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)

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
# Default command sets and commands
######################################################################
COMMAND_DEFAULT_CLASS = "commands.command.Command"
EXTRA_LAUNCHER_COMMANDS["xyzgrid"] = "world.xyzgrid.launchcmd.xyzcommand"
PROTOTYPE_MODULES += ["world.xyzgrid.xyzprototypes"]

# On a multi-match when search objects or commands, the user has the
# ability to search again with an index marker that differentiates
# the results. If multiple "box" objects
# are found, they can by default be separated as 1-box, 2-box. Below you
# can change the regular expression used. The regex must have one
# have two capturing groups (?P<number>...) and (?P<name>...) - the default
# parser expects this. It should also involve a number starting from 1.
# When changing this you must also update SEARCH_MULTIMATCH_TEMPLATE
# to properly describe the syntax.
SEARCH_MULTIMATCH_REGEX = r"(?P<name>[^\s]*)\s(?P<number>[0-9]+)(?P<args>.*)"
# To display multimatch errors in various listings we must display
# the syntax in a way that matches what SEARCH_MULTIMATCH_REGEX understand.
# The template will be populated with data and expects the following markup:
# {number} - the order of the multimatch, starting from 1; {name} - the
# name (key) of the multimatched entity; {aliases} - eventual
# aliases for the entity; {info} - extra info like #dbrefs for staff. Don't
# forget a line break if you want one match per line.
SEARCH_MULTIMATCH_TEMPLATE = " {name} {number}{aliases}{info}\n"
# The handler that outputs errors when using any API-level search
# (not manager methods). This function should correctly report errors
# both for command- and object-searches. This allows full control
# over the error output (it uses SEARCH_MULTIMATCH_TEMPLATE by default).
SEARCH_AT_RESULT = "server.conf.at_search.at_search_result"
# A module that must exist - this holds the instructions Evennia will use to
# first prepare the database for use (create user #1 and Limbo etc). Only override if
# you really know what # you are doing. If replacing, it must contain a function
# handle_setup(stepname=None). The function will start being called with no argument
# and is expected to maintain a named sequence of steps. Once each step is completed, it
# should be saved with ServerConfig.objects.conf('last_initial_setup_step', stepname)
# on a crash, the system will continue by calling handle_setup with the last completed
# step. The last step in the sequence must be named 'done'. Once this key is saved,
# initialization will not run again.
INITIAL_SETUP_MODULE = "server.conf.at_initial_setup"
# An optional module that, if existing, must hold a function
# named at_initial_setup(). This hook method can be used to customize
# the server's initial setup sequence (the very first startup of the system).
# The check will fail quietly if module doesn't exist or fails to load.
AT_INITIAL_SETUP_HOOK_MODULE = "server.conf.at_initial_setup"

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
# Typeclasses and other paths
######################################################################
# Typeclass for clothing (fallback)
BASE_CLOTHING_TYPECLASS = "typeclasses.clothing.Clothing"
# Typeclass for equipment (fallback)
BASE_EQUIPMENT_TYPECLASS = "typeclasses.equipment.equipment.Equipment"
# Typeclass for weapons (fallback)
BASE_WEAPON_TYPECLASS = "typeclasses.equipment.weapons.Weapon"
# Typeclass for mobs (fallback)
BASE_MOB_TYPECLASS = "typeclasses.mobs.Mob"

######################################################################
# Default Account setup and access
######################################################################
# The start position for new characters. Default is Creation (#3).
START_LOCATION = "#3"

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
MAX_NR_CHARACTERS = 2
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
# Evennia components
######################################################################
# Password validation plugins
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa: E501
    },
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
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
