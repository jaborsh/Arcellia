"""
Command module containing CmdDiary.
"""

from evennia.comms.models import Msg
from evennia.utils import create, evtable

from commands.command import Command


class CmdDiary(Command):
    """
    Command to manage the admin diary.

    Usage:
        diary [<entry>]

    This command allows admins to add entries to the admin diary or view the latest entries.

    If no argument is provided, it displays the last 10 diary entries. Each entry includes the author, date, and message.

    If an entry is provided as an argument, it adds the entry to the diary. Only admins can read or add entries to the diary.
    """

    key = "diary"
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        if not self.args:
            return self.display_diary()

        if create.create_message(
            self.account,
            self.args.strip(),
            locks="read:pperm(Admin)",
            tags=["admin_diary"],
        ):
            self.caller.msg("Diary entry added.")
        else:
            self.caller.msg("Failed to add diary entry.")

    def display_diary(self):
        entries = Msg.objects.get_by_tag("admin_diary").reverse()[:10]
        if not entries:
            return self.caller.msg("No diary entries found.")

        diary = evtable.EvTable(
            "|wAuthor|n",
            "|wDate|n",
            "",
            border="header",
            maxwidth=self.client_width(),
        )
        diary.reformat_column(0, valign="t", width=8)
        diary.reformat_column(1, valign="t", width=14)

        for entry in entries:
            diary.add_row(
                entry.senders[0].get_display_name(self.caller),
                entry.db_date_created.strftime("%b %d, %Y"),
                entry.message,
            )
        self.caller.msg("|rAdmin Diary|n:\n\n" + str(diary))
