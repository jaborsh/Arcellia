"""
Account

The Account represents the game "account" and each login has only one
Account object. An Account is what chats on default channels but has no
other in-game-world existence. Rather the Account puppets Objects (such
as Characters) in order to actually participate in the game world.


Guest

Guest accounts are simple low-level accounts that are created/deleted
on the fly and allows users to test the game without the commitment
of a full registration. Guest accounts are deactivated by default; to
activate them, add the following line to your settings file:

    GUEST_ENABLED = True

You will also need to modify the connection screen to reflect the
possibility to connect with a guest account. The setting file accepts
several more options for customizing the Guest account system.

"""
from django.conf import settings
from django.utils.translation import gettext as _
from evennia.accounts.accounts import DefaultAccount, DefaultGuest

from typeclasses.channels import send_mudinfo


class Account(DefaultAccount):
    """
    This class describes the actual OOC account (i.e. the user connecting
    to the MUD). It does NOT have visual appearance in the game world (that
    is handled by the character which is connected to this). Comm channels
    are attended/joined using this object.

    It can be useful e.g. for storing configuration options for your game, but
    should generally not hold any character-related info (that's best handled
    on the character level).

    Can be set using BASE_ACCOUNT_TYPECLASS.
    """

    def at_post_login(self, session=None, **kwargs):
        """
        Called at the end of the login process, just before letting the account
        loose.

        Args:
            session (Session, optional): Session logging in, if any.
            **kwargs (dict): Arbitrary, optional arguments for users overriding
                             the call (unused by default).

        Notes:
            This is called *before* an eventual Character's `at_post_login`
            hook. By default it is used to set up auto-puppeting based on
            `MULTISESSION_MODE`.
        """
        # if we have saved protocol flags on ourselves, load them here.
        protocol_flags = self.attributes.get("_saved_protocol_flags", {})
        if session and protocol_flags:
            session.update_flags(**protocol_flags)

        # inform the client that we logged in through an OOB message
        if session:
            session.msg(logged_in={})

        send_mudinfo(_("|G{key} connected.|n").format(key=self.key))
        if settings.AUTO_PUPPET_ON_LOGIN:
            # in this mode we try to auto-connect to our last connected object, if any
            try:
                self.puppet_object(session, self.db._last_puppet)
            except RuntimeError:
                self.msg(_("The Character does not exist."))
                return
        else:
            # In this mode we don't auto-connect but by default end up at a character selection
            # screen. We execute look on the account.
            # we make sure to clean up the _playable_characters list in case
            # any was deleted in the interim.
            self.db._playable_characters = [
                char for char in self.db._playable_characters if char
            ]
            self.msg(
                self.at_look(target=self.db._playable_characters, session=session),
                session=session,
            )

    def at_disconnect(self, reason=None, **kwargs):
        """
        Called just before user is disconnected.

        Args:
            reason (str, optional): The reason given for the disconnect.
            **kwargs (dict): Arbitrary, optional arguments for users overriding
                             the call (unused by default).
        """
        reason = f" ({reason})." if reason else "."
        send_mudinfo(
            _("|R{key} disconnected{reason}|n").format(key=self.key, reason=reason)
        )


class Guest(DefaultGuest):
    """
    This class is used for guest logins. Unlike Accounts, Guests and their
    characters are deleted after disconnection.
    """

    pass
