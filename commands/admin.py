import re

from django.conf import settings
from evennia import InterruptCommand
from evennia.commands.default import muxcommand
from evennia.comms.models import Msg
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import create, evtable
from evennia.utils.utils import inherits_from

from commands.command import Command
from utils.text import wrap
from world.xyzgrid.xyzroom import XYZRoom

__all__ = (
    "CmdAccess",
    "CmdAnnounce",
    "CmdDiary",
    "CmdEcho",
    "CmdForce",
    "CmdHome",
    "CmdReports",
    "CmdRestore",
    "CmdTeleport",
    "CmdTransfer",
    "CmdWatch",
)


class CmdAccess(Command):
    """
    Command class for displaying the caller's access and permission groups.

    Usage:
      access

    This command displays the permission groups and the caller's access level.
    If the caller is a superuser, it displays "<Superuser>". Otherwise, it
    displays the caller's permissions for both the character and the account.
    """

    key = "access"
    aliases = ["groups", "hierarchy"]
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        """Load the permission groups and display the caller's access"""
        caller = self.caller
        hierarchy_full = settings.PERMISSION_HIERARCHY

        if caller.account.is_superuser:
            cperms = pperms = "<Superuser>"
        else:
            cperms = ", ".join(caller.permissions.all())
            pperms = ", ".join(caller.account.permissions.all())

        string = (
            "\n|wPermission Hierarchy|n (climbing):\n %s\n"
            "\n|wYour access|n:"
            "\n  Character |c%s|n: %s" % (", ".join(hierarchy_full), caller.key, cperms)
        )

        if hasattr(caller, "account"):
            string += "\n  Account |c%s|n: %s" % (caller.account.key, pperms)

        caller.msg(string)


class CmdAnnounce(Command):
    """
    Command to announce a message to all players.

    Usage:
        announce <message>

    This command allows administrators to send an announcement to all players
    currently connected to the game. The message should be provided as an argument
    after the command. The announcement will be displayed to all players in a
    formatted manner.

    Example:
        > announce Welcome to the game!

    This will send the message "Welcome to the game!" as an announcement to all
    connected players.
    """

    key = "announce"
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        if not self.args:
            self.caller.msg("Syntax: announce <message>")
            return

        message = wrap(self.args, text_width=63, align="c", pre_text="  ")
        announcement = (
            "\n|C  .:*~*:._.:*~*:._.:*~ |r{SERVERNAME} Announcement |C~*:._.:*~*:._.:*~*:.|n"
            "\n\n|Y{message}|n"
            "\n\n|C  .:*~*:._.:*~*:._.:*~                       ~*:._.:*~*:._.:*~*:.|n"
        ).format(SERVERNAME=settings.SERVERNAME, message=message)

        SESSIONS.announce_all(announcement)


class CmdDiary(Command):
    """
    Command to manage the admin diary.

    Usage:
        diary [<entry>]

    This command allows admins to add entries to the admin diary or view the latest entries.

    If no argument is provided, it displays the last 10 diary entries. Each entry includes the author, date, and message.

    If an entry is provided as an argument, it adds the entry to the diary. Only admins can read or add entries to the diary.
    """

    key = "diary"
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        if not self.args:
            return self.display_diary()

        if create.create_message(
            self.account,
            self.args.strip(),
            locks="read:pperm(Admin)",
            tags=["admin_diary"],
        ):
            self.caller.msg("Diary entry added.")
        else:
            self.caller.msg("Failed to add diary entry.")

    def display_diary(self):
        entries = Msg.objects.get_by_tag("admin_diary").reverse()[:10]
        if not entries:
            return self.caller.msg("No diary entries found.")

        diary = evtable.EvTable(
            "|wAuthor|n",
            "|wDate|n",
            "",
            border="header",
            maxwidth=self.client_width(),
        )
        diary.reformat_column(0, valign="t", width=8)
        diary.reformat_column(1, valign="t", width=14)

        for entry in entries:
            diary.add_row(
                entry.senders[0].get_display_name(self.caller),
                entry.db_date_created.strftime("%b %d, %Y"),
                entry.message,
            )
        self.caller.msg("|rAdmin Diary|n:\n\n" + str(diary))


