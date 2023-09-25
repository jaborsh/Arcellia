from evennia.commands.default import help as default_help
from evennia.utils.ansi import ANSIString
from evennia.utils.utils import dedent, pad
from parsing.colors import strip_ansi
from parsing.text import format_grid

__all__ = ("CmdHelp", "CmdSetHelp")


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
                        entries = [f"|lchelp {entry}|lt{entry}|le" for entry in entries]

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
                            f"|lchelp {entry}|lt|w{entry}|le" for entry in entries
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
            help_index = f"{sep1}\n{cmd_grid}\n{sep2}\n{db_grid}"
        else:
            print(cmd_grid)
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
            "|#FFD700" + "-" * (self.client_width() - len(strip_ansi(title))) + "|n"
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
                suggested = [f"|lchelp {sug}|lt|w{sug}|n|le" for sug in suggested]
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


class CmdSetHelp(default_help.CmdSetHelp):
    """
    Syntax: sethelp[/switches] <topic>[[;alias;alias][,category[,locks]] [= <text>]

    Switches:
      edit - open a line editor to edit the topic's help text.
      replace - overwrite existing help topic.
      append - add text to the end of existing topic with a newline between.
      extend - as append, but don't add a newline.
      delete - remove help topic.

    Examples:
      sethelp lore = In the beginning was ...
      sethelp/append pickpocketing,Thievery = This steals ...
      sethelp/replace pickpocketing, ,attr(is_thief) = This steals ...
      sethelp/edit thievery

    If not assigning a category, the `settings.DEFAULT_HELP_CATEGORY` category
    will be used. If no lockstring is specified, everyone will be able to read
    the help entry.  Sub-topics are embedded in the help text.

    Note that this cannot modify command-help entries - these are modified
    in-code, outside the game.

    # SUBTOPICS

    ## Adding subtopics

    Subtopics helps to break up a long help entry into sub-sections. Users can
    access subtopics with |whelp topic/subtopic/...|n Subtopics are created and
    stored together with the main topic.

    To start adding subtopics, add the text '# SUBTOPICS' on a new line at the
    end of your help text. After this you can now add any number of subtopics,
    each starting with '## <subtopic-name>' on a line, followed by the
    help-text of that subtopic.
    Use '### <subsub-name>' to add a sub-subtopic and so on. Max depth is 5. A
    subtopic's title is case-insensitive and can consist of multiple words -
    the user will be able to enter a partial match to access it.

    For example:

    | Main help text for <topic>
    |
    | # SUBTOPICS
    |
    | ## about
    |
    | Text for the '<topic>/about' subtopic'
    |
    | ### more about-info
    |
    | Text for the '<topic>/about/more about-info sub-subtopic
    |
    | ## extra
    |
    | Text for the '<topic>/extra' subtopic

    """

    key = "sethelp"
    locks = "cmd:perm(Admin)"
    help_category = "Admin"


"""
The help command. The basic idea is that help texts for commands
are best written by those that write the commands - the admins. So
command-help is all auto-loaded and searched from the current command
set. The normal, database-tied help system is used for collaborative
creation of other help topics such as RP help or game-world aides.
"""

# from collections import defaultdict

# from django.conf import settings
# from evennia.help.models import HelpEntry
# from evennia.utils import create, evmore, evtable
# from evennia.utils.eveditor import EvEditor
# from evennia.utils.utils import class_from_module, dedent, string_suggestions

# COMMAND_DEFAULT_CLASS = class_from_module(settings.COMMAND_DEFAULT_CLASS)
# HELP_MORE = settings.HELP_MORE_ENABLED
# CMD_IGNORE_PREFIXES = settings.CMD_IGNORE_PREFIXES

# # limit symbol import for API
# __all__ = ("CmdHelpOverride", "CmdSetHelp")
# _DEFAULT_WIDTH = settings.CLIENT_DEFAULT_WIDTH
# _SEP = "|302" + "-" * _DEFAULT_WIDTH + "|n"


# class CmdHelpOverride(COMMAND_DEFAULT_CLASS):
#     """
#     View help or a list of topics

