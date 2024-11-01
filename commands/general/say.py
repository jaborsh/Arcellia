from commands.command import Command


class CmdSay(Command):
    """
    Syntax: say <message>
            say to <character> <message>
            say to <character>,[character,...] <message>

    Example: say to jake,john Hi there!

    Talk to those in your current location or directly to specific people
    nearby.
    """

    key = "say"
    aliases = ['"', "'"]
    locks = "cmd:all()"
    arg_regex = None

    def func(self):
        caller = self.caller
        args = self.args.strip()
        receivers = []
        if not args:
            caller.msg("Say what?")
            return

        speech = args
        if args.startswith("to "):
            for obj in args.split(" ", 2)[1].split(","):
                receiver = caller.search(obj)
                if not receiver:
                    continue
                receivers.append(receiver)

            if not receivers:
                return caller.msg("Who do you want to talk to?")
            try:
                speech = args.split(" ", 2)[2]
            except IndexError:
                return caller.msg(
                    "Have you forgotten what you'd like to say to them?"
                )

        speech = caller.at_pre_say(speech)

        if not speech:
            return

        caller.at_say(
            speech,
            msg_self=True,
            receivers=receivers or None,
            width=self.client_width(),
        )
