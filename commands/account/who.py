"""
Command module containing CmdWho.
"""

import time
from datetime import datetime

from django.conf import settings
from evennia.accounts.models import AccountDB
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import utils

from commands.command import Command


class CmdWho(Command):
    """
    Command to display a list of currently logged-in players and their details.

    Usage: who

    This command provides a formatted list of all players currently connected to the MUD,
    including their display names, locations, connection times, idle times, and host addresses.
    The display format varies slightly depending on whether the caller has administrative
    permissions.
    """

    key = "who"
    aliases = ["wh"]
    locks = "cmd:all()"
    help_category = "Account"

    def func(self):
        caller = self.caller
        session_list = [
            sess for sess in SESSIONS.get_sessions() if sess.get_puppet()
        ]
        width = 49 + 5 * ((self.client_width() - 49) // 5)

        if self.account.permissions.check("Admin"):
            admin, table = self.get_admin_and_table(session_list, caller, width)
        else:
            admin, table = self.get_admin_and_player_table(
                session_list, caller, width
            )

        naccounts = SESSIONS.account_count() - len(admin)

        header = self.create_header(width)
        footer = self.get_footer(width)
        player_count = f"{naccounts} player{'s' if naccounts != 1 else ''} logged in.".rjust(
            width
        )

        caller.msg(f"{header}\n{table}\n{footer}\n{player_count}")

    def create_header(self, width):
        header_string = (
            f"{self.get_header(width)}\n"
            f"{self.get_time_display(width)}\n"
            f"{self.get_admin_display(width)}\n"
            f"{self.format_admin(self.get_admin_names(), width)}\n"
            f"{self.get_player_display(width)}"
        )
        return header_string

    def get_header(self, width):
        return f" |145[ {settings.SERVERNAME} ]|n ".center(width + 6, "-")

    def get_time_display(self, width):
        current_time = datetime.now().strftime("%H:%M:%S %p, %A, %B %d, %Y")
        return current_time.center(width)

    def get_admin_display(self, width):
        return " |r[ Administrators ]|n ".center(width + 4, "-")

    def get_admin_names(self):
        return sorted(
            acc.name
            for acc in AccountDB.objects.all()
            if acc.permissions.get("Admin") or acc.permissions.get("Developer")
        )

    def format_admin(self, names, width):
        total_names_length = sum(len(name) for name in names)
        num_gaps = len(names) + 1
        remaining_space = width - total_names_length

        if remaining_space <= 0:
            return " ".join(names)[:width]

        gap, extra_space = divmod(remaining_space, num_gaps)
        formatted_string = " " * gap

        for name in names:
            formatted_string += name + " " * (
                gap + (1 if extra_space > 0 else 0)
            )
            extra_space -= 1

        return formatted_string

    def get_player_display(self, width):
        return " [ Players ] ".center(width, "-")

    def get_footer(self, width):
        return "-" * width

    def add_row_to_table(self, table, session, caller):
        delta_cmd = time.time() - session.cmd_last_visible
        delta_conn = time.time() - session.conn_time
        session_account = session.get_account()
        puppet = session.get_puppet()
        location = puppet.location.key if puppet and puppet.location else "None"

        table.add_row(
            utils.crop(session_account.get_display_name(caller), width=25),
            utils.crop(location, width=25),
            utils.time_format(delta_conn, 0),
            utils.time_format(delta_cmd, 1),
            (
                session.address[0]
                if isinstance(session.address, tuple)
                else session.address
            ),
        )

    def get_admin_and_table(self, session_list, caller, width):
        admin = []
        table = self.styled_table(
            "|wPlayer",
            "|wRoom",
            "|wOn for",
            "|wIdle",
            "|wHost",
            header=True,
            border="header",
            pad_left=2,
            width=width,
            evenwidth=False,
        )

        session_list = sorted(session_list, key=lambda x: x.get_puppet().name)
        for session in session_list:
            account = session.get_account()
            if account.permissions.check("Admin"):
                admin.append(account.get_display_name(caller))
            elif session.logged_in:
                self.add_row_to_table(table, session, caller)

        return admin, table

    def get_admin_and_player_table(self, session_list, caller, width):
        admin = []
        table = self.styled_table(
            header=True,
            border="header",
            pad_left=2,
            width=width,
            evenwidth=False,
        )

        session_list = sorted(session_list, key=lambda x: x.get_puppet().name)
        for session in session_list:
            account = session.get_account()
            if account.permissions.check("Admin"):
                admin.append(account.get_display_name(caller))
            elif session.logged_in:
                table.add_row(
                    utils.crop(
                        session.get_puppet().get_display_name(caller), width=25
                    )
                )

        return admin, table
