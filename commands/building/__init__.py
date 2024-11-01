"""
Building commands for Arcellia.
"""

from commands.building.build import CmdBuild
from commands.building.copy import CmdCopy
from commands.building.cpattr import CmdCpAttr
from commands.building.create import CmdCreate
from commands.building.createexit import CmdCreateExit
from commands.building.describe import CmdDescribe
from commands.building.destroy import CmdDestroy
from commands.building.detail import CmdDetail
from commands.building.edit import CmdEdit
from commands.building.examine import CmdExamine
from commands.building.find import CmdFind
from commands.building.link import CmdLink, CmdUnlink
from commands.building.lockstring import CmdLockstring
from commands.building.map import CmdMap
from commands.building.mvattr import CmdMvAttr
from commands.building.purge import CmdPurge
from commands.building.rename import CmdRename
from commands.building.roomstate import CmdRoomState
from commands.building.setalias import CmdSetAlias
from commands.building.setattr import CmdSetAttribute
from commands.building.setgender import CmdSetGender
from commands.building.sethome import CmdSetHome
from commands.building.spawn import CmdSpawn
from commands.building.tag import CmdTag
from commands.building.tickers import CmdTickers
from commands.building.tunnel import CmdTunnel
from commands.building.typeclass import CmdTypeclass
from commands.building.wipe import CmdWipe

__all__ = (
    "CmdBuild",
    "CmdCopy",
    "CmdCpAttr",
    "CmdCreate",
    "CmdCreateExit",
    "CmdDescribe",
    "CmdDestroy",
    "CmdDetail",
    "CmdEdit",
    "CmdExamine",
    "CmdFind",
    "CmdLink",
    "CmdUnlink",
    "CmdLockstring",
    "CmdMap",
    "CmdMvAttr",
    "CmdPurge",
    "CmdRename",
    "CmdRoomState",
    "CmdSetAlias",
    "CmdSetAttribute",
    "CmdSetHome",
    "CmdSetGender",
    "CmdSpawn",
    "CmdTag",
    "CmdTickers",
    "CmdTunnel",
    "CmdTypeclass",
    "CmdWipe",
)
