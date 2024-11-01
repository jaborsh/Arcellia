"""
Command module containing CmdDiary for managing an admin diary.
"""

from evennia.comms.models import Msg
from evennia.utils import create, evtable

from commands.command import Command


class CmdDiary(Command):
    """
    Command to manage the admin diary.

    Usage:
        diary [<entry>]

    This command allows admins to either view the latest diary entries or add a new entry.
    Without arguments, it displays the last 10 entries in the diary, showing author, date, and message.
    With an entry as an argument, it adds the entry to the diary. Only admins can access the diary.
    """

    key = "diary"
    locks = "cmd:pperm(Admin)"
    help_category = "Admin"

    def func(self):
        """Primary function to either add a new diary entry or display the latest entries."""
        if self.args.strip():
            self._add_entry(self.args.strip())
        else:
            self._display_latest_entries()

    def _add_entry(self, entry_text):
        """
        Adds a new entry to the admin diary.

        Args:
            entry_text (str): The diary entry text to be added.

        Returns:
            None
        """
        if create.create_message(
            self.account,
            entry_text,
            locks="read:pperm(Admin)",
            tags=["admin_diary"],
        ):
            self.caller.msg("Diary entry added successfully.")
        else:
            self.caller.msg("Failed to add diary entry.")

    def _display_latest_entries(self):
        """
        Displays the latest 10 entries in the admin diary.

        Returns:
            None
        """
        entries = Msg.objects.get_by_tag("admin_diary").reverse()[:10]
        if not entries:
            self.caller.msg("No diary entries found.")
            return

        diary_table = self._create_diary_table(entries)
        self.caller.msg("|rAdmin Diary|n:\n\n" + str(diary_table))

    def _create_diary_table(self, entries):
        """
        Creates a formatted table of the latest diary entries.

        Args:
            entries (QuerySet): A queryset of Msg objects representing diary entries.

        Returns:
            EvTable: A formatted table of diary entries.
        """
        diary_table = evtable.EvTable(
            "|wAuthor|n",
            "|wDate|n",
            "",
            border="header",
            maxwidth=self.client_width(),
        )
        diary_table.reformat_column(0, valign="t", width=8)
        diary_table.reformat_column(1, valign="t", width=14)

        for entry in entries:
            diary_table.add_row(
                entry.senders[0].get_display_name(self.caller),
                entry.db_date_created.strftime("%b %d, %Y"),
                entry.message,
            )
        return diary_table
