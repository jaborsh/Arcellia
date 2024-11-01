from evennia.commands.default import help as default_help
from evennia.utils.ansi import ANSIString
from evennia.utils.utils import dedent, pad

from utils.colors import strip_ansi
from utils.text import format_grid


class CmdHelp(default_help.CmdHelp):
    """
    Syntax: help
            help <topic, command, or category>
            help <topic>/<subtopic>
            help <topic>/<subtopic>/<subsubtopic> ...

    Use the 'help' command alone to see an index of all help files, organized
    by category. Some big topics may offer additional sub-topics.
    """

    help_category = "General"
    aliases = ["?"]
    color = "|#FFD700"

    def format_help_index(
        self,
        cmd_help_dict=None,
        db_help_dict=None,
        title_lone_category=True,
        click_topics=True,
    ):
        """Output a category-ordered g for displaying the main help, grouped by
        category.

        Args:
            cmd_help_dict (dict): A dict `{"category": [topic, topic, ...]}` for
                command-based help.
            db_help_dict (dict): A dict `{"category": [topic, topic], ...]}` for
                database-based help.
            title_lone_category (bool, optional): If a lone category should
                be titled with the category name or not. While pointless in a
                general index, the title should probably show when explicitly
                listing the category itself.
            click_topics (bool, optional): If help-topics are clickable or not
                (for webclient or telnet clients with MXP support).
        Returns:
            str: The help index organized into a grid.

        Notes:
            The input are the pre-loaded help files for commands and database-helpfiles
            respectively. You can override this method to return a custom display of
            the list of commands and topics.

        """

        def _group_by_category(help_dict):
            color = self.color
            grid = []
            verbatim_elements = []

            if len(help_dict) == 1 and not title_lone_category:
                # don't list categories if there is only one
                for category in help_dict:
                    # gather and sort the entries from the help dictionary
                    entries = sorted(set(help_dict.get(category, [])))

                    # make the help topics clickable
                    if click_topics:
                        entries = [
                            f"|lchelp {entry}|lt{entry}|le" for entry in entries
                        ]

                    # add the entries to the grid
                    grid.extend(entries)
            else:
                # list the categories
                for category in sorted(set(list(help_dict.keys()))):
                    category_str = f"{color}--|w[ {category.title()} ]{color}--"
                    grid.append(
                        ANSIString(
                            self.index_category_clr
                            + category_str
                            + "-" * (width - len(strip_ansi(category_str)))
                            + self.index_topic_clr
                        )
                    )
                    verbatim_elements.append(len(grid) - 1)

                    # gather and sort the entries from the help dictionary
                    entries = sorted(set(help_dict.get(category, [])))

                    # make the help topics clickable
                    if click_topics:
                        entries = [
                            f"|lchelp {entry}|lt|w{entry}|le"
                            for entry in entries
                        ]

                    # add the entries to the grid
                    grid.extend(entries)

            return grid, verbatim_elements

        help_index = ""
        width = self.client_width()
        grid = []
        verbatim_elements = []
        cmd_grid, db_grid = "", ""

        if any(cmd_help_dict.values()):
            # get the command-help entries by-category
            sep1 = (
                self.index_type_separator_clr
                + pad("Commands", width=width, fillchar="-")
                + self.index_topic_clr
            )
            grid, verbatim_elements = _group_by_category(cmd_help_dict)
            gridrows = format_grid(
                grid,
                width,
                sep="     ",
                verbatim_elements=verbatim_elements,
                line_prefix=self.index_topic_clr,
            )
            cmd_grid = ANSIString("\n").join(gridrows) if gridrows else ""

        if any(db_help_dict.values()):
            # get db-based help entries by-category
            sep2 = (
                self.index_type_separator_clr
                + pad("Game & World", width=width, fillchar="-")
                + self.index_topic_clr
            )
            grid, verbatim_elements = _group_by_category(db_help_dict)
            gridrows = format_grid(
                grid,
                width,
                sep="  ",
                verbatim_elements=verbatim_elements,
                line_prefix=self.index_topic_clr,
            )
            db_grid = ANSIString("\n").join(gridrows) if gridrows else ""

        footer = f"{self.color}" + "-" * width + "|n"

        # only show the main separators if there are actually both cmd and db-based help
        if cmd_grid and db_grid:
            help_index = f"{sep1}{cmd_grid}\n\n{sep2}{db_grid}"
        else:
            help_index = f"{cmd_grid}{db_grid}\n{footer}"

        return help_index

    def format_help_entry(
        self,
        topic="",
        help_text="",
        aliases=None,
        suggested=None,
        subtopics=None,
        click_topics=True,
    ):
        """This visually formats the help entry.
        This method can be overridden to customize the way a help
        entry is displayed.

        Args:
            title (str, optional): The title of the help entry.
            help_text (str, optional): Text of the help entry.
            aliases (list, optional): List of help-aliases (displayed in header).
            suggested (list, optional): Strings suggested reading (based on title).
            subtopics (list, optional): A list of strings - the subcategories available
                for this entry.
            click_topics (bool, optional): Should help topics be clickable. Default is True.

        Returns:
            help_message (str): Help entry formated for console.

        """
        title = (
            f"|#FFD700--|w[ {topic.upper()} ]|n"
            if topic
            else "|#FFD700--|w[ |rNo Help Found! |w]|n"
        )
        head_border = (
            "|#FFD700"
            + "-" * (self.client_width() - len(strip_ansi(title)))
            + "|n"
        )
        start = f"{title}{head_border}"
        help_text = dedent(help_text.strip("\n")) if help_text else ""

        if subtopics:
            if click_topics:
                subtopics = [
                    f"|lchelp {topic}/{subtop}|lt|w{topic}/{subtop}|n|le"
                    for subtop in subtopics
                ]
            else:
                subtopics = [f"|w{topic}/{subtop}|n" for subtop in subtopics]

            subtopics_header = (
                "|#FFD700--|w[ SUBTOPICS ]|n"
                + "|#FFD700"
                + "-" * (self.client_width() - 15)
            )
            subtopics = "\n{}\n\n  {}".format(
                subtopics_header,
                "\n  ".join(
                    format_grid(
                        subtopics,
                        width=self.client_width(),
                        line_prefix=self.index_topic_clr,
                    )
                ),
            )
        else:
            subtopics = ""

        if suggested:
            suggested = sorted(suggested)
            if click_topics:
                suggested = [
                    f"|lchelp {sug}|lt|w{sug}|n|le" for sug in suggested
                ]
            else:
                suggested = [f"|w{sug}|n" for sug in suggested]

            suggested_header = (
                "|#FFD700--|w[ SUGGESTED ]|n"
                + "|#FFD700"
                + "-" * (self.client_width() - 15)
            )
            suggested = "{}\n\n  {}".format(
                suggested_header,
                "\n  ".join(
                    format_grid(
                        suggested,
                        width=self.client_width(),
                        sep=", ",
                        line_prefix=self.index_topic_clr,
                    )
                ),
            )
        else:
            suggested = ""

        if aliases:
            aliases.sort()
            aliases = "|#FFD700--|w[ Aliases: {}|w ]|n".format(
                ", ".join(f"|w{ali}|n" for ali in aliases)
            )
        else:
            aliases = "|#FFD700"

        end = (
            aliases
            + "|#FFD700"
            + "-" * (self.client_width() - len(strip_ansi(aliases)))
            + "|n"
        )

        partorder = (start, help_text, subtopics, suggested, end)

        return "\n\n".join(part.rstrip() for part in partorder if part)
