"""
This changes the login menu to ask for the account name and password in
sequence instead of requiring one to enter both at once.
"""
from django.conf import settings

from evennia.accounts.accounts import DefaultAccount
from evennia.utils.evmenu import EvMenu
from evennia.utils.utils import (
    class_from_module,
)

_ACCOUNT = class_from_module(settings.BASE_ACCOUNT_TYPECLASS)
_CONNECTION_SCREEN_MODULE = settings.CONNECTION_SCREEN_MODULE


def node_enter_username(caller, raw_text, **kwargs):
    """
    Start node of menu.

    Start login by displaying the connection screen and ask for a username.
    """

    def _check_input(caller, username, **kwargs):
        """
        Callback set up to be called from the _default option.

        Called when user enters a username string. Check if this username
        already exists; set the flag 'new_user' if not. Will directly login
        if the username is 'guest' and GUEST_ENABLED is True.

        The return from this callback determines which node we go to next
        and what kwarg it will be called with.
        """
        username = username.rstrip("\n").capitalize()
        try:
            _ACCOUNT.objects.get(username__iexact=username)
        except _ACCOUNT.DoesNotExist:
            valid, errors = DefaultAccount.validate_username(username)
            if not valid:
                caller.msg("|r{}".format("\n".join(errors)))
                return "node_enter_username", {}
            return "node_enter_password", {"new_user": True, "username": username}

        return "node_enter_password", {"new_user": False, "username": username}

    text = "Enter your account name:"

    options = (
        {"key": "", "goto": "node_enter_username"},
        {"key": "_default", "goto": _check_input},
    )

    return text, options


def node_enter_password(caller, raw_string, **kwargs):
    """
    Handle password input.
    """

    def _check_input(caller, password, **kwargs):
        """
        Callback set up to be called from the _default option.

        Called when the user enters a password string. Check username + pass
        viability. If it passes, the account will have been created and login
        will be initiated.

        The return from this callback determines which node we go to next
        and what kwargs will be passed to it.
        """
        username = kwargs["username"]
        new_user = kwargs["new_user"]
        password = password.rstrip("\n")

        session = caller
        address = session.address

        if new_user:
            # create new account
            account, errors = _ACCOUNT.create(
                username=username, password=password, ip=address, session=session
            )
        else:
            # check password against existing account
            account, errors = _ACCOUNT.authenticate(
                username=username, password=password, ip=address, session=session
            )

        if account:
            if new_user:
                session.msg(f"|gAccount created. Welcome to {settings.SERVERNAME}!|n")
            # pass login info to login node
            return "node_quit_or_login", {"login": True, "account": account}
        else:
            # restart due to errors
            session.msg("|R{}".format("\n".join(errors)))
            kwargs["retry_password"] = True
            return "node_enter_password", kwargs

    def _restart_login(caller, *arg, **kwargs):
        caller.msg("|yCancelled login.|n")
        return "node_enter_username"

    username = kwargs["username"]
    if kwargs["new_user"]:
        if kwargs.get("retry_password"):
            # attempting to fix password
            text = "Enter a new password:"
        else:
            text = f"Creating a new account: |w{username}|n.\nEnter a password:"
    else:
        text = "Enter your password:"

    options = (
        {"key": "", "goto": _restart_login},
        {"key": "_default", "goto": (_check_input, kwargs)},
    )

    return text, options


def node_quit_or_login(caller, raw_text, **kwargs):
    """
    Exit menu either by disconnecting or logging in.
    """
    session = caller
    if kwargs.get("login"):
        account = kwargs.get("account")
        session.msg("|gLogging in ...|n")
        session.sessionhandler.login(session, account)
    else:
        session.sessionhandler.disconnect(session, "Goodbye! Logging off.")
    return "", {}


class MenuLoginEvMenu(EvMenu):
    """
    Version of EvMenu that does not display any of its options.
    """

    def node_formatter(self, nodetext, optionstext):
        return nodetext

    def options_formatter(self, optionlist):
        """
        Do not display the options, only the text.

        This function is used by EvMenu to format the text of nodes. The menu
        login is just a series of prompts so we disable all automatic display
        decorations and let the nodes handle everything on their own.
        """
        return ""
