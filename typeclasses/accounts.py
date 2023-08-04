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
from evennia.utils.utils import is_iter

from typeclasses.channels import send_mudinfo

_MAX_NR_CHARACTERS = settings.MAX_NR_CHARACTERS


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

        addr = session.address or "unknown"
        sessions = (
            f"{self.sessions.count()} sessions total"
            if self.sessions.count() > 1
            else f"{self.sessions.count()} session total"
        )
        send_mudinfo(
            _("|GLogged in: {key} ({addr}) ({sessions})|n").format(
                key=self.key, addr=addr, sessions=sessions
            )
        )

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
        count = self.sessions.count() - 1
        sessions = (
            f"{count} sessions remaining"
            if count != 1
            else f"{count} session remaining"
        )
        send_mudinfo(
            _("|RLogged out: {key} ({sessions})|n").format(
                key=self.key, sessions=sessions
            )
        )

    ooc_appearance_template = (
        "{fill}\n"
        "{header}\n"
        "\n"
        "{sessions}\n"
        "\n"
        "|wAvailable Commands:|n\n"
        "    |wcreate <name>|n - Create a new character.\n"
        "    |wdelete <name>|n - Delete a character.\n"
        "    |wic [name]|n - Enter the game as character.\n"
        "\n"
        "{characters}\n"
        "{footer}\n"
        "{fill}\n"
    ).strip()

    def at_look(self, target=None, session=None, **kwargs):
        """
        Called when this object executes a look. It allows to customize
        just what this means.

        Args:
            target (Object or list, optional): An object or a list
                objects to inspect. This is normally a list of characters.
            session (Session, optional): The session doing this look.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).

        Returns:
            look_string (str): A prepared look string, ready to send
                off to any recipient (usually to ourselves)

        """
        if target and not is_iter(target):
            # single target - just show it
            if hasattr(target, "return_appearance"):
                return target.return_appearance(self)
            else:
                return f"{target} has no in-game appearance."

        # multiple targets - this is a list of characters
        # characters = list(tar for tar in target if tar) if target else []
        characters = self.db._playable_characters or []
        ncars = len(characters)
        sessions = self.sessions.all()
        nsess = len(sessions)

        if not nsess:
            # no sessions, nothing to report
            return ""

        # header text
        txt_header = f"Account |g{self.name}|n (you are Out-of-Character)"

        # sessions
        sess_strings = []
        for isess, sess in enumerate(sessions):
            ip_addr = (
                sess.address[0] if isinstance(sess.address, tuple) else sess.address
            )
            addr = f"{sess.protocol_flags['CLIENTNAME']} ({ip_addr})"
            if session and session.sessid == sess.sessid:
                sess_str = f"|w* {isess + 1}|n"
                width = min(sess.protocol_flags["SCREENWIDTH"][0], 56)
            else:
                sess_str = f"  {isess + 1}"

            sess_strings.append(f"  {sess_str} {addr}")

        txt_sessions = "|wConnected session(s):|n\n" + "\n".join(sess_strings)

        if not characters:
            txt_characters = "You don't have a character yet. Use |wcharcreate|n."
        else:
            max_chars = (
                "unlimited"
                if self.is_superuser or _MAX_NR_CHARACTERS is None
                else _MAX_NR_CHARACTERS
            )

            char_strings = []
            for char in characters:
                csessions = char.sessions.all()
                if csessions:
                    for sess in csessions:
                        # character is already puppeted
                        sid = sess in sessions and sessions.index(sess) + 1
                        if sess and sid:
                            char_strings.append(
                                f"  - |G{char.name}|n [{', '.join(char.permissions.all())}] "
                                f"(played by you in session {sid})"
                            )
                        else:
                            char_strings.append(
                                f"  - |R{char.name}|n [{', '.join(char.permissions.all())}] "
                                "(played by someone else)"
                            )
                else:
                    # character is "free to puppet"
                    char_strings.append(
                        f"  - {char.name} [{', '.join(char.permissions.all())}]"
                    )

            txt_characters = (
                f"Available character(s) ({ncars}/{max_chars}, |wic <name>|n to play):|n\n"
                + "\n".join(char_strings)
            )
        return self.ooc_appearance_template.format(
            fill="-" * width,
            header=txt_header,
            sessions=txt_sessions,
            characters=txt_characters,
            footer="",
        )

    def disconnect_session_from_account(self, session, reason=None):
        """
        Access method for disconnecting a given session from the
        account (connection happens automatically in the
        sessionhandler)

        Args:
            session (Session): Session to disconnect.
            reason (str, optional): Eventual reason for the disconnect.

        """
        import evennia

        evennia.SESSION_HANDLER.disconnect(session, reason)


class Guest(DefaultGuest):
    """
    This class is used for guest logins. Unlike Accounts, Guests and their
    characters are deleted after disconnection.
    """

    pass
