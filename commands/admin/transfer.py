from evennia.utils.utils import inherits_from

from commands.command import Command
from server.conf import logger


class CmdTransfer(Command):
    """
    Transfer an object to a different location.

    Syntax:
        transfer <object>

    Description:
        Allows an admin to transfer an object to a different location.
        The object can be any item except rooms or exits. The admin must have
        the necessary permissions to control the object in order to transfer it.

    Examples:
        transfer sword

    Switches:
        None

    Args:
        <object> (str): The name or key of the object to transfer.
    """

    key = "transfer"
    aliases = ["trans"]
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        """Execute the transfer command."""
        caller = self.caller
        obj_name = self.args.strip()

        if not obj_name:
            caller.msg("Syntax: transfer <object>")
            return

        obj_to_transfer = caller.search(obj_name, global_search=True)
        if not obj_to_transfer:
            caller.msg(f"Object '{obj_name}' not found.")
            return

        if not self.is_transferable(obj_to_transfer):
            return

        if obj_to_transfer.location == caller.location:
            caller.msg(f"{obj_to_transfer} is already here.")
            return

        if obj_to_transfer == caller.location:
            caller.msg("You cannot transfer an object to itself.")
            return

        if self.is_object_inside_caller_location(obj_to_transfer):
            caller.msg(
                "You can't transfer an object inside something it holds!"
            )
            return

        if not self.has_transfer_permission(obj_to_transfer):
            return

        self.perform_transfer(obj_to_transfer, caller.location)

    def is_transferable(self, obj):
        """
        Check if the object is eligible for transfer.

        Args:
            obj: The object to check.

        Returns:
            bool: True if transferable, False otherwise.
        """
        if inherits_from(
            obj, ("typeclasses.rooms.Room", "typeclasses.exits.Exit")
        ):
            caller = self.caller
            caller.msg(
                f"You cannot transfer a {obj.__class__.__name__.lower()}."
            )
            return False
        return True

    def is_object_inside_caller_location(self, obj):
        """
        Determine if the object is inside the caller's location.

        Args:
            obj: The object to check.

        Returns:
            bool: True if the object is inside the caller's location, False otherwise.
        """
        return obj in self.caller.location.contents

    def has_transfer_permission(self, obj):
        """
        Check if the caller has permission to transfer the object.

        Args:
            obj: The object to transfer.

        Returns:
            bool: True if the caller has permission, False otherwise.
        """
        caller = self.caller
        if not obj.access(caller, "control"):
            caller.msg(f"You do not have permission to transfer {obj}.")
            return False
        return True

    def perform_transfer(self, obj, destination):
        """
        Perform the transfer of the object to the destination.

        Args:
            obj: The object to transfer.
            destination: The target location.
        """
        success = obj.move_to(
            destination, emit_to_obj=self.caller, move_type="transfer"
        )
        if success:
            self.caller.msg(f"You have transferred {obj} to {destination}.")
            logger.log_info(
                f"{self.caller} transferred {obj} to {destination}."
            )
        else:
            self.caller.msg(f"Failed to transfer {obj}.")