#     Usage:
#       help <topic or command>
#       help list
#       help all

#     This will search for help on commands and other
#     topics related to the game.
#     """

#     key = "help"
#     aliases = ["?"]
#     locks = "cmd:all()"
#     arg_regex = r"\s|$"

#     # this is a special cmdhandler flag that makes the cmdhandler also pack
#     # the current cmdset with the call to self.func().
#     return_cmdset = True

#     # Help messages are wrapped in an EvMore call (unless using the webclient
#     # with separate help popups) If you want to avoid this, simply add
#     # 'HELP_MORE = False' in your settings/conf/settings.py
#     help_more = HELP_MORE

#     # suggestion cutoff, between 0 and 1 (1 => perfect match)
#     suggestion_cutoff = 0.6

#     # number of suggestions (set to 0 to remove suggestions from help)
#     suggestion_maxnum = 5

#     def msg_help(self, text):
#         """
#         messages text to the caller, adding an extra oob argument to indicate
#         that this is a help command result and could be rendered in a separate
#         help window
#         """
#         if type(self).help_more:
#             usemore = True

#             if self.session and self.session.protocol_key in (
#                 "websocket",
#                 "ajax/comet",
#             ):
#                 try:
#                     options = self.account.db._saved_webclient_options
#                     if options and options["helppopup"]:
#                         usemore = False
#                 except KeyError:
#                     pass

#             if usemore:
#                 evmore.msg(self.caller, text, session=self.session)
#                 return

#         self.msg(text=(text, {"type": "help"}))

#     @staticmethod
#     def format_help_entry(title, help_text, aliases=None, suggested=None):
#         """
#         This visually formats the help entry.
#         This method can be overriden to customize the way a help
#         entry is displayed.

#         Args:
#             title (str): the title of the help entry.
#             help_text (str): the text of the help entry.
#             aliases (list of str or None): the list of aliases.
#             suggested (list of str or None): suggested reading.

#         Returns the formatted string, ready to be sent.

#         """
#         string = ""
#         if title:
#             length = _DEFAULT_WIDTH - len(str(title)) - 7
#             string += f"\r|302---[ |w{(str(title).upper())}|302 ]{'-' * length}|n"
#         if help_text:
#             string += f"\n{dedent(help_text.rstrip())}"
#         if aliases:
#             string += "\n\n|cSynonyms:|c|n "
#             ali_string = []
#             for ali in aliases:
#                 click_link = f"{ali}"
#                 ali_string.append(click_link)
#             string += " " + "|n,|n ".join("|w%s|n" % ali for ali in ali_string)
#         if suggested:
#             length = _DEFAULT_WIDTH - len(str("suggested")) - 7
#             string += f"\n\n\r|302---[ |wSUGGESTED|302 ]{'-' * length}|n\n\n"
#             sug_string = []
#             for sug in suggested:
#                 click_link = f"|lchelp {sug}|lt|w{sug}|n|le"
#                 sug_string.append(click_link)
#             string += " " + "|n,|n ".join("|w%s|n" % ali for ali in sug_string)
#         string.strip()
#         string += "\n\n" + _SEP
#         return string

