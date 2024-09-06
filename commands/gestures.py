from commands.command import Command
from utils.text import grammarize

__all__ = (
    "CmdBeckon",
    "CmdBow",
    "CmdBravo",
    "CmdCalm",
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
    message = "$You() $conj(curl) $pron(your,pa) fingers in a slow, beckoning gesture."


class CmdBow(Gesture):
    key = "bow"
    message = "$You() $conj(lower) $pron(your,pa) head and $conj(bow)"


class CmdBravo(Gesture):
    key = "bravo"
    message = "$You() $conj(clap) $pron(your,pa) hands together in a show of appreciation and approval"


class CmdCalm(Gesture):
    key = "calm"
    message = "$You() $conj(raise) $pron(your,pa) hands in a calming gesture"


class CmdCrouch(Gesture):
    key = "crouch"
    message = "$You() $conj(bend) $pron(your,pa) knees into a crouch"


class CmdCry(Gesture):
    key = "cry"
    message = "Tears well up in $your() eyes and $you() $conj(cry)"


class CmdCurtsy(Gesture):
    key = "curtsy"
    message = "$You() gracefully $conj(lower) $pron(yourself) into a curtsy"


class CmdDejection(Gesture):
    key = "dejection"
    message = "$You() $conj(lower) $pron(your,pa) gaze and $conj(sigh) heavily, $pron(your,pa) entire demeanor radiating dejection"


class CmdDoze(Gesture):
    key = "doze"
    message = "$Your() head droops, slipping into a light doze"


class CmdErudition(Gesture):
    key = "erudition"
    message = "$You() $conj(adjust) $pron(your,pa) posture, $conj(lift) $pron(your,pa) chin, and $conj(touch) $pron(your,pa) fingertips together, exuding an air of scholarly erudition"


class CmdGreet(Gesture):
    key = "greet"
    message = "$You() $conj(offer) a warm greeting"


class CmdGrovel(Gesture):
    key = "grovel"
    message = "$You() $conj(fall) to the ground, groveling with utter humility"


class CmdFlex(Gesture):
    key = "flex"
    message = (
        "$You() $conj(tense) $pron(your,pa) muscles and $conj(flex) with confidence"
    )


class CmdHmm(Gesture):
    key = "hmm"
    message = '$You() $conj(utter) a soft "hmm."'


class CmdJump(Gesture):
    key = "jump"
    message = "$You() $conj(bend) $pron(your,pa) knees and $conj(jump) into the air"


class CmdNod(Gesture):
    key = "nod"
    message = "$You() $conj(nod)"


class CmdPoint(Gesture):
    key = "point"
    message = "$You() $conj(extend) $pron(your,pa) finger, pointing"


class CmdPray(Gesture):
    key = "pray"
    message = "$You() $conj(clasp) $pron(your,pa) hands together in prayer"


class CmdRepent(Gesture):
    key = "repent"
    message = (
        "$You() $conj(drop) to $pron(your,pa) knees in a deep expression of repentance"
    )


class CmdRest(Gesture):
    key = "rest"
    message = "$You() $conj(sit) down slowly, $conj(lean) back with a deep exhale, and $conj(allow) $pron(yourself) a moment of rest"


class CmdSit(Gesture):
    key = "sit"
    message = "$You() $conj(sit)"


class CmdSpin(Gesture):
    key = "spin"
    message = "$You() $conj(pivot) on $pron(your,pa) heel and $conj(spin)"


class CmdSnap(Gesture):
    key = "snap"
    message = "$You() $conj(snap) $pron(your,pa) fingers"


class CmdThank(Gesture):
    key = "thank"
    message = "$You() $conj(express) $pron(your,pa) thanks"


class CmdWait(Gesture):
    key = "wait"
    message = "$You() $conj(wait)"


class CmdWave(Gesture):
    key = "wave"
    message = "$You() $conj(lift) $pron(your,pa) hand and $conj(wave)"


class CmdWelcome(Gesture):
    key = "welcome"
    message = "$You() $conj(spread) $pron(your,pa) arms wide in an open welcome"
