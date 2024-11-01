"""
Admin-related commands.
"""

from commands.admin.access import CmdAccess
from commands.admin.announce import CmdAnnounce
from commands.admin.at import CmdAt
from commands.admin.diary import CmdDiary
from commands.admin.echo import CmdEcho
from commands.admin.force import CmdForce
from commands.admin.home import CmdHome
from commands.admin.noshout import CmdNoShout
from commands.admin.petrify import CmdPetrify
from commands.admin.reports import CmdReports
from commands.admin.restore import CmdRestore
from commands.admin.teleport import CmdTeleport
from commands.admin.transfer import CmdTransfer
from commands.admin.watch import CmdWatch
from commands.admin.wizinv import CmdWizInv

__all__ = (
    "CmdAccess",
    "CmdAnnounce",
    "CmdAt",
    "CmdDiary",
    "CmdEcho",
    "CmdForce",
    "CmdHome",
    "CmdNoShout",
    "CmdPetrify",
    "CmdReports",
    "CmdRestore",
    "CmdTeleport",
    "CmdTransfer",
    "CmdWatch",
    "CmdWizInv",
)
