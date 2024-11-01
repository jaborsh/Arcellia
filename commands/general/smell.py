from commands.command import Command


class CmdSmell(Command):
    """
    Syntax: smell
            smell <obj>

    Smell your surroundings or a specific object.
    """

    key = "smell"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            caller.location.msg_contents(
                "$You() $conj(smell) the air.", from_obj=caller, exclude=caller
            )
            return caller.msg(caller.location.smell)

        obj = caller.search(args)
        if not obj:
            return

        caller.location.msg_contents(
            "$You() $conj(smell) %s." % obj.display_name,
            from_obj=caller,
            exclude=caller,
        )

        caller.msg(obj.smell)
