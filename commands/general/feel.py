from commands.command import Command


class CmdFeel(Command):
    """
    Syntax: feel
            feel <obj>

    Feel your surroundings or a specific object.
    """

    key = "feel"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            caller.location.msg_contents(
                "$You() $conj(feel) the air.", from_obj=caller, exclude=caller
            )
            return caller.msg(caller.location.feel)

        obj = caller.search(args)
        if not obj:
            return

        caller.location.msg_contents(
            "$You() $conj(feel) %s." % obj.display_name,
            from_obj=caller,
            exclude=caller,
        )

        caller.msg(obj.feel)
