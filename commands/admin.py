import re

from django.conf import settings
from evennia import InterruptCommand
from evennia.commands.default import building, muxcommand
from evennia.contrib.grid.xyzgrid.xyzroom import XYZRoom
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import class_from_module
from evennia.utils.utils import inherits_from
from parsing.text import wrap
from server.conf.settings import SERVERNAME
from world.amenu import AMenu

from commands.command import Command

COMMAND_DEFAULT_CLASS = class_from_module(settings.COMMAND_DEFAULT_CLASS)

__all__ = (
    "CmdTest",
    "CmdAccess",
    "CmdAnnounce",
    "CmdEcho",
    "CmdForce",
    "CmdHome",
    "CmdTeleport",
    "CmdTransfer",
    "CmdWatch",
)


class CmdTest(Command):
    key = "test"

    def func(self):
        AMenu(
            self.caller,
            "world.chargen.menu",
            startnode="chargen_welcome",
            auto_look=True,
            auto_help=True,
            persistent=True,
        )


class CmdAccess(COMMAND_DEFAULT_CLASS):
    """
    Syntax: access

    This command shows you the permission hierarchy and which permission groups
    you are a member of.
    """

    key = "access"
    aliases = ["groups", "hierarchy"]
    locks = "cmd:perm(Admin)"
    help_category = "Admin"
    arg_regex = r"$"

    def func(self):
        """Load the permission groups"""

        caller = self.caller
        hierarchy_full = settings.PERMISSION_HIERARCHY
        string = "\n|wPermission Hierarchy|n (climbing):\n %s" % ", ".join(
            hierarchy_full
        )

        if self.caller.account.is_superuser:
            cperms = "<Superuser>"
            pperms = "<Superuser>"
        else:
            cperms = ", ".join(caller.permissions.all())
            pperms = ", ".join(caller.account.permissions.all())

        string += "\n|wYour access|n:"
        string += f"\nCharacter |c{caller.key}|n: {cperms}"
        if hasattr(caller, "account"):
            string += f"\nAccount |c{caller.account.key}|n: {pperms}"
        caller.msg(string)


class CmdAnnounce(Command):
    """
    Syntax: announce <message>

    Announces a message to all connected sessions including all currently
    disconnected.
    """

    key = "announce"
    locks = "cmd:perm(announce) or perm(Admin)"
    help_category = "Admin"

    def func(self):
        if not self.args:
            self.caller.msg("Syntax: announce <message>")
            return

        self.args = wrap(self.args, 63, align="c", pre_text="  ")

        string = """
|C  .:*~*:._.:*~*:._.:*~ |r{SERVERNAME} Announcement |C~*:._.:*~*:._.:*~*:.|n
           
|Y{message}|n
            
|C  .:*~*:._.:*~*:._.:*~                       ~*:._.:*~*:._.:*~*:.|n""".format(
            SERVERNAME=SERVERNAME, message=self.args
        )

        SESSIONS.announce_all(string)


