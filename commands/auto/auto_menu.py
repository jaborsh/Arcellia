from math import ceil

from django.conf import settings
from evennia.utils.evmenu import EvMenu
from evennia.utils.evtable import EvColumn, EvTable
from evennia.utils.utils import m_len
from parsing.colors import strip_ansi

from commands.auto import assistants

_MAX_TEXT_WIDTH = settings.CLIENT_DEFAULT_WIDTH


def node_start(caller, raw_input, **kwargs):
    text = "Which assistant would you like to begin a conversation with?\n\n |w[D]|nesigner\n |w[Q]|nuit"
    options = (
        {
            "key": ("[D]esigner", "designer", "d"),
            # "desc": "",
            "goto": "designer_start",
        },
        {
            "key": ("[Q]uit", "quit", "q"),
            "goto": "node_quit",
        },
    )
    return text, options


def designer_start(caller, raw_input, **kwargs):
    Designer = assistants.Designer()
    text = "At any time, you can use these commands:\n |w[N]|new - Begin a new conversation.\n |w[Q]|nuit - Quit the conversation.\n\n|MDesigner|n: Wordsmith Wonderscribe at your service. How may I help?"
    options = (
        {
            "key": "_default",
            "goto": ("node_designer", {"Designer": Designer}),
        },
        {
            "key": ("[N]ew", "new", "n"),
            "goto": "designer_start",
        },
        {
            "key": ("[Q]uit", "quit", "q"),
            "goto": "node_quit",
        },
    )
    return text, options


def node_designer(caller, raw_input, **kwargs):
    Designer = kwargs.get("Designer")
    text = "|MDesigner|n:\n" + Designer.ask(raw_input)
    options = (
        {
            "key": "_default",
            "goto": ("node_designer", {"Designer": Designer}),
        },
        {
            "key": ("[N]ew", "new", "n"),
            "goto": "designer_start",
        },
        {
            "key": ("[Q]uit", "quit", "q"),
            "goto": "node_quit",
        },
    )
    return text, options


def node_quit(caller, raw_input, **kwargs):
    text = "Goodbye!"
    return text, None  # None means quit


class AutoMenu(EvMenu):
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

        nlist = len(optionlist)

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
                    table.append(f" {key}{desc_string}")
                else:
                    # add a default white color to key
                    table.append(f" |w{key}|n{desc_string}")
        ncols = _MAX_TEXT_WIDTH // table_width_max  # number of columns

        if ncols < 0:
            # no visible options at all
            return ""

        ncols = 1 if ncols == 0 else ncols

        # minimum number of rows in a column
        min_rows = 4

        # split the items into columns
        split = max(min_rows, ceil(len(table) / ncols))
        max_end = len(table)
        cols_list = []
        for icol in range(ncols):
            start = icol * split
            end = min(start + split, max_end)
            cols_list.append(EvColumn(*table[start:end]))

        return str(EvTable(table=cols_list, border="none"))

    def node_formatter(self, nodetext, optionstext):
        """
        Formats the entirety of the node.

        Args:
            nodetext (str): The node text as returned by `self.nodetext_formatter`.
            optionstext (str): The options display as returned by `self.options_formatter`.
            caller (Object, Account or None, optional): The caller of the node.

        Returns:
            node (str): The formatted node to display.

        """
        # sep = self.node_border_char

        # if self._session:
        #     screen_width = self._session.protocol_flags.get("SCREENWIDTH", {0: _MAX_TEXT_WIDTH})[0]
        # else:
        #     screen_width = _MAX_TEXT_WIDTH

        # nodetext_width_max = max(m_len(line) for line in nodetext.split("\n"))
        # options_width_max = max(m_len(line) for line in optionstext.split("\n"))
        # total_width = min(screen_width, max(options_width_max, nodetext_width_max))
        # separator1 = sep * total_width + "\n\n" if nodetext_width_max else ""
        # separator2 = "\n" + sep * total_width + "\n\n" if total_width else ""
        # return separator1 + "|n" + nodetext + "|n" + separator2 + "|n" + optionstext
        return nodetext + "\n"  # + "\n\n" + optionstext
