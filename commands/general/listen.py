from commands.command import Command


class CmdListen(Command):
    """
    Syntax: listen

    Listen to your surroundings.
    """

    key = "listen"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            caller.location.msg_contents(
                "$You() $conj(listen) to the surroundings.",
                from_obj=caller,
                exclude=caller,
            )
            return caller.msg(caller.location.sound)

        obj = caller.search(args)
        if not obj:
            return

        caller.location.msg_contents(
            "$You() $conj(listen) to %s." % obj.display_name,
            from_obj=caller,
            exclude=caller,
        )

        caller.msg(obj.sound)
