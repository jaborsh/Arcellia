from evennia.commands.default import help as default_help


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
