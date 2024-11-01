"""
Command module containing CmdEcho.
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
