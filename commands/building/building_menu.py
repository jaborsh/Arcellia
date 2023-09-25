from django.conf import settings
from evennia.contrib.base_systems.building_menu import building_menu
from parsing.colors import strip_ansi
from server.conf import logger

GOLD = "|#FFD700"

width = settings.CLIENT_DEFAULT_WIDTH


class BuildingMenuCmdSet(building_menu.BuildingMenuCmdSet):
    """
    Building Menu CmdSet.
    """

    key = "building_menu"
    priority = 5
    mergetype = "Replace"
    no_exits = True


def menu_quit(menu, caller):
    """
    Quit the menu, closing the CmdSet.

    Args:
        caller (Account or Object): the caller.

    Note:
        This callback is used by default when using the
        `BuildingMenu.add_choice_quit` method.  This method is called
        automatically if the menu has no parent.
    """
    try:
        menu.close()
        caller.msg("Closing the building menu...")
        desc = caller.at_look(caller.location)
        caller.msg(text=(desc, {"type": "look"}), options=None)
    except Exception:
        caller.msg("An error has occurred. Contact an administrator.")


class BuildingMenu(building_menu.BuildingMenu):
    """
    Class allowing to create and set building menus to edit specific objects.

    A building menu is somewhat similar to `EvMenu`, but designed to edit
    objects by builders, although it can be used for players in some contexts.
    You could, for instance, create a building menu to edit a room with a
    sub-menu for the room's key, another for the room's description,
    another for the room's exits, and so on.

    To add choices (simple sub-menus), you should call `add_choice` (see the
    full documentation of this method).  With most arguments, you can
    specify either a plain string or a callback.  This callback will be
    called when the operation is to be performed.

    Some methods are provided for frequent needs (see the `add_choice_*`
    methods).  Some helper functions are defined at the top of this
    module in order to be used as arguments to `add_choice`
    in frequent cases.
    """

    def __init__(
        self,
        caller=None,
        obj=None,
        title="Building menu: {obj}",
        keys=None,
        parents=None,
        persistent=False,
        **kwargs,
    ):
        """Constructor, you shouldn't override.  See `init` instead.

        Args:
            caller (Account or Object): the caller.
            obj (Object): the object to be edited, like a room.
            title (str, optional): the menu title.
            keys (list of str, optional): the starting menu keys (None
                    to start from the first level).
            parents (tuple, optional): information for parent menus,
                    automatically supplied.
            persistent (bool, optional): should this building menu
                    survive a reload/restart?

        Note:
            If some of these options have to be changed, it is
            preferable to do so in the `init` method and not to
            override `__init__`.  For instance:
                class RoomBuildingMenu(BuildingMenu):
                    def init(self, room):
                        self.title = "Menu for room: {obj.key}(#{obj.id})"
                        # ...

        """
        self.caller = caller
        self.obj = obj
        self.title = title
        self.keys = keys or []
        self.parents = parents or ()
        self.persistent = persistent
        self.choices = []
        self.cmds = {}
        self.can_quit = False
        self.kwargs = kwargs
        self.footer = (
            f"{GOLD}"
            + "-" * self.kwargs.get("width", settings.CLIENT_DEFAULT_WIDTH)
            + "|n"
        )

        if obj:
            self.init(obj)
            if not parents and not self.can_quit:
                # Automatically add the menu to quit
                self.add_choice_quit(key=None)
            self._add_keys_choice()

    def add_choice(
        self,
        title,
        key=None,
        aliases=None,
        attr=None,
        text=None,
        glance=None,
        on_enter=None,
        on_nomatch=None,
        on_leave=None,
    ):
        """
        Add a choice, a valid sub-menu, in the current builder menu.

        Args:
            title (str): the choice's title.
            key (str, optional): the key of the letters to type to access
                    the sub-neu.  If not set, try to guess it based on the
                    choice title.
            aliases (list of str, optional): the aliases for this choice.
            attr (str, optional): the name of the attribute of 'obj' to set.
                    This is really useful if you want to edit an
                    attribute of the object (that's a frequent need).  If
                    you don't want to do so, just use the `on_*` arguments.
            text (str or callable, optional): a text to be displayed when
                    the menu is opened  It can be a callable.
            glance (str or callable, optional): an at-a-glance summary of the
                    sub-menu shown in the main menu.  It can be set to
                    display the current value of the attribute in the
                    main menu itself.
            on_enter (callable, optional): a callable to call when the
                    caller enters into this choice.
            on_nomatch (callable, optional): a callable to call when
                    the caller enters something in this choice.  If you
                    don't set this argument but you have specified
                    `attr`, then `obj`.`attr` will be set with the value
                    entered by the user.
            on_leave (callable, optional): a callable to call when the
                    caller leaves the choice.

        Returns:
            choice (Choice): the newly-created choice.

        Raises:
            ValueError if the choice cannot be added.

        Note:
            Most arguments can be callables, like functions.  This has the
            advantage of allowing great flexibility.  If you specify
            a callable in most of the arguments, the callable should return
            the value expected by the argument (a str more often than
            not).  For instance, you could set a function to be called
            to get the menu text, which allows for some filtering:
                def text_exits(menu):
                    return "Some text to display"
                class RoomBuildingMenu(BuildingMenu):
                    def init(self):
                        self.add_choice("exits", key="x", text=text_exits)

            The allowed arguments in a callable are specific to the
            argument names (they are not sensitive to orders, not all
            arguments have to be present).  For more information, see
            `_call_or_get`.

        """
        key = key or ""
        key = key.lower()
        aliases = aliases or []
        aliases = [a.lower() for a in aliases]
        if attr and on_nomatch is None:
            on_nomatch = building_menu.menu_setattr

        if key and key in self.cmds:
            raise ValueError(
                "A conflict exists between {} and {}, both use key or alias {}".format(
                    self.cmds[key], title, repr(key)
                )
            )

        if attr:
            if glance is None:
                glance = "{obj." + attr + "}"
            if text is None:
                global width
                width = self.kwargs.get("width", settings.CLIENT_DEFAULT_WIDTH)
                header_title = (
                    f"|w[{self.obj.key} {title.capitalize()} Editor]{GOLD}--|n"
                )
                header = (
                    f"{GOLD}"
                    + "-" * (width - len(strip_ansi(header_title)))
                    + header_title
                )
                text = """
                        {header}

                        {attr_cap} for {{obj}}(#{{obj.id}}): {{{obj_attr}}}

                        {footer}
                        Enter a new {attr} or use |y{back}|n to return:""".format(
                    header=header,
                    attr_cap=attr.capitalize(),
                    attr=attr,
                    obj_attr="obj." + attr,
                    footer=self.footer,
                    back="|n or |y".join(self.keys_go_back),
                )

        choice = building_menu.Choice(
            title,
            key=key,
            aliases=aliases,
            attr=attr,
            text=text,
            glance=glance,
            on_enter=on_enter,
            on_nomatch=on_nomatch,
            on_leave=on_leave,
            menu=self,
            caller=self.caller,
            obj=self.obj,
        )
        self.choices.append(choice)
        if key:
            self.cmds[key] = choice

        for alias in aliases:
            self.cmds[alias] = choice

        return choice

    def add_choice_quit(self, title="quit", key="q", aliases=None, on_enter=None):
        """
        Add a simple choice just to quit the building menu.

        Args:
            title (str, optional): the choice's title.
            key (str, optional): the choice's key.
            aliases (list of str, optional): the choice's aliases.
            on_enter (callable, optional): a different callable
                    to quit the building menu.

        Note:
            This is just a shortcut method, calling `add_choice`.
            If `on_enter` is not set, use `menu_quit` which simply
            closes the menu and displays a message.  It also
            removes the CmdSet from the caller.  If you supply
            another callable instead, make sure to do the same.

        """
        on_enter = on_enter or menu_quit
        self.can_quit = True
        return self.add_choice(title, key=key, aliases=aliases, on_enter=on_enter)

    def display(self):
        """Display the entire menu or a single choice, depending on the keys."""
        choice = self.current_choice
        if self.keys and choice:
            if choice.key == "q":
                return
            text = choice.format_text()
        else:
            text = self.display_title()
            for choice in self.relevant_choices:
                text += "\n\n" + self.display_choice(choice)
            text += "\n\n" + self.footer + "\nSelect Edit Option: "

        self.caller.msg(text)

    def open_submenu(self, submenu_class, submenu_obj, parent_keys=None):
        """
        Open a sub-menu, closing the current menu and opening the new one.

        Args:
            submenu_class (str): the submenu class as a Python path.
            submenu_obj (Object): the object to give to the submenu.
            parent_keys (list of str, optional): the parent keys when
                    the submenu is closed.

        Note:
            When the user enters `@` in the submenu, she will go back to
            the current menu, with the `parent_keys` set as its keys.
            Therefore, you should set it on the keys of the choice that
            should be opened when the user leaves the submenu.

        Returns:
            new_menu (BuildingMenu): the new building menu or None.

        """
        parent_keys = parent_keys or []
        parents = list(self.parents)
        parents.append(
            (type(self).__module__ + "." + type(self).__name__, self.obj, parent_keys)
        )
        if self.caller.cmdset.has(BuildingMenuCmdSet):
            self.caller.cmdset.remove(BuildingMenuCmdSet)

        # Create the submenu
        try:
            building_menu = submenu_class(self.caller, submenu_obj, parents=parents)
        except Exception:
            logger.log_trace(
                "An error occurred while creating building menu {}".format(
                    repr(submenu_class)
                )
            )
            return
        else:
            return building_menu.open()