#     @staticmethod
#     def format_help_list(hdict_cmds, hdict_db, cat):
#         # we've added an extra arg here to catch the "category/query"
#         """
#         Output a category-ordered list. The input are the
#         pre-loaded help files for commands and database-helpfiles
#         respectively.  You can override this method to return a
#         custom display of the list of commands and topics.
#         """
#         string = ""
#         count = 0
#         column_str = []
#         if hdict_cmds and any(hdict_cmds.values()):
#             if not cat:
#                 string += (
#                     _SEP
#                     + "\n   |wHELP ENTRIES|n\n   Use HELP <topic> to see more information.\n"
#                     + _SEP
#                     + "\n\n"
#                 )
#             for category in sorted(hdict_cmds.keys()):
#                 count += 1
#                 if cat == category:
#                     string += f"{_SEP}\n   |wHELP ENTRY: {str(category).upper()}|n\n   Use HELP <sub-topic> to see more information.\n{_SEP}\n"
#                     _DEFAULT_WIDTH - len(str(category)) - 7
#                     topic_list = []
#                     for topic in hdict_cmds[category]:
#                         click_str = str(topic).title()
#                         click_link = (
#                             f"|302   ~ |lchelp {click_str}|lt|w{click_str}|n|le"
#                         )
#                         topic_list.append(click_link)
#                     # there's probably a better way to do this
#                     topic_table = evtable.EvTable(border=None, width=60)
#                     divide = len(topic_list) / 2
#                     col_count = 0
#                     topcol1 = []
#                     topcol2 = []
#                     for top in topic_list:
#                         if col_count < divide:
#                             topcol1.append(top)
#                         else:
#                             topcol2.append(top)
#                         col_count += 1
#                     if len(topcol2) < len(topcol1):
#                         topcol2.append(" ")
#                     topic_table.add_column("\n".join(topcol1))
#                     topic_table.add_column("\n".join(topcol2))
#                     string += f"\n|n{topic_table}"
#                 else:
#                     _DEFAULT_WIDTH - len(str(category)) - 7
#                     click_str = f"{(str(category).title())}"
#                     click_link = f"|lchelp {click_str}|lt|w{click_str}|n|le"
#                     column_str.append(f"|302   ~ |w{click_link}|302 |n ")
#         if hdict_db and any(hdict_db.values()):
#             for category in sorted(hdict_db.keys()):
#                 count += 1
#                 if cat:
#                     string += (
#                         f"{_SEP}\n   |wHELP ENTRY: {str(category).upper()}|n\n{_SEP}\n"
#                     )
#                     _DEFAULT_WIDTH - len(str(category)) - 7
#                     topic_list = []
#                     for topic in hdict_cmds[category]:
#                         click_str = str(topic).title()
#                         click_link = (
#                             f"|302   ~ |lchelp {click_str}|lt|w{click_str}|n|le"
#                         )
#                         topic_list.append(click_link)
#                     # there's probably a better way to do this
#                     topic_table = evtable.EvTable(border=None, width=60)
#                     divide = len(topic_list) / 2
#                     col_count = 0
#                     topcol1 = []
#                     topcol2 = []
#                     for top in topic_list:
#                         if col_count < divide:
#                             topcol1.append(top)
#                         else:
#                             topcol2.append(top)
#                         col_count += 1
#                     if len(topcol2) < len(topcol1):
#                         topcol2.append(" ")
#                     topic_table.add_column("\n".join(topcol1))
#                     topic_table.add_column("\n".join(topcol2))
#                     string += f"\n|n{topic_table}"
#                 else:
#                     _DEFAULT_WIDTH - len(str(category)) - 7
#                     click_str = f"{(str(category).title())}"
#                     click_link = f"|lchelp {click_str}|lt|w{click_str}|n|le"
#                     column_str.append(f"|302   ~ |w{click_link}|302 |n ")
#         # there's probably a better way to do this table too
#         table = evtable.EvTable(border=None, width=60)
#         divide = count / 2
#         col_count = 0
#         col1 = []
#         col2 = []
#         for info in column_str:
#             if col_count < divide:
#                 col1.append(info)
#             else:
#                 col2.append(info)
#             col_count += 1
#         table.add_column("\n".join(col1))
#         table.add_column("\n".join(col2))
#         string += f"{table}\n\n" + _SEP
#         return string

#     def check_show_help(self, cmd, caller):
#         """
#         Helper method. If this return True, the given cmd
#         auto-help will be viewable in the help listing.
#         Override this to easily select what is shown to
#         the account. Note that only commands available
#         in the caller's merged cmdset are available.

#         Args:
#             cmd (Command): Command class from the merged cmdset
#             caller (Character, Account or Session): The current caller
#                 executing the help command.

#         """
#         # return only those with auto_help set and passing the cmd: lock
#         return cmd.auto_help and cmd.access(caller)

