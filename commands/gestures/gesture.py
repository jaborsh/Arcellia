from commands.command import Command
from commands.gestures.gestures import _GESTURES, GESTURE


class CmdGesture(Command):
    """
    Command to perform a gesture.

    Usage:
        <gesture> [target]

    Description:
        This command allows you to perform a gesture, either to yourself or directed at a target.
        Gestures can be a powerful way to express emotions, intentions, or actions in the game world.

    Examples:
        wave
        nod Alice
    """

    key = "gesture"
    aliases = list(_GESTURES.keys())
    locks = "cmd:all()"
    auto_help = False

    def func(self):
        caller = self.caller
        gesture_type = GESTURE.DEFAULT

        if self.args:
            if target := caller.search(self.args.strip().split(" ")[0]):
                gesture_type = (
                    GESTURE.SELF if target == caller else GESTURE.TARGET
                )
            else:
                return

        caller.location.msg_contents(
            _GESTURES[self.cmdstring][gesture_type],
            from_obj=caller,
            mapping={"target": target}
            if gesture_type == GESTURE.TARGET
            else {},
        )
