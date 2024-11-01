"""
Purge command module.
"""

from django.conf import settings
from evennia.utils.utils import inherits_from

from commands.command import Command
from typeclasses.characters import Character as CharacterTypeclass

CHAR_TYPECLASS = settings.BASE_CHARACTER_TYPECLASS
ROOM_TYPECLASS = settings.BASE_ROOM_TYPECLASS


class CmdPurge(Command):
    """
    Command to delete all items in the current location.

    Syntax: purge

    This command deletes all contents in the current location.
    """

    key = "purge"
    locks = "cmd:perm(Builder)"
    help_category = "Building"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            for obj in caller.location.contents:
                if inherits_from(obj, CHAR_TYPECLASS):
                    continue
                obj.delete()
            return caller.msg("You purge the room's contents.")

        target = caller.search(args)
        if not target:
            return
        if inherits_from(target, CharacterTypeclass):
            return caller.msg("You cannot purge a character.")
        elif inherits_from(target, ROOM_TYPECLASS):
            return caller.msg("You cannot purge a room.")

        caller.msg(f"{target.get_display_name(caller)} purged.")
        target.delete()
