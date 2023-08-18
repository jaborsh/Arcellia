import re

from django.conf import settings

# from evennia.commands.default import admin
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import class_from_module
from server.conf.settings import SERVERNAME
from ui.formatting import wrap

from commands.command import Command

COMMAND_DEFAULT_CLASS = class_from_module(settings.COMMAND_DEFAULT_CLASS)


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


def echo_command(command_string):
    """
    Parses an echo command and handles optional switches, objects, and the message.

    The command follows the pattern "echo[/switches] [objects] message", where:
      - [/switches]: An optional part starting with a slash, followed by one or more non-space characters representing command switches.
      - [objects]: An optional part representing one or more non-space characters, typically a list of objects separated by commas.
      - message: The remaining part of the command, representing the message to be echoed.

    Examples:
      - "echo/switch1,switch2 obj1,obj2 This is the message." will identify the switches "switch1,switch2", the objects "obj1,obj2", and the message "This is the message."
      - "echo/switch This is the message." will identify the switch "switch", no objects, and the message "This is the message."
      - "echo This is the message." will identify no switches, no objects, and the message "This is the message."

    Args:
        command_string (str): The command string to be parsed.

    Returns:
        dict: A dictionary containing the parsed components: 'switches', 'objects', and 'message'.
    """

    pattern = r"echo(/[^ ]+)? ?([^ ]+)? (.+)"
    match = re.match(pattern, command_string)

    if match:
        match.group(1)[1:] if match.group(1) else None
