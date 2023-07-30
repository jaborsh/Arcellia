r"""
Evennia settings file.

The available options are found in the default settings file found
here:

/root/evennia/mud-platform/evennia/evennia/settings_default.py

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
# The access hierarchy, in climbing order. A higher permission in the
# hierarchy includes access of all levels below it. Used by the perm()/pperm()
# lock functions, which accepts both plural and singular (Admin & Admins)
PERMISSION_HIERARCHY = [
    #"Guest",  # note-only used if GUEST_ENABLED=True
    "Player",
    #"Helper",
    "Builder",
    "Admin",
    "Developer",
]

# Default sizes for client window (in number of characters), if client
# is not supplying this on its own
CLIENT_DEFAULT_WIDTH = 80

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
        "key": "OOC",
        #"aliases": ("pub",),
        "desc": "The official out-of-character channel.",
        "locks": "control:perm(Admin);listen:all();send:all()",
    },
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
    }
]

######################################################################
# Evennia components
######################################################################
# Password validation plugins
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
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
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")