#     def should_list_cmd(self, cmd, caller):
#         """
#         Should the specified command appear in the help table?

#         This method only checks whether a specified command should
#         appear in the table of topics/commands.  The command can be
#         used by the caller (see the 'check_show_help' method) and
#         the command will still be available, for instance, if a
#         character type 'help name of the command'.  However, if
#         you return False, the specified command will not appear in
#         the table.  This is sometimes useful to "hide" commands in
#         the table, but still access them through the help system.

#         Args:
#             cmd: the command to be tested.
#             caller: the caller of the help system.

#         Return:
#             True: the command should appear in the table.
#             False: the command shouldn't appear in the table.

#         """
#         return cmd.access(caller, "view", default=True)

#     def parse(self):
#         """
#         input is a string containing the command or topic to match.
#         """
#         self.original_args = self.args.strip()
#         self.args = self.args.strip().lower()

#     def func(self):
#         """
#         Run the dynamic help entry creator.
#         """
#         query, cmdset = self.args, self.cmdset
#         caller = self.caller

#         suggestion_cutoff = self.suggestion_cutoff
#         suggestion_maxnum = self.suggestion_maxnum

#         if not query:
#             query = "all"

#         # removing doublets in cmdset, caused by cmdhandler
#         # having to allow doublet commands to manage exits etc.
#         cmdset.make_unique(caller)

#         # retrieve all available commands and database topics
#         all_cmds = [cmd for cmd in cmdset if self.check_show_help(cmd, caller)]
#         all_topics = [
#             topic
#             for topic in HelpEntry.objects.all()
#             if topic.access(caller, "view", default=True)
#         ]
#         all_categories = list(
#             set(
#                 [cmd.help_category.lower() for cmd in all_cmds]
#                 + [topic.help_category.lower() for topic in all_topics]
#             )
#         )

#         if query in ("list", "all"):
#             # we want to list all available help entries, grouped by category
#             hdict_cmd = defaultdict(list)
#             hdict_topic = defaultdict(list)
#             # create the dictionaries {category:[topic, topic ...]} required by format_help_list
#             # Filter commands that should be reached by the help
#             # system, but not be displayed in the table, or be displayed differently.
#             for cmd in all_cmds:
#                 if self.should_list_cmd(cmd, caller):
#                     key = (
#                         cmd.auto_help_display_key
#                         if hasattr(cmd, "auto_help_display_key")
#                         else cmd.key
#                     )
#                     hdict_cmd[cmd.help_category].append(key)
#             [hdict_topic[topic.help_category].append(topic.key) for topic in all_topics]
#             # report back
#             self.msg_help(self.format_help_list(hdict_cmd, hdict_topic, self.args))
#             return

#         # Try to access a particular command

#         # build vocabulary of suggestions and rate them by string similarity.
#         suggestions = None
#         if suggestion_maxnum > 0:
#             vocabulary = (
#                 [cmd.key for cmd in all_cmds if cmd]
#                 + [topic.key for topic in all_topics]
#                 + all_categories
#             )
#             [vocabulary.extend(cmd.aliases) for cmd in all_cmds]
#             suggestions = [
#                 sugg
#                 for sugg in string_suggestions(
#                     query,
#                     set(vocabulary),
#                     cutoff=suggestion_cutoff,
#                     maxnum=suggestion_maxnum,
#                 )
#                 if sugg != query
#             ]
#             if not suggestions:
#                 suggestions = [
#                     sugg
#                     for sugg in vocabulary
#                     if sugg != query and sugg.startswith(query)
#                 ]

#         # try an exact command auto-help match
#         match = [cmd for cmd in all_cmds if cmd == query]

#         if not match:
#             # try an inexact match with prefixes stripped from query and cmds
#             _query = query[1:] if query[0] in CMD_IGNORE_PREFIXES else query

#             match = [
#                 cmd
#                 for cmd in all_cmds
#                 for m in cmd._matchset
#                 if m == _query or m[0] in CMD_IGNORE_PREFIXES and m[1:] == _query
#             ]

