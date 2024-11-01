from evennia import InterruptCommand
from evennia.commands.default import muxcommand

from commands.command import Command
from world.xyzgrid.xyzroom import XYZRoom


class CmdTeleport(Command):
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
      quiet    - don't echo leave/arrive messages to the source/target
      intoexit - if target is an exit, teleport INTO the exit object
      tonone   - teleport the object to a none-location
      loc      - teleport object to the target's location
      map      - show coordinate map of given Zcoord/mapname.

    Teleports an object somewhere. If no object is given, you yourself are
    teleported to the target location. If (X,Y) or (X,Y,Z) coordinates
    are given, the target is a location on the XYZGrid.
    """

    key = "teleport"
    aliases = ["goto", "tel"]
    switch_options = ("quiet", "intoexit", "tonone", "loc")
    rhs_split = ("=", " to ")  # Prefer = delimiter, but allow " to " usage.
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def parse(self):
        muxcommand.MuxCommand.parse(self)
        self.obj_to_teleport = self.caller
        self.destination = None

        if self.rhs:
            self.obj_to_teleport = self.caller.search(
                self.lhs, global_search=True
            )
            if not self.obj_to_teleport:
                self.caller.msg("Did not find object to teleport.")
                raise InterruptCommand

            if self.is_coordinate_input(self.rhs):
                self.search_by_xyz(self.rhs)
            else:
                self.destination = self.caller.search(
                    self.rhs, global_search=True
                )
        elif self.lhs:
            if self.is_coordinate_input(self.lhs):
                self.search_by_xyz(self.lhs)
            else:
                self.destination = self.caller.search(
                    self.lhs, global_search=True
                )

    def is_coordinate_input(self, input_str):
        """
        Determine if the input string represents coordinates.
        """
        return (
            input_str.startswith("(")
            and input_str.endswith(")")
            and "," in input_str
        )

    def search_by_xyz(self, inp):
        """
        Search for a destination based on XYZ coordinates.
        """
        inp = inp.strip("()")
        parts = [part.strip() for part in inp.split(",")]

        if len(parts) < 2:
            self.caller.msg("Invalid coordinate format. Use (X,Y) or (X,Y,Z).")
            raise InterruptCommand

        X, Y = parts[0], parts[1]
        Z = parts[2] if len(parts) > 2 else self.get_default_z()

        if Z is None:
            return

        self.destination = XYZRoom.objects.get_xyz(xyz=(X, Y, Z))
        if not self.destination:
            self.caller.msg(f"No XYZRoom found at ({X}, {Y}, {Z}).")
            raise InterruptCommand

    def get_default_z(self):
        """
        Retrieve the default Z-coordinate from the caller's current location.
        """
        try:
            xyz = self.caller.location.xyz
            return xyz[2]
        except AttributeError:
            self.caller.msg(
                "Z-coordinate is required as your current location lacks one."
            )
            raise InterruptCommand

    def func(self):
        """Execute the teleport action based on parsed arguments and switches."""
        caller = self.caller
        obj = self.obj_to_teleport
        dest = self.destination

        if "tonone" in self.switches:
            self.teleport_to_none(obj, dest)
            return

        if not self.args:
            caller.msg(
                "Usage: teleport[/switches] [<obj> =] <target or (X,Y,Z)>||home"
            )
            return

        if not dest:
            caller.msg("Destination not found.")
            return

        if "loc" in self.switches:
            dest = dest.location
            if not dest:
                caller.msg("Destination has no location.")
                return

        if obj == dest:
            caller.msg("You can't teleport an object inside itself!")
            return

        if obj == dest.location:
            caller.msg(
                "You can't teleport an object inside something it holds!"
            )
            return

        if obj.location == dest:
            caller.msg(f"{obj} is already at {dest}.")
            return

        if not self.has_permission(obj, dest):
            return

        self.perform_teleport(obj, dest)

    def teleport_to_none(self, obj, dest):
        """
        Handle teleporting an object to a none-location.
        """
        if dest:
            obj = dest

        if obj.has_account:
            self.caller.msg(
                f"Cannot teleport a puppeted object ({obj.key}, puppeted by {obj.account}) to a None-location."
            )
            return

        self.caller.msg(f"Teleported {obj} -> None-location.")
        if obj.location and "quiet" not in self.switches:
            obj.location.msg_contents(
                f"{self.caller} teleported {obj} into nothingness.",
                exclude=self.caller,
            )
        obj.location = None

    def has_permission(self, obj, dest):
        """
        Check if the caller has permission to teleport the object to the destination.
        """
        caller = self.caller
        if not (
            caller.permissions.check("Admin") or obj.access(caller, "teleport")
        ):
            caller.msg(
                f"{obj} 'teleport'-lock blocks you from teleporting it anywhere."
            )
            return False

        if not (
            caller.permissions.check("Admin")
            or dest.access(obj, "teleport_here")
        ):
            caller.msg(
                f"{dest} 'teleport_here'-lock blocks {obj} from moving there."
            )
            return False

        return True

    def perform_teleport(self, obj, dest):
        """
        Execute the teleportation of the object to the destination.
        """
        caller = self.caller
        quiet = "quiet" in self.switches
        intoexit = "intoexit" in self.switches

        if not obj.location:
            obj.location = dest
            caller.msg(f"Teleported {obj} None -> {dest}")
            return

        moved = obj.move_to(
            dest,
            quiet=quiet,
            emit_to_obj=caller,
            use_destination=not intoexit,
            move_type="teleport",
        )

        if moved:
            if obj == caller:
                caller.msg(f"Teleported to {dest}.")
            else:
                caller.msg(f"Teleported {obj} -> {dest}.")
        else:
            caller.msg("Teleportation failed.")
