"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia.objects.objects import DefaultRoom
from evennia.utils.utils import lazy_property

from handlers import combat
from handlers.appearance import RoomAppearanceHandler

from .objects import Object


class Room(Object, DefaultRoom):
    """
    Modified Extended Room (Griatch)

    Room states:
      A room state is set as a Tag with category "roomstate" and tagkey "on_fire" or "flooded"
      etc).

    Alternative descriptions:
    - Add an Attribute `desc_<roomstate>` to the room, where <roomstate> is the name of the
      roomstate to use this for, like `desc_on_fire` or `desc_flooded`. If not given, seasonal
      descriptions given in desc_spring/summer/autumn/winter will be used, and last the
      regular `desc` Attribute.

    Alternative text sections
    - Used to add alternative text sections to the room description. These are embedded in the
      description by adding `$state(roomstate, txt)`. They will show only if the room is in the
      given roomstate. These are managed via the add/remove/get_alt_text methods.

    Details:
    - This is set as an Attribute `details` (a dict) on the room, with the detail name as key.
      When looking at this room, the detail name can be used as a target to look at without having
      to add an actual database object for it. The `detail` command is used to add/remove details.

    Room messages
    - Set `room_message_rate > 0` and add a list of `room_messages`. These will be randomly
      echoed to the room at the given rate.
    """

    def at_object_creation(self):
        """
        Called when the room is created.
        """
        super().at_object_creation()
        self.add_desc("This room is dark.", "dark")

    def basetype_setup(self):
        super().basetype_setup()
        self.locks.add(
            ";".join(
                [
                    "get:false()",
                    "puppet:false()",
                    "teleport:false()",
                    "teleport_here:true()",
                ]
            )
        )  # would be weird to puppet a room ...
        self.location = None

    @lazy_property
    def appearance(self):
        return RoomAppearanceHandler(self)

    @lazy_property
    def combat(self):
        return combat.CombatHandler(self, db_attribute_key="combat")

    # Methods
    def brighten(self, text=None, magical=False):
        if magical and self.tags.has("magical_dark", category="room_state"):
            self.tags.remove("magical_dark", category="room_state")
        elif self.tags.has("dark", category="room_state"):
            self.tags.remove("dark", category="room_state")
        else:
            return False

        if text:
            self.msg_contents(text)

        return True

    def darken(self, text=None, magical=False):
        if magical:
            if self.tags.has("magical_dark", category="room_state"):
                return False

            if self.tags.has("dark", category="room_state"):
                self.tags.remove("dark", category="room_state")

            self.tags.add("magical_dark", category="room_state")
        elif not self.tags.has("dark", category="room_state"):
            self.tags.add("dark", category="room_state")
        else:
            return False

        if text:
            self.msg_contents(text)

        return True