#         if len(match) == 1:
#             cmd = match[0]
#             key = (
#                 cmd.auto_help_display_key
#                 if hasattr(cmd, "auto_help_display_key")
#                 else cmd.key
#             )
#             formatted = self.format_help_entry(
#                 key,
#                 cmd.get_help(caller, cmdset),
#                 aliases=cmd.aliases,
#                 suggested=suggestions,
#             )
#             self.msg_help(formatted)
#             return

#         # try an exact database help entry match
#         match = list(HelpEntry.objects.find_topicmatch(query, exact=True))
#         if len(match) == 1:
#             formatted = self.format_help_entry(
#                 match[0].key,
#                 match[0].entrytext,
#                 aliases=match[0].aliases.all(),
#                 suggested=suggestions,
#             )
#             self.msg_help(formatted)
#             return

#         # try to see if a category name was entered
#         if query in all_categories:
#             self.msg_help(
#                 self.format_help_list(
#                     {
#                         query: [
#                             cmd.auto_help_display_key
#                             if hasattr(cmd, "auto_help_display_key")
#                             else cmd.key
#                             for cmd in all_cmds
#                             if cmd.help_category == query
#                         ]
#                     },
#                     {
#                         query: [
#                             topic.key
#                             for topic in all_topics
#                             if topic.help_category == query
#                         ]
#                     },
#                     cat=query,
#                 )
#             )
#             return

#         # no exact matches found. Just give suggestions.
#         self.msg(
#             self.format_help_entry(
#                 "", f"No help entry found for '{query}'", None, suggested=suggestions
#             ),
#             options={"type": "help"},
#         )


# def _loadhelp(caller):
#     entry = caller.db._editing_help
#     if entry:
#         return entry.entrytext
#     else:
#         return ""


# def _savehelp(caller, buffer):
#     entry = caller.db._editing_help
#     caller.msg("Saved help entry.")
#     if entry:
#         entry.entrytext = buffer


# def _quithelp(caller):
#     caller.msg("Closing the editor.")
#     del caller.db._editing_help


# class CmdSetHelp(COMMAND_DEFAULT_CLASS):
#     """
#     Edit the help database.

#     Usage:
#       help[/switches] <topic>[[;alias;alias][,category[,locks]] [= <text>]

#     Switches:
#       edit - open a line editor to edit the topic's help text.
#       replace - overwrite existing help topic.
#       append - add text to the end of existing topic with a newline between.
#       extend - as append, but don't add a newline.
#       delete - remove help topic.

#     Examples:
#       sethelp throw = This throws something at ...
#       sethelp/append pickpocketing,Thievery = This steals ...
#       sethelp/replace pickpocketing, ,attr(is_thief) = This steals ...
#       sethelp/edit thievery

#     This command manipulates the help database. A help entry can be created,
#     appended/merged to and deleted. If you don't assign a category, the
#     "General" category will be used. If no lockstring is specified, default
#     is to let everyone read the help file.

#     """

#     key = "sethelp"
#     switch_options = ("edit", "replace", "append", "extend", "delete")
#     locks = "cmd:perm(Helper)"
#     help_category = "Building"

#     def func(self):
#         """Implement the function"""

#         switches = self.switches
#         lhslist = self.lhslist

#         if not self.args:
#             self.msg(
#                 "Syntax: sethelp[/switches] <topic>[;alias;alias][,category[,locks,..] = <text>"
#             )
#             return

#         nlist = len(lhslist)
#         topicstr = lhslist[0] if nlist > 0 else ""
#         if not topicstr:
#             self.msg("You have to define a topic!")
#             return
#         topicstrlist = topicstr.split(";")
#         topicstr, aliases = (
#             topicstrlist[0],
#             topicstrlist[1:] if len(topicstr) > 1 else [],
#         )
#         aliastxt = ("(aliases: %s)" % ", ".join(aliases)) if aliases else ""
#         old_entry = None

