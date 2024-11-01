from commands.command import Command
from typeclasses.clothing import Clothing


class CmdUncover(Command):
    """
    Syntax: uncover <clothing>

    This command allows a character to uncover a specific clothing object that
    is currently covered by another clothing object. The command takes one
    argument, which is the name or key of the object to be uncovered.
    """

    key = "uncover"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            return caller.msg("Uncover what?")

        obj = caller.search(args, candidates=caller.contents)
        if not obj:
            return

        if not isinstance(obj, Clothing):
            return caller.msg("You can't uncover that.")

        if not obj.covered_by:
            return caller.msg(
                f"{obj.get_display_name(caller)} isn't covered by anything."
            )

        for cover in obj.covered_by:
            cover.covering.remove(obj)
            obj.covered_by.remove(cover)

            caller.location.msg_contents(
                f"$You() $conj(uncover) {obj.get_display_name(caller)} from beneath {cover.get_display_name(caller)}.",
                from_obj=caller,
            )
