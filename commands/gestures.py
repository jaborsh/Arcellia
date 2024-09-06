from enum import Enum

from commands.command import Command

__all__ = (
    "CmdGesture",
    "CmdGestures",
)


class GESTURE(Enum):
    DEFAULT = 0
    TARGET = 1
    SELF = 2


_GESTURES = {
    "beckon": {
        GESTURE.DEFAULT: "$You() $conj(beckon).",
        GESTURE.TARGET: "$You() $conj(beckon) to $you(target).",
        GESTURE.SELF: "$You() $conj(beckon) to $pron(yourself), because $pron(you) clearly need $pron(your) own attention.",
    },
    "bow": {
        GESTURE.DEFAULT: "$You() $conj(bow).",
        GESTURE.TARGET: "$You() $conj(bow) to $you(target).",
        GESTURE.SELF: "$You() $conj(bow) to $pron(yourself), acknowledging $pron(your) own greatness.",
    },
    "calm": {
        GESTURE.DEFAULT: "$You() $conj(calm) down.",
        GESTURE.TARGET: "$You() $conj(calm) $you(target) down.",
        GESTURE.SELF: "$You() $conj(calm) $pron(yourself) down.",
    },
    "clap": {
        GESTURE.DEFAULT: "$You() $conj(clap) $pron(your) hands.",
        GESTURE.TARGET: "$You() $conj(clap) for $you(target).",
        GESTURE.SELF: "$You() $conj(clap) for $pron(yourself).",
    },
    "cry": {
        GESTURE.DEFAULT: "$You() $conj(cry).",
        GESTURE.TARGET: "$You() $conj(cry) at the sight of $you(target).",
        GESTURE.SELF: "$You() $conj(cry) to $pron(yourself), because no one else understands.",
    },
    "curtsy": {
        GESTURE.DEFAULT: "$You() $conj(curtsy).",
        GESTURE.TARGET: "$You() $conj(curtsy) towards $you(target).",
        GESTURE.SELF: "$You() $conj(curtsy) to $pron(yourself).",
    },
    "gesture": {
        GESTURE.DEFAULT: "$You() $conj(gesture).",
        GESTURE.TARGET: "$You() $conj(gesture) at $you(target).",
        GESTURE.SELF: "$You() $conj(gesture) at $pron(yourself).",
    },
    "greet": {
        GESTURE.DEFAULT: "$You() $conj(greet) everyone.",
        GESTURE.TARGET: "$You() $conj(greet) $you(target).",
        GESTURE.SELF: "$You() $conj(greet) $pron(yourself).",
    },
    "grovel": {
        GESTURE.DEFAULT: "$You() $conj(grovel) before everyone.",
        GESTURE.TARGET: "$You() $conj(grovel) at $your(target) feet.",
        GESTURE.SELF: "$You() $conj(grovel) before $pron(yourself), because even $pron(you) $pconj(are) not worthy of $pron(your) own respect.",
    },
    "jump": {
        GESTURE.DEFAULT: "$You() $conj(jump).",
        GESTURE.TARGET: "$You() $conj(jump) on $you(target).",
        GESTURE.SELF: "$You() $conj(jump) for $pron(yourself), because self-celebration is important.",
    },
    "nod": {
        GESTURE.DEFAULT: "$You() $conj(nod).",
        GESTURE.TARGET: "$You() $conj(nod) at $you(target).",
        GESTURE.SELF: "$You() $conj(nod) at $pron(yourself).",
    },
    "point": {
        GESTURE.DEFAULT: "$You() $conj(point).",
        GESTURE.TARGET: "$You() $conj(point) at $you(target).",
        GESTURE.SELF: "$You() $conj(point) at $pron(yourself).",
    },
    "pray": {
        GESTURE.DEFAULT: "$You() $conj(pray).",
        GESTURE.TARGET: "$You() $conj(pray) for $you(target).",
        GESTURE.SELF: "$You() $conj(pray) for $pron(yourself).",
    },
    "rest": {
        GESTURE.DEFAULT: "$You() $conj(rest).",
        GESTURE.TARGET: "$You() $conj(rest) your eyes on $you(target).",
        GESTURE.SELF: "$You() $conj(rest). Clearly even $pron(you) tire of $pron(yourself).",
    },
    "shake": {
        GESTURE.DEFAULT: "$You() $conj(shake) your head.",
        GESTURE.TARGET: "$You() $conj(shake) your head at $you(target).",
        GESTURE.SELF: "$You() $conj(shake) your head at $pron(yourself).",
    },
    "snap": {
        GESTURE.DEFAULT: "$You() $conj(snap) your fingers.",
        GESTURE.TARGET: "$You() $conj(snap) your fingers at $you(target).",
        GESTURE.SELF: "$You() $conj(snap) your fingers at $pron(yourself).",
    },
    "spin": {
        GESTURE.DEFAULT: "$You() $conj(spin) around.",
        GESTURE.TARGET: "$You() $conj(spin) around $you(target).",
        GESTURE.SELF: "$You() $conj(spin) around $pron(yourself), marveling at $pron(your) own magnificence.",
    },
    "thank": {
        GESTURE.DEFAULT: "$You() $conj(thank) everyone.",
        GESTURE.TARGET: "$You() $conj(thank) $you(target).",
        GESTURE.SELF: "$You() $conj(thank) $pron(yourself).",
    },
    "wait": {
        GESTURE.DEFAULT: "$You() $conj(wait).",
        GESTURE.TARGET: "$You() $conj(wait) for $you(target).",
        GESTURE.SELF: "$You() $conj(wait) for $pron(yourself).",
    },
    "wave": {
        GESTURE.DEFAULT: "$You() $conj(wave).",
        GESTURE.TARGET: "$You() $conj(wave) at $you(target).",
        GESTURE.SELF: "$You() $conj(wave) to $pron(your) biggest fan: $pron(yourself).",
    },
    "welcome": {
        GESTURE.DEFAULT: "$You() $conj(welcome) everyone.",
        GESTURE.TARGET: "$You() $conj(welcome) $you(target).",
        GESTURE.SELF: "$You() $conj(welcome) $pron(yourself).",
    },
}


class CmdGesture(Command):
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


class CmdGestures(Command):
    """
    This command displays a list of available gestures to the caller.

    Usage:
      gestures
      gesturelist
    """

    key = "gestures"
    aliases = "gesturelist"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        caller.msg("Available gestures:")
        for gesture in _GESTURES.keys():
            caller.msg(f"  {gesture}")
