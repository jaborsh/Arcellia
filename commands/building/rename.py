"""
Rename command module.
"""

from evennia.commands.default.building import ObjManipCommand
from evennia.utils.utils import inherits_from

from server.conf import logger
from utils.colors import strip_ansi


class CmdRename(ObjManipCommand):
    """
    Syntax: rename [*]<obj> <new name>[;alias,alias,...]

    Rename an object to something new. Use *obj to rename an account.

    Note: What is written as the 'new name' will be the object's new display
          string. Any aliases provided will not be shown visibly, but can be
          used to reference the item.
    """

    key = "rename"
    locks = "perm(Builder)"
    help_category = "Building"

    def func(self):
        caller = self.caller
        args = self.args.strip().split(" ", 1)
        if len(args) < 2:
            caller.msg("Syntax: rename <obj> <new name>[;alias,alias,...]")
            return

        obj_name, rest = args
        if ";" in rest:
            new_name, aliases = rest.split(";", 1)
            aliases = [
                strip_ansi(alias.strip()) for alias in aliases.split(",")
            ]
        else:
            new_name = rest
            aliases = None

        if not new_name:
            caller.msg("No new name given.")
            return

        if new_name.startswith("|") and not new_name.endswith("|n"):
            new_name += "|n"

        new_key = strip_ansi(new_name)
        if obj_name.startswith("*"):
            # rename an account
            obj = caller.account.search(obj_name.lstrip("*"))
            if not obj:
                return

            if aliases:
                caller.msg("Accounts cannot have aliases.")
                return

            if not (
                obj.access(caller, "control") or obj.access(caller, "edit")
            ):
                caller.msg(
                    f"You don't have permission to rename {obj.username}."
                )
                return

            logger.log_sec(
                f"Rename: {caller} renamed {obj.username} to {new_key} (Account)."
            )
            caller.msg(f"Account {obj.username} renamed to {new_key}.")
            obj.username = new_key
            obj.save()
            obj.msg(f"Your account was renamed to {obj.username}.")
        else:
            # rename an object
            obj = caller.search(obj_name)
            if not obj:
                return

            if not (
                obj.access(caller, "control") or obj.access(caller, "edit")
            ):
                caller.msg(f"You don't have permission to rename {obj.name}.")
                return

            if inherits_from(obj, "typeclasses.characters.Character"):
                aliases = None
                logger.log_sec(
                    f"Rename: {caller} renamed {obj.name} to {new_name} (Character)."
                )

            obj.key = new_key
            obj.display_name = new_name
            astring = ""
            if aliases:
                obj.aliases.clear()
                [obj.aliases.add(alias) for alias in aliases]
                astring = " (aliases: %s)" % ", ".join(aliases)

            if obj.destination:
                obj.flush_from_cache(force=True)

            type = obj.typeclass_path.split(".")[-1] or "Object"
            caller.msg(f"{type} {obj_name} renamed to {new_name}{astring}.")
            obj.msg(f"You've been renamed to {new_name}{astring}.")
