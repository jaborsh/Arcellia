"""
Command sets

All commands in the game must be grouped in a cmdset.  A given command
can be part of any number of cmdsets and cmdsets can be added/removed
and merged onto entities at runtime.

To create new commands to populate the cmdset, see
`commands/command.py`.

This module wraps the default command sets of Evennia; overloads them
to add/remove commands from the default lineup. You can create your
own cmdsets by inheriting from them or directly from `evennia.CmdSet`.

"""

from evennia import default_cmds

from commands import (
    account,
    admin,
    clothing,
    comms,
    developer,
    general,
    git,
    help,
    system,
    unloggedin,
)
from commands.building import building


def add_modules(self, modules):
    """
    Add all commands from modules passed by argument.
    """
    for module_group in modules.values():
        for module in module_group:
            for cmd_name in module.__all__:
                cmd_class = getattr(module, cmd_name)
                self.add(cmd_class)


class AccountCmdSet(default_cmds.AccountCmdSet):
    """
    This is the cmdset available to the Account at all times. It is
    combined with the `CharacterCmdSet` when the Account puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """

    key = "DefaultAccount"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        modules = {
            "Developer Modules": [developer, git],
            "Admin Modules": [admin],
            "Account Modules": [account],
            "Comm Modules": [comms],
            "Help Modules": [help],
            "System Modules": [system],
        }
        add_modules(self, modules)


class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `AccountCmdSet` when an Account puppets a Character.
    """

    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        modules = {
            "Building Modules": [building],
            "General Modules": [clothing, general],
        }
        add_modules(self, modules)


class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    This cmdset is made available on Session level once logged in. It
    is empty by default.
    """

    key = "DefaultSession"

    def at_cmdset_creation(self):
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.

        As and example we just add the empty base `Command` object.
        It prints some info.
        """
        super().at_cmdset_creation()


class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    Command set available to the Session before being logged in.  This
    holds commands like creating a new account, logging in, etc.
    """

    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        modules = {"Unloggedin Modules": [unloggedin]}
        add_modules(self, modules)