class CmdEcho(Command):
    """
    Echo a message to specified objects or all objects.

    Usage:
        echo[/switches] <objects> <message>

    Switches:
        all    - Echo to all objects.
        rooms  - Echo to objects in the same room as the caller.

    Arguments:
        objects - Comma-separated list of object names to echo to.
        message - The message to echo.

    Examples:
        echo player1, player2 Hello, world!
        echo/all Hello, everyone!

    This command allows administrators to send a message to specific objects
    or all objects in the game. If the 'all' switch is used or the command is
    invoked as 'aecho', the message will be echoed to all objects. If the
    'rooms' switch is used or the command is invoked as 'recho', the message
    will be echoed to objects in the same room as the caller.
    """

    key = "echo"
    aliases = ["aecho", "recho"]
    switch_options = ("all", "rooms")
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def parse(self):
        pattern = r"(\/[^ ]+)? ?([^ ]+)? (.+)"
        match = re.match(pattern, self.args)
        if match:
            self.switches = match.group(1).lstrip("/") if match.group(1) else ""
            self.objects = match.group(2).split(",") if match.group(2) else []
            self.message = match.group(3).strip()

    def func(self):
        if not self.message:
            self.caller.msg("Echo what?")
            return

        if self.cmdstring == "aecho" or "all" in self.switches:
            self.caller.msg("Echoing to all objects:")
            SESSIONS.announce_all(self.message)
            return

        if not self.objects:
            self.caller.msg("Syntax: echo[/switches] <objects> <message>")
            return

        echoed = set()
        locations = set()

        for obj_name in self.objects:
            obj = self.caller.search(obj_name, global_search=True)
            if not obj:
                continue

            if self.cmdstring == "recho" or "rooms" in self.switches:
                if obj.location not in locations:
                    obj.location.msg_contents(self.message)
                    echoed.update(obj.name for obj in obj.location.contents)
                    locations.add(obj.location)
            else:
                obj.msg(self.message)
                echoed.add(obj.name)

        self.caller.msg(f"Echoed to {', '.join(echoed)}: {self.message}")


class CmdForce(Command):
    """
    Admin command to force an object to execute a command.

    Usage:
        force <object> <command>

    This command allows administrators to force an object to execute a command.
    The <object> parameter specifies the name of the object to be forced, and
    the <command> parameter specifies the command to be executed by the object.

    Example:
        force jake look

    This will force the object named 'jake' to execute the 'look' command.
    """

    key = "force"
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        if not self.args:
            self.msg("Syntax: force <object> <command>")
            return

        args = self.args.split(None, 1)
        if len(args) < 2:
            self.msg("Syntax: force <object> <command>")
            return

        obj_name, command = args
        obj = self.account.search(obj_name, global_search=True, search_object=True)
        if not obj:
            self.msg(f"Object '{obj_name}' not found.")
            return

        obj.execute_cmd(command)
        self.msg(f"You force {obj} to {command}")


