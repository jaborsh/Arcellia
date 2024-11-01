from evennia import syscmdkeys

from commands.command import Command


class CmdNoInput(Command):
    """
    Command class for handling cases where no input is provided.

    This command is triggered when the player enters a command without any input.
    It does not perform any action and simply returns without doing anything.
    """

    key = syscmdkeys.CMD_NOINPUT
    locks = "cmd:all()"
    auto_help = False

    def func(self):
        pass