#         # check if we have an old entry with the same name
#         try:
#             for querystr in topicstrlist:
#                 old_entry = HelpEntry.objects.find_topicmatch(
#                     querystr
#                 )  # also search by alias
#                 if old_entry:
#                     old_entry = list(old_entry)[0]
#                     break
#             category = lhslist[1] if nlist > 1 else old_entry.help_category
#             lockstring = ",".join(lhslist[2:]) if nlist > 2 else old_entry.locks.get()
#         except Exception:
#             old_entry = None
#             category = lhslist[1] if nlist > 1 else "General"
#             lockstring = ",".join(lhslist[2:]) if nlist > 2 else "view:all()"
#         category = category.lower()

#         if "edit" in switches:
#             # open the line editor to edit the helptext. No = is needed.
#             if old_entry:
#                 topicstr = old_entry.key
#                 if self.rhs:
#                     # we assume append here.
#                     old_entry.entrytext += "\n%s" % self.rhs
#                 helpentry = old_entry
#             else:
#                 helpentry = create.create_help_entry(
#                     topicstr,
#                     self.rhs,
#                     category=category,
#                     locks=lockstring,
#                     aliases=aliases,
#                 )
#             self.caller.db._editing_help = helpentry

#             EvEditor(
#                 self.caller,
#                 loadfunc=_loadhelp,
#                 savefunc=_savehelp,
#                 quitfunc=_quithelp,
#                 key="topic {}".format(topicstr),
#                 persistent=True,
#             )
#             return

#         if "append" in switches or "merge" in switches or "extend" in switches:
#             # merge/append operations
#             if not old_entry:
#                 self.msg(
#                     "Could not find topic '%s'. You must give an exact name." % topicstr
#                 )
#                 return
#             if not self.rhs:
#                 self.msg("You must supply text to append/merge.")
#                 return
#             if "merge" in switches:
#                 old_entry.entrytext += " " + self.rhs
#             else:
#                 old_entry.entrytext += "\n%s" % self.rhs
#             old_entry.aliases.add(aliases)
#             self.msg("Entry updated:\n%s%s" % (old_entry.entrytext, aliastxt))
#             return
#         if "delete" in switches or "del" in switches:
#             # delete the help entry
#             if not old_entry:
#                 self.msg("Could not find topic '%s'%s." % (topicstr, aliastxt))
#                 return
#             old_entry.delete()
#             self.msg("Deleted help entry '%s'%s." % (topicstr, aliastxt))
#             return

#         # at this point it means we want to add a new help entry.
#         if not self.rhs:
#             self.msg("You must supply a help text to add.")
#             return
#         if old_entry:
#             if "replace" in switches:
#                 # overwrite old entry
#                 old_entry.key = topicstr
#                 old_entry.entrytext = self.rhs
#                 old_entry.help_category = category
#                 old_entry.locks.clear()
#                 old_entry.locks.add(lockstring)
#                 old_entry.aliases.add(aliases)
#                 old_entry.save()
#                 self.msg("Overwrote the old topic '%s'%s." % (topicstr, aliastxt))
#             else:
#                 self.msg(
#                     "Topic '%s'%s already exists. Use /replace to overwrite "
#                     "or /append or /merge to add text to it." % (topicstr, aliastxt)
#                 )
#         else:
#             # no old entry. Create a new one.
#             new_entry = create.create_help_entry(
#                 topicstr, self.rhs, category=category, locks=lockstring, aliases=aliases
#             )
#             if new_entry:
#                 self.msg(
#                     "Topic '%s'%s was successfully created." % (topicstr, aliastxt)
#                 )
#                 if "edit" in switches:
#                     # open the line editor to edit the helptext
#                     self.caller.db._editing_help = new_entry
#                     EvEditor(
#                         self.caller,
#                         loadfunc=_loadhelp,
#                         savefunc=_savehelp,
#                         quitfunc=_quithelp,
#                         key="topic {}".format(new_entry.key),
#                         persistent=True,
#                     )
#                     return
#             else:
#                 self.msg(
#                     "Error when creating topic '%s'%s! Contact an admin."
#                     % (topicstr, aliastxt)
#                 )
