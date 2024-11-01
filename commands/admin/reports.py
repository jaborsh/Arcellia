from evennia.comms.models import Msg
from evennia.utils import evtable

from commands.command import Command


class CmdReports(Command):
    """
    The `reports` command allows administrators to manage various types of reports, such as bugs and ideas.
    This command can display the latest reports or delete a specific report based on its ID.

    Usage:
        reports
            - Displays the latest 10 reports in a table format.

        reports delete <report_id>
            - Deletes the report with the specified ID.

    Examples:
        reports
            - This will display the latest 10 reports.

        reports delete 5
            - This will delete the report with ID 5.

    Notes:
        - The command will notify if no reports are found or if an invalid report ID is provided.
    """

    key = "reports"
    aliases = ["bugs", "ideas"]
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        report_type = self.cmdstring[:-1]
        reports = Msg.objects.get_by_tag(report_type)

        if not reports:
            return self.msg(f"No {self.cmdstring} found.")

        if not self.args:
            self.display_reports(reports)
        else:
            args = self.args.split(" ")
            if args[0] == "delete":
                self.delete_report(args)

    def display_reports(self, reports):
        table = evtable.EvTable(
            "|wID|n",
            "|wAuthor|n",
            "|wDate|n",
            "",
            border="header",
            maxwidth=self.client_width(),
        )
        table.reformat_column(0, valign="t", width=6)
        table.reformat_column(1, valign="t", width=8)
        table.reformat_column(2, valign="t", width=14)

        for report in reports.reverse()[:10]:
            table.add_row(
                report.id,
                report.senders[0].get_display_name(self.caller),
                report.db_date_created.strftime("%b %d, %Y"),
                report.message,
            )

        self.caller.msg(f"|w{self.cmdstring.capitalize()}|n:\n\n{str(table)}")

    def delete_report(self, args):
        if len(args) < 2:
            return self.msg(f"Please specify a {self.cmdstring[:-1]} ID.")
        elif not args[1].isdigit():
            return self.msg(f"Invalid {self.cmdstring[:-1]} ID.")

        report = Msg.objects.filter(id=args[1]).first()
        if report:
            report.delete()
            self.msg(f"{self.cmdstring[:-1]} deleted.")
        else:
            self.msg(f"{self.cmdstring[:-1]} not found.")