class CmdHome(Command):
    """
    Command to teleport the player to their home location.

    Usage:
      home

    This command allows the player to teleport to their home location.
    If the player has no home, they will receive a message indicating so.
    If the player is already at their home location, they will receive a
    message indicating so. Otherwise, the player will be teleported to
    their home location.
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
            self.msg_no_home()
        elif home == caller.location:
            self.msg_already_home()
        else:
            self.msg_teleport_home()
            caller.move_to(home, move_type="teleport")

    def msg_no_home(self):
        """Send message when player has no home"""
        self.caller.msg("You have no home!")

    def msg_already_home(self):
        """Send message when player is already at home"""
        self.caller.msg("You are already home!")

    def msg_teleport_home(self):
        """Send message when player is teleporting home"""
        self.caller.msg("There's no place like home ...")


class CmdReports(Command):
    """
    The `reports` command allows administrators to manage various types of reports, such as bugs and ideas.
    This command can display the latest reports or delete a specific report based on its ID.

    Usage:
        reports
            - Displays the latest 10 reports in a table format.

        reports delete <report_id>
            - Deletes the report with the specified ID.

    Examples:
        reports
            - This will display the latest 10 reports.

        reports delete 5
            - This will delete the report with ID 5.

    Notes:
        - The command will notify if no reports are found or if an invalid report ID is provided.
    """

    key = "reports"
    aliases = ["bugs", "ideas"]
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        report_type = self.cmdstring[:-1]
        reports = Msg.objects.get_by_tag(report_type)

        if not reports:
            return self.msg(f"No {self.cmdstring} found.")

        if not self.args:
            self.display_reports(reports)
        else:
            args = self.args.split(" ")
            if args[0] == "delete":
                self.delete_report(args)

    def display_reports(self, reports):
        table = evtable.EvTable(
            "|wID|n",
            "|wAuthor|n",
            "|wDate|n",
            "",
            border="header",
            maxwidth=self.client_width(),
        )
        table.reformat_column(0, valign="t", width=6)
        table.reformat_column(1, valign="t", width=8)
        table.reformat_column(2, valign="t", width=14)

        for report in reports.reverse()[:10]:
            table.add_row(
                report.id,
                report.senders[0].get_display_name(self.caller),
                report.db_date_created.strftime("%b %d, %Y"),
                report.message,
            )

        self.caller.msg(f"|w{self.cmdstring.capitalize()}|n:\n\n{str(table)}")

    def delete_report(self, args):
        if len(args) < 2:
            return self.msg(f"Please specify a {self.cmdstring[:-1]} ID.")
        elif not args[1].isdigit():
            return self.msg(f"Invalid {self.cmdstring[:-1]} ID.")

        report = Msg.objects.filter(id=args[1]).first()
        if report:
            report.delete()
            self.msg(f"{self.cmdstring[:-1]} deleted.")
        else:
            self.msg(f"{self.cmdstring[:-1]} not found.")


class CmdRestore(Command):
    """
    Command to restore a target character.

    Usage:
        restore <target>

    This command allows an admin to restore a target character. The target is searched globally, and if found, the target is restored. Both the caller and the target receive messages indicating the restoration.
    """

    key = "restore"
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        caller = self.caller
        args = self.args

        if not args:
            return caller.msg("Usage: restore <target>")

        target = caller.search(args, global_search=True)
        if not target:
            return

        target.at_restore()
        caller.msg(f"You restore {target.get_display_name(caller)}.")
        target.msg(f"{caller.get_display_name(target)} restores you.")


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
            self.obj_to_teleport = self.caller.search(self.lhs, global_search=True)
            if not self.obj_to_teleport:
                self.caller.msg("Did not find object to teleport.")
                raise InterruptCommand
            if all(char in self.rhs for char in ("(", ")", ",")):
                # search by (X,Y) or (X,Y,Z)
                self.search_by_xyz(self.rhs)
            else:
                # fallback to regular search by name/alias
                self.destination = self.caller.search(self.rhs, global_search=True)

        elif self.lhs:
            if all(char in self.lhs for char in ("(", ")", ",")):
                self.search_by_xyz(self.lhs)
            else:
                self.destination = self.caller.search(self.lhs, global_search=True)

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
            caller.msg("Usage: teleport[/switches] [<obj> =] <target or (X,Y,Z)>||home")
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
            caller.msg("You can't teleport an object inside something it holds!")
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


class CmdTransfer(Command):
    """
    Command to transfer an object to a different location.

    Usage:
      transfer <object>

    This command allows an admin to transfer an object to a different location.
    The object can be a room or an exit. The admin must have the necessary
    permission to control the object in order to transfer it.

    Args:
      <object> (str): The name or key of the object to transfer.

    Example:
      transfer sword
    """

    key = "transfer"
    aliases = ["trans"]
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("Syntax: transfer <object>")
            return

        obj_to_transfer = caller.search(self.args.strip(), global_search=True)
        if not obj_to_transfer:
            return

        if inherits_from(
            obj_to_transfer,
            ("typeclasses.rooms.Room", "typeclasses.exits.Exit"),
        ):
            caller.msg(
                f"You cannot transfer a {obj_to_transfer.__class__.__name__.lower()}."
            )
            return

        if obj_to_transfer.location == caller.location:
            caller.msg(f"{obj_to_transfer} is already here.")
            return

        if obj_to_transfer == caller.location:
            caller.msg("You cannot transfer an object to itself.")
            return

        if obj_to_transfer in caller.location.contents:
            caller.msg("You can't transfer an object inside something it holds!")
            return

        if not obj_to_transfer.access(caller, "control"):
            caller.msg(f"You do not have permission to transfer {obj_to_transfer}.")
            return

        success = obj_to_transfer.move_to(
            caller.location, emit_to_obj=caller, move_type="transfer"
        )
        caller.msg(
            f"You {'transfer' if success else 'fail to transfer'} {obj_to_transfer}."
        )


class CmdWatch(Command):
    """
    Command to start watching a character.

    Usage:
      watch <character>

    This command allows an admin to start watching a character. Once
    watching, the admin will receive updates about the character's
    actions and movements.
    """

    key = "watch"
    aliases = ["snoop"]
    locks = "cmd:perm(Admin)"
    help_category = "Admin"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            if caller.ndb._watching:
                self._stop_watching(caller)
                return

            return self.msg("Syntax: watch <character>")

        target = caller.search(self.args.strip(), global_search=True)
        if not target:
            self.msg("Character not found.")
            return

        if caller == target:
            return self.msg("You cannot watch yourself.")
        elif (watching := target.ndb._watching or None) and caller == watching:
            return self.msg(f"{target.name} is already watching you.")

        if caller.ndb._watching:
            self._stop_watching(caller)

        self._start_watching(caller, target)

    def _start_watching(self, watcher, target):
        watcher.ndb._watching = target
        if not target.ndb._watchers:
            target.ndb._watchers = list()
        target.ndb._watchers.append(watcher)
        self.msg(f"You start watching {target.name}.")

    def _stop_watching(self, watcher):
        target = watcher.ndb._watching
        target.ndb._watchers.remove(watcher)
        watcher.ndb._watching = None
        self.msg(f"You stop watching {target.name}.")
