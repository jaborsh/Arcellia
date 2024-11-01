"""
Create exit command module.
"""

from evennia import InterruptCommand
from evennia.commands.default import building

from world.xyzgrid import xyzcommands
from world.xyzgrid.xyzroom import XYZRoom


class CmdCreateExit(xyzcommands.CmdXYZOpen):
    """
    Syntax: createexit <new exit>[;alias;..][:typeclass]
                 [,<return exit>[;alias;..][:typeclass]]] = <destination>
            createexit <new exit>[;alias;..][:typeclass]
                 [,<return exit>[;alias;..][:typeclass]]] = (X,Y,Z)

    Handles the creation of exits. If a destination is given, the exit
    will point there. The destination can also be given as an (X,Y,Z)
    coordinate on the XYZGrid - this command is used to link non-grid rooms to
    the grid and vice-versa.

    The <return exit> argument sets up an exit at the destination leading back
    to the current room. Apart from (X,Y,Z) coordinate, destination name can be
    given both as a #dbref and a name, if that name is globally unique.

    Examples:
        createexit kitchen = Kitchen
        createexit north, south = Town Center
        createexit cave mouth;cave = (3, 4, the small cave)
    """

    key = "createexit"

    def parse(self):
        building.ObjManipCommand.parse(self)

        self.location = self.caller.location
        if not self.args or not self.rhs:
            self.caller.msg(
                "Usage: createexit <new exit>[;alias...][:typeclass]"
                "[,<return exit>[;alias..][:typeclass]]] "
                "= <destination or (X,Y,Z)>"
            )
            raise InterruptCommand
        if not self.location:
            self.caller.msg("You cannot create an exit from a None-location.")
            raise InterruptCommand

        if all(char in self.rhs for char in ("(", ")", ",")):
            # search by (X,Y) or (X,Y,Z)
            inp = self.rhs.strip("()")
            X, Y, *Z = inp.split(",", 2)
            if not Z:
                self.caller.msg(
                    "A full (X,Y,Z) coordinate must be given for the destination."
                )
                raise InterruptCommand
            Z = Z[0]
            # search by coordinate
            X, Y, Z = str(X).strip(), str(Y).strip(), str(Z).strip()
            try:
                self.destination = XYZRoom.objects.get_xyz(xyz=(X, Y, Z))
            except XYZRoom.DoesNotExist:
                self.caller.msg(f"Found no target XYZRoom at ({X},{Y},{Z}).")
                raise InterruptCommand
        else:
            # regular search query
            self.destination = self.caller.search(self.rhs, global_search=True)
            if not self.destination:
                raise InterruptCommand

        self.exit_name = self.lhs_objs[0]["name"]
        self.exit_aliases = self.lhs_objs[0]["aliases"]
        self.exit_typeclass = self.lhs_objs[0]["option"]
