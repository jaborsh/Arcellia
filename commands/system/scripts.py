from evennia.commands.default import building


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
