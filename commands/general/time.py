from evennia import InterruptCommand
from evennia.commands.default import system


class CmdTime(system.CmdTime):
    """
    Syntax: time

    Shows the current in-game time and season.
    """

    key = "time"
    locks = "cmd:all()"
    help_category = "General"

    def parse(self):
        location = self.caller.location
        if (
            not location
            or not hasattr(location, "get_time_of_day")
            or not hasattr(location, "get_season")
        ):
            self.caller.msg("No location available - you are outside time.")
            raise InterruptCommand()
        self.location = location

    def func(self):
        location = self.location

        season = location.get_season()
        timeslot = location.get_time_of_day()

        prep = "an" if season == "autumn" else "a"
        self.caller.msg(f"It's {prep} {season} day, in the {timeslot}.")
