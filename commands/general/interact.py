from commands.command import Command
from menus.interaction_menu import InteractionMenu


class CmdInteract(Command):
    """
    Syntax: interact
            interact <target>

    This command allows the player to interact with the specified target.
    """

    key = "interact"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            if not (interaction := caller.location.db.interaction):
                return caller.msg("Interact with what?")
        else:
            target = caller.search(args)
            if not target:
                return

            if not (interaction := target.db.interaction):
                return caller.msg(
                    f"{target.get_display_name(caller)} is not interactive."
                )

        InteractionMenu(
            caller,
            interaction,
            startnode="node_start",
            auto_look=True,
            auto_help=True,
            cmd_on_exit="",
            persistent=True,
        )
