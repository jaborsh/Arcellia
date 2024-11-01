from evennia.commands.default import system


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
