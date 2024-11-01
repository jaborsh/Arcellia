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
        """
        Handle the report command.

        This method parses the user input, creates a report of the specified type,
        and provides user feedback on the success or failure of the report submission.
        """
        if not self.args:
            return self.msg("You must provide a report.")

        try:
            self.create_report(self.args.strip(), self.cmdstring)
            return self.msg(f"Your {self.cmdstring} has been submitted.")
        except Exception as e:
            self.msg(
                f"Something went wrong with creating your {self.cmdstring}. Please contact staff directly. Error: {e}"
            )

    def create_report(self, message, report_type):
        """
        Create a report of the specified type.

        Args:
            message (str): The content of the report.
            report_type (str): The type of the report.
        """
        create.create_message(
            self.account,
            message,
            locks="read:pperm(Admin)",
            tags=[report_type],
        )
