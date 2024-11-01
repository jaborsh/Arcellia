from evennia.utils import (
    evtable,
)

from commands.command import Command
from utils.colors import strip_ansi
from utils.text import wrap


class CmdJournal(Command):
    """
    This command allows the player to view their quests and quest details.

    Usage:
      journal - Lists all quests.
      journal <quest_name> - Shows details of the specified quest.
    """

    key = "journal"
    aliases = ["quests", "quest"]

    def func(self):
        caller = self.caller
        args = self.args.strip().capitalize()

        if not args:
            self.list_quests()
            return

        if quest := caller.quests.get(args):
            self.list_quest_details(quest)
        else:
            return caller.msg("You do not have that quest.")

    def list_quests(self):
        """
        Display a list of quests and their progress for the caller.

        Args:
            self (Command): The command instance.

        Returns:
            None

        """
        caller = self.caller
        quests = self.caller.quests.all()

        if not quests:
            return caller.msg("You do not have any quests.")

        table = evtable.EvTable("Quests", "Progress", border="rows")
        for quest in quests:
            table.add_row(
                quest.key,
                quest.get_status().name,
            )

        caller.msg(table)

    def list_quest_details(self, quest):
        """
        Display the details of a quest.

        Args:
            quest (Quest): The quest object to display details for.

        Returns:
            None
        """
        caller = self.caller
        information = quest.get_information()

        table = evtable.EvTable(border=None, width=self.client_width())

        for key, value in information.items():  # Maybe use reversed()?
            name_status = (
                "|w" + value.get("name") + "|n - " + value.get("status").name
            )
            table.add_row(name_status)
            table.add_row("-" * len(strip_ansi(name_status)))
            table.add_row(value.get("description"))
            table.add_row()
            # table.add_column(value.get("status").name)

        caller.msg(
            wrap(
                f"{quest.key.capitalize()} Quest Information",
                text_width=self.client_width(),
                align="c",
            )
            + "\n"
        )
        caller.msg(table)
