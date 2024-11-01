"""
Edit command module.
"""

from commands.command import Command
from menus import building_menu
from utils.colors import strip_ansi

GOLD = "|#FFD700"


class CmdEdit(Command):
    """
    Syntax: edit <object>

    Open a building menu to edit the specified object.  This menu allows to
    change the object's key and description.

    Examples:
      edit here
      edit self
      edit #142
    """

    key = "edit"
    aliases = ["redit"]
    locks = "cmd:perm(edit) or perm(Builder)"
    help_category = "Building"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            obj = caller.location
        else:
            obj = self.caller.search(args, global_search=True)

        if not obj:
            return

        if obj.typename == "Room":
            width = self.client_width()
            title = f"|w[Room Editor]{GOLD}--|n"
            title = f"{GOLD}" + "-" * (width - len(strip_ansi(title))) + title
            menu = building_menu.RoomBuildingMenu(
                caller, obj, title=title, width=width
            )
        else:
            obj_name = obj.get_display_name(caller)
            return self.msg(f"|r{obj_name} cannot be edited currently.|n")

        menu.open()