class CmdEcho(COMMAND_DEFAULT_CLASS):
    """
    Syntax: echo[/switch] <objects> <message>

    Switches:
      - all:   Echo to all objects in the game.
      - rooms: Echo to objects' rooms.

    Aliases:
      - aecho: Alias for echo/all.
      - recho: Alias for echo/rooms.

    Examples:
      1. "echo jake Hello, Jake!"
           - send the message "Hello, Jake!" to only Jake.
      2. "echo jake,jeanne Hello, Jake and Jeanne!"
           - will send the message "Hello, Jake and Jeanne!" to Jake and
             Jeanne.
      3. "echo/rooms jake Hello, Jake!"
           - will send the message "Hello, Jake" to Jake's location.
      4. "echo/rooms jake,jeanne Hello, Jake and Jeanne!"
           - will send the message "Hello, Jake and Jeanne!" to Jake's
             and Jeanne's locations.
      5. "echo/all Hello, world!"
           - will send the message "Hello, world!" to all objects in the game.
      6. "aecho Hello, world!"
           - will send the message "Hello, world!" globally.
      7. "recho Hello, world!"
           - will send the message "Hello, world!" to the rooms of the objects.

    Echo a message to the selected objects or globally. If the object is a
    room, send to its contents. If the object is a character, send to the
    character.
    """

    key = "echo"
    aliases = ["aecho", "recho"]
    switch_options = ("all", "rooms")
    locks = "cmd:perm(echo) or perm(Admin)"
    help_category = "Admin"

    def parse(self):
        pattern = r"(\/[^ ]+)? ?([^ ]+)? (.+)"
        match = re.match(pattern, self.args)

        if match:
            self.switches = match.group(1).lstrip("/") if match.group(1) else ""
            self.objects = (
                [obj.strip() for obj in match.group(2).split(",")]
                if match.group(2)
                else []
            )
            self.message = match.group(3).strip() if match.group(3) else None

    def func(self):
        caller = self.caller
        objects = self.objects
        message = self.message

        if not self.message:
            caller.msg("Echo what?")
            return

        if self.cmdstring == "aecho" or "all" in self.switches:
            caller.msg("Echoing to all objects:")
            SESSIONS.announce_all(message)
            return

        if not self.objects:
            caller.msg("Syntax: echo[/switches] <objects> <message>")
            return

        # send the message to the objects
        echoed = []
        locations = []
        for obj in objects:
            obj = caller.search(obj, global_search=True)
            if not obj:
                return
            if self.cmdstring == "recho" or "rooms" in self.switches:
                if obj.location not in locations:
                    obj.location.msg_contents(message)
                    for obj in obj.location.contents:
                        echoed.append(obj.name)
                    locations.append(obj.location)
                    continue

            obj.msg(message)
            echoed.append(obj.name)

        caller.msg(f"Echoed to {', '.join(echoed)}: {message}")


class CmdForce(Command):
    """
    Syntax: force <object> <command>

    Forces an object to execute a command.
    """

    key = "force"
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        if not self.args:
            self.msg("Syntax: force <object> <command>")

        args = self.args.split(" ", 1)
        obj = self.account.search(args[0], global_search=True, search_object=True)
        if not obj:
            return

        if not args[1]:
            self.msg(f"{obj} is all ears.")
            return

        obj.execute_cmd(args[1])
        self.msg(f"You force {obj} to {args[1]}")


class CmdHome(COMMAND_DEFAULT_CLASS):
    """
    Syntax: home

    Teleports you to your home location.
    """

    key = "home"
    locks = "cmd:perm(home) or perm(Admin)"
    help_category = "Admin"
    arg_regex = r"$"

    def func(self):
        """Implement the command"""
        caller = self.caller
        home = caller.home
        if not home:
            caller.msg("You have no home!")
        elif home == caller.location:
            caller.msg("You are already home!")
        else:
            caller.msg("There's no place like home ...")
            caller.move_to(home, move_type="teleport")


