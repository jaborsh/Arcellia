from math import ceil

from django.conf import settings
from utils.colors import strip_ansi

from evennia.utils.evtable import EvColumn, EvTable
from evennia.utils.utils import dedent, m_len

from .amenu import AMenu

_MAX_TEXT_WIDTH = settings.CLIENT_DEFAULT_WIDTH


class InteractionMenu(AMenu):
    def nodetext_formatter(self, nodetext):
        """
        Format the node text itself.

        Args:
            nodetext (str): The full node text (the text describing the node).

        Returns:
            nodetext (str): The formatted node text.

        """

        text = nodetext.strip("\n")
        if not text == "":
            text += "\n\n|CSelect an Option:|n"

        return dedent(text.strip("\n"), baseline_index=0).rstrip()

    def options_formatter(self, optionlist):
        """
        Formats the option block.

        Args:
            optionlist (list): List of (key, description) tuples for every
                option related to this node.

        Returns:
            options (str): The formatted option display.

        """
        if not optionlist:
            return ""

        # column separation distance
        colsep = 4

        # get the widest option line in the table.
        table_width_max = -1
        table = []
        for key, desc in optionlist:
            if key or desc:
                desc_string = f": {desc}" if desc else ""
                table_width_max = max(
                    table_width_max,
                    max(m_len(p) for p in key.split("\n"))
                    + max(m_len(p) for p in desc_string.split("\n"))
                    + colsep,
                )
                raw_key = strip_ansi(key)
                if raw_key != key:
                    # already decorations in key definition
                    table.append(f" |lc{raw_key}|lt{key}|le{desc_string}")
                else:
                    # add a default white color to key
                    table.append(f" |lc{raw_key}|lt|w{key}|n|le{desc_string}")

        # check if the caller is using a screenreader
        screenreader_mode = False
        if sessions := getattr(self.caller, "sessions", None):
            screenreader_mode = any(
                sess.protocol_flags.get("SCREENREADER") for sess in sessions.all()
            )
        # the caller doesn't have a session; check it directly
        elif hasattr(self.caller, "protocol_flags"):
            screenreader_mode = self.caller.protocol_flags.get("SCREENREADER")

        # ncols = 1 if screenreader_mode else _MAX_TEXT_WIDTH // table_width_max

        ncols = _MAX_TEXT_WIDTH // table_width_max
        if ncols < 0:
            return ""

        ncols = 1 if ncols == 0 or screenreader_mode else ncols

        # minimum number of rows in a column
        min_rows = 5

        # split the items into columns
        split = max(min_rows, ceil(len(table) / ncols))
        max_end = len(table)
        cols_list = []
        for icol in range(ncols):
            start = icol * split
            end = min(start + split, max_end)
            cols_list.append(EvColumn(*table[start:end]))

        return "\n" + str(EvTable(table=cols_list, border="none")) + "\n"
