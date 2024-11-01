from commands.command import Command


class CmdWhisper(Command):
    """
    Syntax: whisper <character> <message>
            whisper <character>,[[character],...] <message>

    Speak privately to one or more characters in your current location without
    others in the room being informed.
    """

    key = "whisper"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()
        if not args:
            caller.msg("Whisper what?")
            return

        args = args.split(" ", 1)
        if len(args) == 1:
            return caller.msg("What do you want to whisper?")

        receivers, whisper = args[0].split(","), args[1] or None
        receivers = [caller.search(target) for target in receivers] or []
        if not receivers:
            return caller.msg("Who do you want to whisper to?")
        if not whisper:
            return caller.msg("What do you want to whisper to them?")

        whisper = caller.at_pre_say(whisper, whisper=True, receivers=receivers)

        if not whisper:
            return

        caller.at_say(
            whisper,
            msg_self=True,
            receivers=receivers or None,
            msg_type="whisper",
        )
