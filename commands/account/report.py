"""
Command module containing CmdReport.
"""

from evennia.utils import create

from commands.command import Command


class CmdReport(Command):
    """
    Submit reports, bugs, or ideas to the staff.

    Usage:
        report <message> - Submit a general report.
        bug <message> - Report a bug.
        idea <message> - Submit an idea.
    """

    key = "report"
    aliases = ["bug", "idea"]
    locks = "cmd:all()"

    def func(self):
        if not self.args:
            return self.msg("You must provide a report.")

        if create.create_message(
            self.account,
            self.args.strip(),
            locks="read:pperm(Admin)",
            tags=[self.cmdstring],
        ):
            return self.msg("Your report has been submitted.")

        self.msg(
            "Something went wrong with creating your report. Please contact staff directly."
        )
