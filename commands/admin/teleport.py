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
            if all(char in self.rhs for char in ("(", ")", ",")):
                # search by (X,Y) or (X,Y,Z)
                self.search_by_xyz(self.rhs)
            else:
                # fallback to regular search by name/alias
                self.destination = self.caller.search(
                    self.rhs, global_search=True
                )

        elif self.lhs:
            if all(char in self.lhs for char in ("(", ")", ",")):
                self.search_by_xyz(self.lhs)
            else:
                self.destination = self.caller.search(
                    self.lhs, global_search=True
                )

    def search_by_xyz(self, inp):
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

    def func(self):
        """Performs the teleport"""

        caller = self.caller
        obj_to_teleport = self.obj_to_teleport
        destination = self.destination

        if "tonone" in self.switches:
            # teleporting to None

            if destination:
                # in this case lhs is always the object to teleport
                obj_to_teleport = destination

            if obj_to_teleport.has_account:
                caller.msg(
                    f"Cannot teleport a puppeted object ({obj_to_teleport.key}, puppeted by"
                    f" {obj_to_teleport.account}) to a None-location."
                )
                return
            caller.msg(f"Teleported {obj_to_teleport} -> None-location.")
            if obj_to_teleport.location and "quiet" not in self.switches:
                obj_to_teleport.location.msg_contents(
                    f"{caller} teleported {obj_to_teleport} into nothingness.",
                    exclude=caller,
                )
            obj_to_teleport.location = None
            return

        if not self.args:
            caller.msg(
                "Usage: teleport[/switches] [<obj> =] <target or (X,Y,Z)>||home"
            )
            return

        if not destination:
            caller.msg("Destination not found.")
            return

        if "loc" in self.switches:
            destination = destination.location
            if not destination:
                caller.msg("Destination has no location.")
                return

        if obj_to_teleport == destination:
            caller.msg("You can't teleport an object inside of itself!")
            return

        if obj_to_teleport == destination.location:
            caller.msg(
                "You can't teleport an object inside something it holds!"
            )
            return

        if obj_to_teleport.location and obj_to_teleport.location == destination:
            caller.msg(f"{obj_to_teleport} is already at {destination}.")
            return

        # check any locks
        if not (
            caller.permissions.check("Admin")
            or obj_to_teleport.access(caller, "teleport")
        ):
            caller.msg(
                f"{obj_to_teleport} 'teleport'-lock blocks you from teleporting it anywhere."
            )
            return

        if not (
            caller.permissions.check("Admin")
            or destination.access(obj_to_teleport, "teleport_here")
        ):
            caller.msg(
                f"{destination} 'teleport_here'-lock blocks {obj_to_teleport} from moving there."
            )
            return

        # try the teleport
        if not obj_to_teleport.location:
            # teleporting from none-location
            obj_to_teleport.location = destination
            caller.msg(f"Teleported {obj_to_teleport} None -> {destination}")
        elif obj_to_teleport.move_to(
            destination,
            quiet="quiet" in self.switches,
            emit_to_obj=caller,
            use_destination="intoexit" not in self.switches,
            move_type="teleport",
        ):
            if obj_to_teleport == caller:
                caller.msg(f"Teleported to {destination}.")
            else:
                caller.msg(f"Teleported {obj_to_teleport} -> {destination}.")
        else:
            caller.msg("Teleportation failed.")
