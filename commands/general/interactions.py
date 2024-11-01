from commands.command import Command


class CmdInteractions(Command):
    """
    Syntax: interactions

    View all the available interactions in your current location.
    """

    key = "interactions"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller

        interactions = [
            item.get_display_name(caller)
            for item in caller.location.contents
            if item.db.interaction
        ]

        if not interactions:
            return caller.msg("There are no interactions here.")

        string = "Interactions:\n - "
        string += "\n - ".join(interactions)
        caller.msg(string)
