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
    "admire": {
        GESTURE.DEFAULT: "$You() $conj(admire) the view.",
        GESTURE.TARGET: "$You() $conj(admire) $you(target).",
        GESTURE.SELF: "$You() $conj(admire) $pron(yourself).",
    },
    "apologize": {
        GESTURE.DEFAULT: "$You() $conj(apologize).",
        GESTURE.TARGET: "$You() $conj(apologize) to $you(target).",
        GESTURE.SELF: "$You() $conj(apologize) to $pron(yourself).",
    },
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
    "brag": {
        GESTURE.DEFAULT: "$You() $conj(brag).",
        GESTURE.TARGET: "$You() $conj(brag) about $you(target).",
        GESTURE.SELF: "$You() $conj(brag) about $pron(yourself).",
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
    "cuddle": {
        GESTURE.DEFAULT: "$You() $conj(cuddle) yourself.",
        GESTURE.TARGET: "$You() $conj(cuddle) $you(target).",
        GESTURE.SELF: "$You() $conj(cuddle) $pron(yourself).",
    },
    "curtsy": {
        GESTURE.DEFAULT: "$You() $conj(curtsy).",
        GESTURE.TARGET: "$You() $conj(curtsy) towards $you(target).",
        GESTURE.SELF: "$You() $conj(curtsy) to $pron(yourself).",
    },
    "dance": {
        GESTURE.DEFAULT: "$You() $conj(dance).",
        GESTURE.TARGET: "$You() $conj(dance) with $you(target).",
        GESTURE.SELF: "$You() $conj(dance) with $pron(yourself).",
    },
    "flirt": {
        GESTURE.DEFAULT: "$You() $conj(flirt).",
        GESTURE.TARGET: "$You() $conj(flirt) with $you(target).",
        GESTURE.SELF: "$You() $conj(flirt) with $pron(yourself). So debutante.",
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
    "hug": {
        GESTURE.DEFAULT: "$You() $conj(hug) yourself.",
        GESTURE.TARGET: "$You() $conj(hug) $you(target).",
        GESTURE.SELF: "$You() $conj(hug) $pron(yourself).",
    },
    "jump": {
        GESTURE.DEFAULT: "$You() $conj(jump).",
        GESTURE.TARGET: "$You() $conj(jump) on $you(target).",
        GESTURE.SELF: "$You() $conj(jump) for $pron(yourself), because self-celebration is important.",
    },
    "kiss": {
        GESTURE.DEFAULT: "$You() $conj(kiss) the air.",
        GESTURE.TARGET: "$You() $conj(kiss) $you(target).",
        GESTURE.SELF: "$You() $conj(kiss) $pron(yourself).",
    },
    "nag": {
        GESTURE.DEFAULT: "$You() $conj(nag) everyone.",
        GESTURE.TARGET: "$You() $conj(nag) $you(target).",
        GESTURE.SELF: "$You() $conj(nag) $pron(yourself).",
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
    "poke": {
        GESTURE.DEFAULT: "$You() $conj(poke) yourself.",
        GESTURE.TARGET: "$You() $conj(poke) $you(target).",
        GESTURE.SELF: "$You() $conj(poke) $pron(yourself).",
    },
    "pray": {
        GESTURE.DEFAULT: "$You() $conj(pray).",
        GESTURE.TARGET: "$You() $conj(pray) for $you(target).",
        GESTURE.SELF: "$You() $conj(pray) for $pron(yourself).",
    },
    "rest": {
        GESTURE.DEFAULT: "$You() $conj(rest).",
        GESTURE.TARGET: "$You() $conj(rest) your eyes on $you(target).",
        GESTURE.SELF: "$You() $conj(rest). Clearly even $pron(you) $conj(tire) of $pron(yourself).",
    },
    "shake": {
        GESTURE.DEFAULT: "$You() $conj(shake) your head.",
        GESTURE.TARGET: "$You() $conj(shake) your head at $you(target).",
        GESTURE.SELF: "$You() $conj(shake) your head at $pron(yourself).",
    },
    "slap": {
        GESTURE.DEFAULT: "$You() $conj(slap) yourself.",
        GESTURE.TARGET: "$You() $conj(slap) $you(target).",
        GESTURE.SELF: "$You() $conj(slap) $pron(yourself).",
    },
    "snap": {
        GESTURE.DEFAULT: "$You() $conj(snap) your fingers.",
        GESTURE.TARGET: "$You() $conj(snap) your fingers at $you(target).",
        GESTURE.SELF: "$You() $conj(snap) your fingers at $pron(yourself).",
    },
    "snuggle": {
        GESTURE.DEFAULT: "$You() $conj(snuggle) yourself.",
        GESTURE.TARGET: "$You() $conj(snuggle) $you(target).",
        GESTURE.SELF: "$You() $conj(snuggle) $pron(yourself).",
    },
    "spin": {
        GESTURE.DEFAULT: "$You() $conj(spin) around.",
        GESTURE.TARGET: "$You() $conj(spin) around $you(target).",
        GESTURE.SELF: "$You() $conj(spin) around $pron(yourself), marveling at $pron(your) own magnificence.",
    },
    "squeeze": {
        GESTURE.DEFAULT: "$You() $conj(squeeze) yourself.",
        GESTURE.TARGET: "$You() $conj(squeeze) $you(target).",
        GESTURE.SELF: "$You() $conj(squeeze) $pron(yourself).",
    },
    "thank": {
        GESTURE.DEFAULT: "$You() $conj(thank) everyone.",
        GESTURE.TARGET: "$You() $conj(thank) $you(target).",
        GESTURE.SELF: "$You() $conj(thank) $pron(yourself).",
    },
    "tickle": {
        GESTURE.DEFAULT: "$You() $conj(tickle) yourself.",
        GESTURE.TARGET: "$You() $conj(tickle) $you(target).",
        GESTURE.SELF: "$You() $conj(tickle) $pron(yourself).",
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
    "wink": {
        GESTURE.DEFAULT: "$You() $conj(wink).",
        GESTURE.TARGET: "$You() $conj(wink) at $you(target).",
        GESTURE.SELF: "$You() $conj(wink) at $pron(yourself).",
    },
}


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
                gesture_type = GESTURE.SELF if target == caller else GESTURE.TARGET
            else:
                return

        caller.location.msg_contents(
            _GESTURES[self.cmdstring][gesture_type],
            from_obj=caller,
            mapping={"target": target} if gesture_type == GESTURE.TARGET else {},
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
