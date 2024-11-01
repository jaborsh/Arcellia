from commands.command import Command


class CmdTaste(Command):
    """
    Syntax: taste
            taste <obj>

    Taste your surroundings or a specific object.
    """

    key = "taste"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            caller.location.msg_contents(
                "$You() $conj(taste) the air.", from_obj=caller, exclude=caller
            )
            return caller.msg(caller.location.taste)

        obj = caller.search(args)
        if not obj:
            return

        caller.location.msg_contents(
            "$You() $conj(taste) %s." % obj.display_name,
            from_obj=caller,
            exclude=caller,
        )

        caller.msg(obj.taste)
