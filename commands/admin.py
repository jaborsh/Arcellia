import re

from django.conf import settings
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import class_from_module
from evennia.utils.utils import inherits_from
from server.conf import logger
from server.conf.settings import SERVERNAME
from ui.formatting import wrap

from commands.command import Command

COMMAND_DEFAULT_CLASS = class_from_module(settings.COMMAND_DEFAULT_CLASS)

__all__ = (
    "CmdAnnounce",
    "CmdEcho",
    "CmdForce",
    "CmdHome",
    "CmdTeleport",
    "CmdTransfer",
    "CmdWatch",
)


class CmdAnnounce(Command):
    """
    Usage: announce <message>

    Announces a message to all connected sessions including all currently
    disconnected.
    """

    key = "announce"
    locks = "cmd:perm(announce) or perm(Admin)"
    help_category = "Admin"

    def func(self):
        if not self.args:
            self.caller.msg("Usage: announce <message>")
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
    Usage: echo[/switch] <objects> <message>

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
            caller.msg("Usage: echo[/switches] <objects> <message>")
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
    Usage: force <object> <command>

    Forces an object to execute a command.
    """

    key = "force"
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        if not self.args:
            self.msg("Usage: force <object> <command>")

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
    Usage: home

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


class CmdTeleport(COMMAND_DEFAULT_CLASS):
    """
    Usage: tel[/switch] <target>
           goto[/switch] <target>

    Switches:
        quiet    - don't echo leave/arrive messages to the source/target
                   locations for the move.
        intoexit - if target is an exit, teleport INTO the exit object
                   instead of to its destination.

    Examples:
        tel Limbo
        tel/quiet Limbo

    Teleports an object somewhere. If no object is given, you yourself are
    teleported to the target location.

    To lock an object from being teleported, set its `teleport` lock, it will
    be checked with the caller. To block a destination from being teleported
    to, set the destination's `teleport_here` lock - it will be checked with
    the thing being teleported. Admins and higher permissions can always
    teleport.
    """

    key = "teleport"
    aliases = ["tel", "goto"]
    switch_options = ("quiet", "intoexit")
    locks = "cmd:perm(Admin)"
    help_category = "Admin"

    def func(self):
        caller = self.caller

        if not self.args:
            caller.msg("Usage: tel[/switch] <target>")
            return

        destination = self.args.strip()
        destination = caller.search(destination, global_search=True)

        if not destination:
            return

        if "intoexit" in self.switches and not destination.destination:
            caller.msg("You cannot teleport INTO a non-exit object.")
            return

        if inherits_from(destination, "typeclasses.characters.Character"):
            log_msg = f"{caller} teleported to {destination}."
        destination = destination.location if destination.location else destination

        if caller.location == destination:
            caller.msg("You are already here.")
            return

        if caller.move_to(
            destination,
            quiet="quiet" in self.switches,
            emit_to_obj=caller,
            use_destination="intoexit" not in self.switches,
            move_type="teleport",
        ):
            caller.msg(f"You teleport to {destination}.")
            if log_msg:
                logger.log_sec(log_msg)
        else:
            caller.msg(f"You fail to teleport to {destination}.")


class CmdTransfer(COMMAND_DEFAULT_CLASS):
    """
    Usage: transfer <object>

    Transfers an object to your current location.
    """

    key = "transfer"
    locks = "cmd:perm(Admin)"
    help_category = "Admin"

    def func(self):
        caller = self.caller

        if not self.args:
            caller.msg("Usage: transfer <object>")
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
    key = "watch"
    aliases = ["snoop"]

    def func(self):
        caller = self.caller
        if caller.ndb._watching:
            # Remove the caller from the old target's watchers list
            caller.ndb._watching.ndb._watchers.remove(caller)
            self.msg(f"You stop watching {caller.ndb._watching}.")
            caller.ndb._watching = None
        elif not self.args:
            self.msg("Usage: watch <character>")
            return

        target = self.account.search(self.args.strip(), search_object=True)
        if not target:
            return

        # Set up the watch
        self.msg(f"Watching {target.name}.")
        caller.ndb._watching = target
        target.ndb._watchers = target.ndb._watchers or []
        target.ndb._watchers.append(caller)