class CmdTeleport(building.CmdTeleport):
    """
    Syntax: tel/switch [<object> to||=] <target location>
            tel/switch [<object> to||=] (X,Y[,Z])

    Examples:
      tel Limbo
      tel/quiet box = Limbo
      tel/tonone box
      tel (3, 3, the small cave)
      tel (4, 1)   # on the same map
      tel/map Z | mapname

    Switches:
      quiet  - don't echo leave/arrive messages to the source/target
               locations for the move.
      intoexit - if target is an exit, teleport INTO
                 the exit object instead of to its destination
      tonone - if set, teleport the object to a None-location. If this
               switch is set, <target location> is ignored.
               Note that the only way to retrieve
               an object from a None location is by direct #dbref
               reference. A puppeted object cannot be moved to None.
      loc - teleport object to the target's location instead of its contents
      map - show coordinate map of given Zcoord/mapname.

    Teleports an object somewhere. If no object is given, you yourself are
    teleported to the target location. If (X,Y) or (X,Y,Z) coordinates
    are given, the target is a location on the XYZGrid.
    """

    key = "teleport"
    aliases = ["goto", "tel"]

    def _search_by_xyz(self, inp):
        inp = inp.strip("()")
        X, Y, *Z = inp.split(",", 2)
        if Z:
            # Z was specified
            Z = Z[0]
        else:
            # use current location's Z, if it exists
            try:
                xyz = self.caller.location.xyz
            except AttributeError:
                self.caller.msg(
                    "Z-coordinate is also required since you are not currently "
                    "in a room with a Z coordinate of its own."
                )
                raise InterruptCommand
            else:
                Z = xyz[2]
        # search by coordinate
        X, Y, Z = str(X).strip(), str(Y).strip(), str(Z).strip()
        try:
            self.destination = XYZRoom.objects.get_xyz(xyz=(X, Y, Z))
        except XYZRoom.DoesNotExist:
            self.caller.msg(f"Found no target XYZRoom at ({X},{Y},{Z}).")
            raise InterruptCommand

    def parse(self):
        muxcommand.MuxCommand.parse(self)
        self.obj_to_teleport = self.caller
        self.destination = None

        if self.rhs:
            self.obj_to_teleport = self.caller.search(self.lhs, global_search=True)
            if not self.obj_to_teleport:
                self.caller.msg("Did not find object to teleport.")
                raise InterruptCommand
            if all(char in self.rhs for char in ("(", ")", ",")):
                # search by (X,Y) or (X,Y,Z)
                self._search_by_xyz(self.rhs)
            else:
                # fallback to regular search by name/alias
                self.destination = self.caller.search(self.rhs, global_search=True)

        elif self.lhs:
            if all(char in self.lhs for char in ("(", ")", ",")):
                self._search_by_xyz(self.lhs)
            else:
                self.destination = self.caller.search(self.lhs, global_search=True)


class CmdTransfer(COMMAND_DEFAULT_CLASS):
    """
    Syntax: transfer <object>

    Transfers an object to your current location.
    """

    key = "transfer"
    locks = "cmd:perm(Admin)"
    help_category = "Admin"

    def func(self):
        caller = self.caller

        if not self.args:
            caller.msg("Syntax: transfer <object>")
            return

        obj_to_transfer = self.caller.search(self.args.strip(), global_search=True)
        if not obj_to_transfer:
            return

        if inherits_from(obj_to_transfer, "typeclasses.rooms.Room"):
            caller.msg("You cannot transfer a room.")
            return

        if inherits_from(obj_to_transfer, "typeclasses.exits.Exit"):
            caller.msg("You cannot transfer an exit.")
            return

        if obj_to_transfer.location == caller.location:
            caller.msg(f"{obj_to_transfer} is already here.")
            return

        if obj_to_transfer == caller.location:
            caller.msg("You cannot transfer an object to itself.")
            return

        if obj_to_transfer in caller.location.contents:
            caller.msg("You can't teleport an object inside something it holds!")

        if not obj_to_transfer.access(caller, "control"):
            caller.msg(f"You do not have permission to transfer {obj_to_transfer}.")
            return

        if obj_to_transfer.move_to(
            caller.location, emit_to_obj=caller, move_type="transfer"
        ):
            caller.msg(f"You transfer {obj_to_transfer}.")
        else:
            caller.msg(f"You fail to transfer {obj_to_transfer}.")


class CmdWatch(Command):
    """
    Syntax: watch <character>

    When called, the admin will start watching the actions of the specified character.
    If the admin is already watching a character, calling watch again will stop the
    current watch and start a new one on the specified character.
    """

    key = "watch"
    aliases = ["snoop"]
    locks = "cmd:perm(Admin)"
    help_category = "Admin"

    def func(self):
        caller = self.caller
        if caller.ndb._watching:
            # Remove the caller from the old target's watchers list
            caller.ndb._watching.ndb._watchers.remove(caller)
            self.msg(f"You stop watching {caller.ndb._watching}.")
            caller.ndb._watching = None
            return
        elif not self.args:
            self.msg("Syntax: watch <character>")
            return

        target = self.account.search(self.args.strip(), search_object=True)
        if not target:
            return

        # Set up the watch
        self.msg(f"Watching {target.name}.")
        caller.ndb._watching = target
        target.ndb._watchers = target.ndb._watchers or []
        target.ndb._watchers.append(caller)
