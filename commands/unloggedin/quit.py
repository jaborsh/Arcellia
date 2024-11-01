from commands.command import Command


class CmdUnloggedinQuit(Command):
    """
    quit when in unlogged-in state

    Usage:
      quit

    We maintain a different version of the quit command
    here for unconnected accounts for the sake of simplicity. The logged in
    version is a bit more complicated.
    """

    key = "quit"
    aliases = ["q", "qu"]
    locks = "cmd:all()"

    def func(self):
        session = self.caller
        session.sessionhandler.disconnect(session, "Good bye! Disconnecting.")