class RoomBuildingMenu(BuildingMenu):
    def init(self, room):
        self.add_choice("Key", "k", attr="key")
        self.add_choice_edit("description", key="d", attr="db.desc")
        self.add_choice(
            "exits", "e", glance=glance_exits, text=text_exits, on_nomatch=nomatch_exits
        )


# Menu functions
def glance_exits(room):
    """Show the room exits."""
    if room.exits:
        glance = ""
        for exit in room.exits:
            glance += f"\n  |y{exit.key}|n"

        return glance

    return "\n  |gNo exit yet|n"


def text_exits(caller, room):
    """Show the room exits in the choice itself."""
    header = f"|w[Room Exit Editor]{GOLD}--|n"
    header = f"{GOLD}" + "-" * (width - len(strip_ansi(header))) + header
    text = header
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
        border = f"{GOLD}" + "-" * width + "|n"
        text += "\n\n" + border + "\n"
        text += "Select Edit Option [|y@|n to return]:"
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
    title = f"|w[{exit.key.capitalize()} Exit Editor]{GOLD}--|n"
    border = f"{GOLD}" + "-" * (width - len(strip_ansi(title))) + title
    caller.msg(f"{border}")
    menu.open_submenu(ExitBuildingMenu, exit, parent_keys=["e"])
    return False


class ExitBuildingMenu(BuildingMenu):
    """
    Building menu to edit an exit.
    """

    def init(self, exit):
        self.add_choice("key", key="k", attr="key", glance="{obj.key}")
        self.add_choice_edit("description", "d")

    def display(self):
        """Display the entire menu or a single choice, depending on the keys."""
        choice = self.current_choice
        if self.keys and choice:
            if choice.key == "q":
                return
            text = choice.format_text()
        else:
            text = "\n\n".join(
                self.display_choice(choice) for choice in self.relevant_choices
            )
            text = f"\n{text}\n\n{self.footer}\nSelect Edit Option [|y@|n to return]: "

        self.caller.msg(text)
