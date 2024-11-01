from evennia.commands.default.building import (
    CmdListCmdSets as EvenniaCmdListCmdSets,
)


class CmdListCmdSets(EvenniaCmdListCmdSets):
    """
    Syntax: cmdsets <obj>

    This displays all cmdsets assigned to a user. Defaults to yourself.
    """

    key = "cmdsets"
    locks = "cmd:pperm(Developer)"
    help_category = "Developer"
