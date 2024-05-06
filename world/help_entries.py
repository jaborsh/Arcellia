"""
File-based help entries. These complements command-based help and help entries
added in the database using the `sethelp` command in-game.

Control where Evennia reads these entries with `settings.FILE_HELP_ENTRY_MODULES`,
which is a list of python-paths to modules to read.

A module like this should hold a global `HELP_ENTRY_DICTS` list, containing
dicts that each represent a help entry. If no `HELP_ENTRY_DICTS` variable is
given, all top-level variables that are dicts in the module are read as help
entries.

Each dict is on the form
::

    {'key': <str>,
     'text': <str>}``     # the actual help text. Can contain # subtopic sections
     'category': <str>,   # optional, otherwise settings.DEFAULT_HELP_CATEGORY
     'aliases': <list>,   # optional
     'locks': <str>       # optional, 'view' controls seeing in help index, 'read'
                          #           if the entry can be read. If 'view' is unset,
                          #           'read' is used for the index. If unset, everyone
                          #           can read/view the entry.

"""

# HELP_ENTRY_DICTS = [
#     {
#         "key": "evennia",
#         "aliases": ["ev"],
#         "category": "General",
#         "locks": "read:perm(Developer)",
#         "text": """
#             Evennia is a MU-game server and framework written in Python. You can read more
#             on https://www.evennia.com.

#             # subtopics

#             ## Installation

#             You'll find installation instructions on https://www.evennia.com.

#             ## Community

#             There are many ways to get help and communicate with other devs!

#             ### Discussions

#             The Discussions forum is found at https://github.com/evennia/evennia/discussions.

#             ### Discord

#             There is also a discord channel for chatting - connect using the
#             following link: https://discord.gg/AJJpcRUhtF

#         """,
#     },
# ]

HELP_ENTRY_DICTS = [
    {
        "key": "attributes",
        "aliases": [
            "str",
            "dex",
            "con",
            "int",
            "wis",
            "cha",
            "strength",
            "dexterity",
            "constitution",
            "intelligence",
            "wisdom",
            "charisma",
        ],
        "text": """
            Attributes represent the physical and mental capabilities of a character or creature. Throughout the game, you will encounter various situations that require your character to perform physical, mental, or charismatic tasks. These challenges are resolved in three ways:
            
                1. Automatically - Some attribute checks are automatic. For example, approaching a trap might require a check to notice it.
                
                2. Interactions - Some attribute checks are made during interactions. For example, convincing a guard to let you pass might require a Charisma check.
                
                3. Combat - Some attribute checks are made during combat. Both you and an opponent might oppose each other with checks to determine who wins a grapple.
            
            The six attributes are:
            
            1. Strength (STR)     - Muscles and physical power.
            
            2. Dexterity (DEX)    - Agility, reflexes, and balance.
            
            3. Constitution (CON) - Stamina and physical endurance.
            
            4. Intelligence (INT) - Memory and mental power.
            
            5. Wisdom (WIS)       - Senses and intuitions.
            
            6. Charisma (CHA)     - Force of personality.
        """,
    }
]
