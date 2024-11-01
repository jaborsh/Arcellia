"""
Set gender command module.
"""

from commands.command import Command


class CmdSetGender(Command):
    """
    Syntax: setgender <target> <gender>

    Genders Available:
        male       (he, him, his)
        female     (she, her, hers)
        neutral    (it, its)
        ambiguous  (they, them, their, theirs)
    """

    key = "setgender"
    locks = "cmd:perm(Builder)"
    help_category = "Building"

    gender_map = {
        "m": "male",
        "f": "female",
        "n": "neutral",
        "a": "ambiguous",
    }

    def func(self):
        caller = self.caller
        args = self.args.split(" ", 1)
        if len(args) < 2:
            return caller.msg(
                "Syntax: gender [m]ale || [f]emale || [n]eutral || [a]mbiguous"
            )

        target, gender = args
        target = caller.search(target, global_search=True)
        if not target:
            return

        if not (
            target.access(caller, "control") or target.access(caller, "edit")
        ):
            return caller.msg(
                f"You don't have permission to regender {target.display_name}."
            )

        if gender[0] not in ("m", "f", "n", "a"):
            return caller.msg(
                "Syntax: gender [m]ale || [f]emale || [n]eutral || [a]mbiguous"
            )

        target.gender.value = self.gender_map[gender[0]]
        caller.msg(
            f"{target.display_name} has been assigned the {target.gender.value} gender."
        )
        target.msg(f"You've been assigned the {target.gender.value} gender.")
