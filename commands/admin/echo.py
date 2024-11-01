"""
Command module containing CmdEcho for sending messages to specified objects or groups.
"""

import re

from evennia.server.sessionhandler import SESSIONS

from commands.command import Command


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
        """
        Parse the command input to identify switches, target objects, and the message.
        """
        pattern = r"(\/[^ ]+)? ?([^ ]+)? (.+)"
        match = re.match(pattern, self.args)
        if match:
            self.switches = match.group(1).lstrip("/") if match.group(1) else ""
            self.objects = match.group(2).split(",") if match.group(2) else []
            self.message = match.group(3).strip()
        else:
            self.switches, self.objects, self.message = "", [], None

    def func(self):
        """
        Executes the echo command based on parsed switches and target objects.
        """
        if not self.message:
            self.caller.msg("Echo what?")
            return

        if self._is_global_echo():
            self._echo_to_all()
        elif not self.objects:
            self.caller.msg("Syntax: echo[/switches] <objects> <message>")
        else:
            self._echo_to_targets()

    def _is_global_echo(self):
        """Checks if the command is for global echo (aecho or /all switch)."""
        return self.cmdstring == "aecho" or "all" in self.switches

    def _echo_to_all(self):
        """Echoes the message to all connected sessions."""
        self.caller.msg("Echoing to all objects:")
        SESSIONS.announce_all(self.message)

    def _echo_to_targets(self):
        """
        Echoes the message to specified target objects or rooms based on switches.
        """
        echoed = set()
        locations = set()

        for obj_name in self.objects:
            obj = self.caller.search(obj_name, global_search=True)
            if not obj:
                continue

            if self._is_room_echo():
                self._echo_to_room(obj, echoed, locations)
            else:
                self._echo_to_object(obj, echoed)

        if echoed:
            self.caller.msg(f"Echoed to {', '.join(echoed)}: {self.message}")

    def _is_room_echo(self):
        """Checks if the command is for room-based echo (recho or /rooms switch)."""
        return self.cmdstring == "recho" or "rooms" in self.switches

    def _echo_to_room(self, obj, echoed, locations):
        """
        Echoes the message to all objects in the room of the specified object.

        Args:
            obj (Object): The object whose room will receive the message.
            echoed (set): Set of names that have received the message.
            locations (set): Set of rooms that have already received the message.
        """
        if obj.location and obj.location not in locations:
            obj.location.msg_contents(self.message)
            echoed.update(
                loc.get_display_name(self.caller) for loc in locations
            )
            locations.add(obj.location)

    def _echo_to_object(self, obj, echoed):
        """
        Echoes the message directly to the specified object.

        Args:
            obj (Object): The object to receive the message.
            echoed (set): Set of names that have received the message.
        """
        obj.msg(self.message)
        echoed.add(obj.get_display_name(self.caller))
