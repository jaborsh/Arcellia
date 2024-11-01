from evennia.commands.default import batchprocess


class CmdBatchCommands(batchprocess.CmdBatchCommands):
    """
    Syntax: batchcommands[/interactive] <python.path.to.file>

    Switch:
       interactive - this mode will offer more control when
                     executing the batch file, like stepping,
                     skipping, reloading etc.

    Runs batches of commands from a batch-cmd text file (*.ev).
    """

    key = "batchcommands"
    aliases = ["batchcommand", "batchcmd"]
    switch_options = ("interactive",)
    locks = "cmd:pperm(Developer)"
    help_category = "System"
