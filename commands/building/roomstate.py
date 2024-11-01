"""
Room state command module.
"""

from evennia import InterruptCommand
from evennia.utils.utils import list_to_string

from commands.command import Command


class CmdRoomState(Command):
    """
    Toggle and view room state for the current room.

    Usage:
        roomstate [<roomstate>]

    Examples:
        roomstate spring
        roomstate burning
        roomstate burning      (a second time toggles it off)

    If the roomstate was already set, it will be disabled. Use
    without arguments to see the roomstates on the current room.
    """

    key = "roomstate"
    locks = "cmd:perm(Builder)"
    help_category = "Building"

    def parse(self):
        super().parse()
        self.room = self.caller.location
        if not self.room or not hasattr(self.room, "room_states"):
            self.caller.msg(
                "You have no current location, or it doesn't support room states."
            )
            raise InterruptCommand()

        self.room_state = self.args.strip().lower()

    def func(self):
        caller = self.caller
        room = self.room
        room_state = self.room_state

        if room_state:
            # toggle room state
            if room_state in room.room_states:
                room.remove_room_state(room_state)
                caller.msg(f"Cleared room state '{room_state}' from this room.")
            else:
                room.add_room_state(room_state)
                caller.msg(f"Added room state '{room_state}' to this room.")
        else:
            # view room states
            room_states = list_to_string(
                [f"'{state}'" for state in room.room_states]
                if room.room_states
                else ("None",)
            )
            caller.msg(
                "Room states (not counting automatic time/season) on"
                f" {room.get_display_name(caller)}:\n {room_states}"
            )
