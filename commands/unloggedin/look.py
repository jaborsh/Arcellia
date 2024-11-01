from django.conf import settings
from evennia import syscmdkeys
from evennia.utils import utils

from commands.command import Command
from world.login import login_menu

_CONNECTION_SCREEN_MODULE = settings.CONNECTION_SCREEN_MODULE


class CmdUnloggedinLook(Command):
    """
    An unloggedin version of the look command. This is called by the server
    when the session first connects. It sets up the menu before handing off
    the menu's own look command.
    """

    key = syscmdkeys.CMD_LOGINSTART
    aliases = ["look", "l"]
    locks = "cmd:all()"
    arg_regex = r"^$"

    def func(self):
        """
        Run the menu using the nodes in this module.
        """

        # Get the connection screen
        callables = utils.callables_from_module(_CONNECTION_SCREEN_MODULE)
        if "connection_screen" in callables:
            connection_screen = callables["connection_screen"]()
        else:
            connection_screen = utils.random_string_from_module(
                _CONNECTION_SCREEN_MODULE
            )
            if not connection_screen:
                connection_screen = (
                    "No connection screen found. Please contact an admin."
                )
        self.caller.msg(connection_screen)

        # Set up the menu
        menu_nodes = {
            "node_enter_username": login_menu.node_enter_username,
            "node_enter_password": login_menu.node_enter_password,
            "node_quit_or_login": login_menu.node_quit_or_login,
        }

        # Start the menu
        login_menu.MenuLoginEvMenu(
            self.caller,
            menu_nodes,
            startnode="node_enter_username",
            auto_look=False,
            auto_quit=False,
            cmd_on_exit=None,
        )
