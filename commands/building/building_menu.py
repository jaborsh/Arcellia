"""
Module containing the building menu system.

Evennia contributor: vincent-lg 2018
Modifications by: Jake 2023

Building menus are in-game menus, not unlike `EvMenu` though using a
different approach.  Building menus have been specifically designed to edit
information as a builder.  Creating a building menu in a command allows
builders quick-editing of a given object, like a room.  If you follow the
steps below to add the contrib, you will have access to an `@edit` command
that will edit any default object offering to change its key and description.

1. Import the `GenericBuildingCmd` class from this contrib in your
   `mygame/commands/default_cmdset.py` file:

    ```python
    from evennia.contrib.base_systems.building_menu import GenericBuildingCmd

    ```

2. Below, add the command in the `CharacterCmdSet`:

    ```python
    # ... These lines should exist in the file
    class CharacterCmdSet(default_cmds.CharacterCmdSet):
        key = "DefaultCharacter"

        def at_cmdset_creation(self):
            super().at_cmdset_creation()
            # ... add the line below
            self.add(GenericBuildingCmd())
    ```

The `@edit` command will allow you to edit any object.  You will need to
specify the object name or ID as an argument.  For instance: `@edit here`
will edit the current room.  However, building menus can perform much more
than this very simple example, read on for more details.

Building menus can be set to edit about anything.  Here is an example of
output you could obtain when editing the room:

```
 Editing the room: Limbo(#2)

 [T]itle: the limbo room
 [D]escription
    This is the limbo room.  You can easily change this default description,
    either by using the |y@desc/edit|n command, or simply by entering this
    menu (enter |yd|n).
 [E]xits:
     north to A parking(#4)
 [Q]uit this menu
```

From there, you can open the title choice by pressing t.  You can then
change the room title by simply entering text, and go back to the
main menu entering @ (all this is customizable).  Press q to quit this menu.

The first thing to do is to create a new module and place a class
inheriting from `BuildingMenu` in it.

```python
from evennia.contrib.base_systems.building_menu.building_menu import BuildingMenu

class RoomBuildingMenu(BuildingMenu):
    # ...

```

Next, override the `init` method.  You can add choices (like the title,
description, and exits choices as seen above) by using the `add_choice`
method.

```
class RoomBuildingMenu(BuildingMenu):
    def init(self, room):
        self.add_choice("title", "t", attr="key")
```

That will create the first choice, the title choice.  If one opens your menu
and enter t, she will be in the title choice.  She can change the title
(it will write in the room's `key` attribute) and then go back to the
main menu using `@`.

`add_choice` has a lot of arguments and offers a great deal of
flexibility.  The most useful ones is probably the usage of callbacks,
as you can set almost any argument in `add_choice` to be a callback, a
function that you have defined above in your module.  This function will be
called when the menu element is triggered.

Notice that in order to edit a description, the best method to call isn't
`add_choice`, but `add_choice_edit`.  This is a convenient shortcut
which is available to quickly open an `EvEditor` when entering this choice
and going back to the menu when the editor closes.

```
class RoomBuildingMenu(BuildingMenu):
    def init(self, room):
        self.add_choice("title", "t", attr="key")
        self.add_choice_edit("description", key="d", attr="db.desc")
```

When you wish to create a building menu, you just need to import your
class, create it specifying your intended caller and object to edit,
then call `open`:

```python
from <wherever> import RoomBuildingMenu

class CmdEdit(Command):

    key = "redit"

    def func(self):
        menu = RoomBuildingMenu(self.caller, self.caller.location)
        menu.open()
```

This is a very short introduction.  For more details, see the online tutorial
(https://github.com/evennia/evennia/wiki/Building-menus) or read the
heavily-documented code below.

"""

from evennia.contrib.base_systems import building_menu


class GenericBuildingMenu(building_menu.GenericBuildingCmd):
    """
    A generic building menu, allowing to edit any object.

    This is more a demonstration menu.  By default, it allows to edit the
    object key and description.  Nevertheless, it will be useful to demonstrate
    how building menus are meant to be used.
    """


def glance_exits(obj):
    """Show the room exits."""
    if not obj.exits:
        return "\n  |gNo exit yet|n"

    return "\n" + "\n".join(f"  |w{exit.key}|n" for exit in obj.exits)


def text_exits(caller, room):
    """Show the room exits in the choice itself."""
    text = "-" * 79
    text += "\n\nRoom exits:"
    text += "\n Use |y@c|n to create a new exit."
    text += "\n\nExisting exits:"
    if room.exits:
        for exit in room.exits:
            text += f"\n  |y@e {exit.key}|n"
            if exit.aliases.all():
                text += " (|y{aliases}|n)".format(
                    aliases="|n, |y".join(alias for alias in exit.aliases.all())
                )
            if exit.destination:
                text += f" toward {exit.get_display_name(caller)}"
    else:
        text += "\n\n |gNo exit has yet been defined.|n"

    return text


def nomatch_exits(menu, caller, room, string):
    """
    The user typed something in the list of exits.  Maybe an exit name?
    """
    string = string[3:]
    exit = caller.search(string, candidates=room.exits)
    if exit is None:
        return

    # Open a sub-menu, using nested keys
    caller.msg(f"Editing: {exit.key}")
    menu.move(exit)
    return False


# Exit sub-menu
def text_single_exit(menu, caller):
    """Show the text to edit single exits."""
    exit = menu.keys[1]
    if exit is None:
        return ""

    return f"""
        Exit {exit.key}:

        Enter the exit key to change it, or |y@|n to go back.

        New exit key:
    """


def nomatch_single_exit(menu, caller, room, string):
    """The user entered something in the exit sub-menu.  Replace the exit key."""
    # exit is the second key element: keys should contain ['e', <Exit object>]
    exit = menu.keys[1]
    if exit is None:
        caller.msg("|rCannot find the exit.|n")
        menu.move(back=True)
        return False

    exit.key = string
    return True


class RoomBuildingMenu(building_menu.BuildingMenu):

    """A generic building menu, allowing to edit any object.

    This is more a demonstration menu.  By default, it allows to edit the
    object key and description.  Nevertheless, it will be useful to demonstrate
    how building menus are meant to be used.

    """

    def init(self, obj):
        self.add_choice("key", "k", attr="key")
        self.add_choice_edit("description", key="d", attr="db.desc")
        self.add_choice(
            "exits", "e", glance=glance_exits, text=text_exits, on_nomatch=nomatch_exits
        )

        # Exit sub-menu
        self.add_choice(
            "exit", "e.*", text=text_single_exit, on_nomatch=nomatch_single_exit
        )
