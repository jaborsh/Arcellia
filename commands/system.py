from commands.command import Command
from evennia import syscmdkeys
from evennia.commands.default import batchprocess, building, system

__all__ = (
    "CmdNoInput",
    "CmdAccounts",
    "CmdBatchCommands",
    "CmdBatchCode",
    "CmdObjects",
    "CmdPy",
    "CmdReload",
    "CmdReset",
    "CmdScripts",
    "CmdService",
    "CmdShutdown",
    "CmdTasks",
)


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


class CmdAccounts(system.CmdAccounts):
    """
    Syntax: accounts [nr]
            accounts/delete <name or #id> [: reason]

    Switches:
      delete    - delete an account from the server

    By default, lists statistics about the Accounts registered with the game.
    It will list the <nr> amount of latest registered accounts
    If not given, <nr> defaults to 10.
    """

    key = "accounts"
    aliases = ["account"]
    help_category = "System"


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


class CmdObjects(building.CmdObjects):
    """
    Syntax: objects [<nr>]

    Gives statictics on objects in database as well as a list of <nr> latest
    objects in database. If not given, <nr> defaults to 10.
    """

    key = "objects"
    aliases = ["objs"]
    help_category = "System"


class CmdPy(system.CmdPy):
    """
    Syntax: py [cmd]
            py/edit
            py/time <cmd>
            py/clientraw <cmd>
            py/noecho

    Switches:
      time - output an approximate execution time for <cmd>
      edit - open a code editor for multi-line code experimentation
      clientraw - turn off all client-specific escaping. Note that this may
        lead to different output depending on prototocol (such as angular brackets
        being parsed as HTML in the webclient but not in telnet clients)
      noecho - in Python console mode, turn off the input echo (e.g. if your client
        does this for you already)

    Without argument, open a Python console in-game. This is a full console,
    accepting multi-line Python code for testing and debugging. Type `exit()` to
    return to the game. If Evennia is reloaded, the console will be closed.

    Enter a line of instruction after the 'py' command to execute it
    immediately.  Separate multiple commands by ';' or open the code editor
    using the /edit switch (all lines added in editor will be executed
    immediately when closing or using the execute command in the editor).

    A few variables are made available for convenience in order to offer access
    to the system (you can import more at execution time).

    Available variables in py environment:
      self, me                   : caller
      here                       : caller.location
      evennia                    : the evennia API
      inherits_from(obj, parent) : check object inheritance

    You can explore The evennia API from inside the game by calling
    the `__doc__` property on entities:
        py evennia.__doc__
        py evennia.managers.__doc__

    |rNote: In the wrong hands this command is a severe security risk.  It
    should only be accessible by trusted server admins/superusers.|n
    """

    key = "py"
    aliases = ["!"]
    help_category = "System"


class CmdReload(system.CmdReload):
    """
    Syntax: reload [reason]

    This restarts the server. The Portal is not
    affected. Non-persistent scripts will survive a reload (use
    reset to purge) and at_reload() hooks will be called.
    """

    key = "reload"
    aliases = ["restart"]
    help_category = "System"


class CmdReset(system.CmdReset):
    """
    Syntax: reset

    Notes:
      For normal updating you are recommended to use reload rather
      than this command. Use shutdown for a complete stop of
      everything.

    This emulates a cold reboot of the Server component of Evennia.
    The difference to shutdown is that the Server will auto-reboot
    and that it does not affect the Portal, so no users will be
    disconnected. Contrary to reload however, all shutdown hooks will
    be called and any non-database saved scripts, ndb-attributes,
    cmdsets etc will be wiped.
    """

    key = "reset"
    aliases = ["reboot"]
    help_category = "System"


class CmdScripts(building.CmdScripts):
    """
    Syntax: script[/switches] [script-#dbref, key, script.path]
            script[/start||stop] <obj> = [<script.path or script-key>]

    Switches:
        start - start/unpause an existing script's timer.
        stop - stops an existing script's timer
        pause - pause a script's timer
        delete - deletes script. This will also stop the timer as needed

    Examples:
        script                            - list all scripts
        script foo.bar.Script             - create a new global Script
        script/pause foo.bar.Script       - pause global script
        script scriptname|#dbref          - examine named existing global script
        script/delete #dbref[-#dbref]     - delete script or range by #dbref

        script myobj =                    - list all scripts on object
        script myobj = foo.bar.Script     - create and assign script to object
        script/stop myobj = name|#dbref   - stop named script on object
        script/delete myobj = name|#dbref - delete script on object
        script/delete myobj =             - delete ALL scripts on object

    When given with an `<obj>` as left-hand-side, this creates and
    assigns a new script to that object. Without an `<obj>`, this
    manages and inspects global scripts.

    If no switches are given, this command just views all active
    scripts. The argument can be either an object, at which point it
    will be searched for all scripts defined on it, or a script name
    or #dbref. For using the /stop switch, a unique script #dbref is
    required since whole classes of scripts often have the same name.

    Use the `script` build-level command for managing scripts attached to
    objects.
    """

    key = "scripts"
    aliases = ["script"]
    locks = "cmd:perm(Developer)"
    help_category = "System"


class CmdService(system.CmdService):
    """
    Syntax: service[/switch] <service>

    Switches:
      list   - shows all available services (default)
      start  - activates or reactivate a service
      stop   - stops/inactivate a service (can often be restarted)
      delete - tries to permanently remove a service

    Service management system. Allows for the listing,
    starting, and stopping of services. If no switches
    are given, services will be listed. Note that to operate on the
    service you have to supply the full (green or red) name as given
    in the list.
    """

    key = "service"
    aliases = ["services"]
    help_category = "System"


class CmdShutdown(system.CmdShutdown):
    """
    Syntax: shutdown [announcement]

    Gracefully shut down both Server and Portal.
    """

    key = "shutdown"
    help_category = "System"


class CmdTasks(system.CmdTasks):
    """
    Syntax: tasks[/switch] [task_id or function_name]

    Switches:
        pause   - Pause the callback of a task.
        unpause - Process all callbacks made since pause() was called.
        do_task - Execute the task (call its callback).
        call    - Call the callback of this task.
        remove  - Remove a task without executing it.
        cancel  - Stop a task from automatically executing.

    Notes:
        A task is a single use method of delaying the call of a function. Calls are created
        in code, using `evennia.utils.delay`.
        See |luhttps://www.evennia.com/docs/latest/Command-Duration.html|ltthe docs|le for help.

        By default, tasks that are canceled and never called are cleaned up after one minute.

    Examples:
        - `tasks/cancel move_callback` - Cancels all movement delays from the slow_exit contrib.
            In this example slow exits creates it's tasks with
            `utils.delay(move_delay, move_callback)`
        - `tasks/cancel 2` - Cancel task id 2.

    """

    key = "tasks"
    aliases = ["delays", "task"]
    help_category = "System"
