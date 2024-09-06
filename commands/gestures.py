from commands.command import Command
from utils.text import grammarize

__all__ = (
    "CmdBeckon",
    "CmdBow",
    "CmdCalm",
    "CmdClap",
    "CmdCrouch",
    "CmdCry",
    "CmdCurtsy",
    "CmdDejection",
    "CmdDoze",
    "CmdErudition",
    "CmdFlex",
    "CmdGreet",
    "CmdGrovel",
    "CmdHmm",
    "CmdJump",
    "CmdNod",
    "CmdPoint",
    "CmdPray",
    "CmdRepent",
    "CmdRest",
    "CmdSit",
    "CmdSnap",
    "CmdSpin",
    "CmdThank",
    "CmdWait",
    "CmdWave",
    "CmdWelcome",
)


class Gesture(Command):
    locks = "cmd:all()"
    message = ""
    auto_help = False

    def func(self):
        message = (
            grammarize(f"{self.message} {self.args}")
            if self.args
            else grammarize(self.message)
        )
        self.caller.location.msg_contents(message, from_obj=self.caller)


class CmdBeckon(Gesture):
    key = "beckon"
    message = "$You() $conj(beckon)"


class CmdBow(Gesture):
    key = "bow"
    message = "$You() $conj(bow)"


class CmdCalm(Gesture):
    key = "calm"
    message = "$You() $conj(raise) $pron(your,pa) hands in a calming gesture"


class CmdClap(Gesture):
    key = "clap"
    message = "$You() $conj(clap)"


class CmdCrouch(Gesture):
    key = "crouch"
    message = "$You() $conj(crouch)"


class CmdCry(Gesture):
    key = "cry"
    message = "$You() $conj(cry)"


class CmdCurtsy(Gesture):
    key = "curtsy"
    message = "$You() $conj(curtsy)"


class CmdDejection(Gesture):
    key = "dejection"
    message = "$You() $conj(lower) $pron(your,pa) gaze in dejection"


class CmdDoze(Gesture):
    key = "doze"
    message = "$Your() head droops as $pron(you) $conj(doze) off"


class CmdErudition(Gesture):
    key = "erudition"
    message = "$You() $conj(adjust) $pron(your,pa) posture, exuding erudition"


class CmdGreet(Gesture):
    key = "greet"
    message = "$You() $conj(greet)"


class CmdGrovel(Gesture):
    key = "grovel"
    message = "$You() $conj(grovel)"


class CmdFlex(Gesture):
    key = "flex"
    message = "$You() $conj(flex)"


class CmdHmm(Gesture):
    key = "hmm"
    message = '$You() $conj(utter) a soft "hmm."'


class CmdJump(Gesture):
    key = "jump"
    message = "$You() $conj(jump)"


class CmdNod(Gesture):
    key = "nod"
    message = "$You() $conj(nod)"


class CmdPoint(Gesture):
    key = "point"
    message = "$You() $conj(point)"


class CmdPray(Gesture):
    key = "pray"
    message = "$You() $conj(pray)"


class CmdRepent(Gesture):
    key = "repent"
    message = "$You() $conj(drop) to $pron(your,pa) knees in repentance"


class CmdRest(Gesture):
    key = "rest"
    message = "$You() $conj(rest)"


class CmdSit(Gesture):
    key = "sit"
    message = "$You() $conj(sit)"


class CmdSpin(Gesture):
    key = "spin"
    message = "$You() $conj(spin)"


class CmdSnap(Gesture):
    key = "snap"
    message = "$You() $conj(snap) $pron(your,pa) fingers"


class CmdThank(Gesture):
    key = "thank"
    message = "$You() $conj(express) thanks"


class CmdWait(Gesture):
    key = "wait"
    message = "$You() $conj(wait)"


class CmdWave(Gesture):
    key = "wave"
    message = "$You() $conj(wave)"


class CmdWelcome(Gesture):
    key = "welcome"
    message = "$You() $conj(spread) $pron(your,pa) arms in welcome"
