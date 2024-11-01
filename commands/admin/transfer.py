from evennia.utils.utils import inherits_from

from commands.command import Command
from server.conf import logger


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
            caller.msg(
                "You can't transfer an object inside something it holds!"
            )
            return

        if not obj_to_transfer.access(caller, "control"):
            caller.msg(
                f"You do not have permission to transfer {obj_to_transfer}."
            )
            return

        success = obj_to_transfer.move_to(
            caller.location, emit_to_obj=caller, move_type="transfer"
        )
        caller.msg(
            f"You {'transfer' if success else 'fail to transfer'} {obj_to_transfer}."
        )
        logger.log_info(
            f"{caller} transferred {obj_to_transfer} to {caller.location}."
        )
