from evennia.commands.default import batchprocess


class CmdBatchCode(batchprocess.CmdBatchCode):
    """
    Syntax: batchcode[/interactive] <python path to file>

    Switch:
       interactive - this mode will offer more control when
                     executing the batch file, like stepping,
                     skipping, reloading etc.
       debug - auto-delete all objects that has been marked as
               deletable in the script file (see example files for
               syntax). This is useful so as to to not leave multiple
               object copies behind when testing out the script.

    Runs batches of commands from a batch-code text file (*.py).
    """

    key = "batchcode"
    aliases = ["batchcodes"]
    switch_options = ("interactive", "debug")
    locks = "cmd:superuser()"
    help_category = "System"
