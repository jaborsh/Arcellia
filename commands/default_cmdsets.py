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

from evennia import CmdSet, default_cmds

from commands.spells.destruction import novice as d_novice

from . import (
    account,
    admin,
    building,
    developer,
    general,
    gestures,
    git,
    help,
    system,
    unloggedin,
)


def add_modules(self, modules):
    """
    Adds command classes from the given modules to the command set.

    Args:
        modules (dict): A dictionary containing module groups, where each group is a list of modules.

    Returns:
        None
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
            "Admin Modules": [admin, developer, git, system],
            "Account Modules": [account, help],
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
        # super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        modules = {
            "Builder Modules": [building],
            "Character Modules": [general, gestures],
            "Spell Modules": [d_novice],
        }

        add_modules(self, modules)


class MobCmdSet(CmdSet):
    """
    The `MobCmdSet` contains default commands for mobs. These will closely
    mirror the basic commands available to characters.
    """

    key = "DefaultMob"

    def at_cmdset_creation(self):
        modules = {
            "General Modules": [general, gestures],
            # "Merchant Modules": [clothing],
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
        # super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #


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
        # super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        modules = {
            "Unloggedin Modules": [unloggedin],
        }

        add_modules(self, modules)
