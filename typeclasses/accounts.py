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

import os

from django.conf import settings
from django.utils.translation import gettext as _
from evennia.accounts.accounts import DefaultAccount, DefaultGuest
from evennia.objects.models import ObjectDB
from evennia.server.signals import SIGNAL_OBJECT_POST_PUPPET
from evennia.utils import class_from_module
from evennia.utils.utils import (
    is_iter,
    make_iter,
    to_str,
)
from server.conf import logger

_MAX_NR_CHARACTERS = settings.MAX_NR_CHARACTERS
_MAX_NR_SIMULTANEOUS_PUPPETS = settings.MAX_NR_SIMULTANEOUS_PUPPETS
_MULTISESSION_MODE = settings.MULTISESSION_MODE


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


    * available properties

     key (string) - name of account
     name (string)- wrapper for user.username
     aliases (list of strings) - aliases to the object. Will be saved to database as AliasDB entries but returned as strings.
     dbref (int, read-only) - unique #id-number. Also "id" can be used.
     date_created (string) - time stamp of object creation
     permissions (list of strings) - list of permission strings

     user (User, read-only) - django User authorization object
     obj (Object) - game object controlled by account. 'character' can also be used.
     sessions (list of Sessions) - sessions connected to this account
     is_superuser (bool, read-only) - if the connected user is a superuser

    * Handlers

     locks - lock-handler: use locks.add() to add new lock strings
     db - attribute-handler: store/retrieve database attributes on this self.db.myattr=val, val=self.db.myattr
     ndb - non-persistent attribute handler: same as db but does not create a database entry when storing data
     scripts - script-handler. Add new scripts to object with scripts.add()
     cmdset - cmdset-handler. Use cmdset.add() to add new cmdsets to object
     nicks - nick-handler. New nicks with nicks.add().

    * Helper methods

     msg(text=None, **kwargs)
     execute_cmd(raw_string, session=None)
     search(ostring, global_search=False, attribute_name=None, use_nicks=False, location=None, ignore_errors=False, account=False)
     is_typeclass(typeclass, exact=False)
     swap_typeclass(new_typeclass, clean_attributes=False, no_default=True)
     access(accessing_obj, access_type='read', default=False)
     check_permstring(permstring)

    * Hook methods (when re-implementation, remember methods need to have self as first arg)

     basetype_setup()
     at_account_creation()

     - note that the following hooks are also found on Objects and are
       usually handled on the character level:

     at_init()
     at_cmdset_get(**kwargs)
     at_first_login()
     at_post_login(session=None)
     at_disconnect()
     at_message_receive()
     at_message_send()
     at_server_reload()
     at_server_shutdown()

    """

    def at_account_creation(self):
        """
        This is called once, the very first time the account is created (i.e.
        the first time they register with the gamee). It's a good place to store
        attributes all accounts should have, like configuration values.
        """
        # set an (empty) attribute holding the characters this account has
        lockstring = (
            "attrread:perm(Admin);attredit:perm(Admins);attrcreate:perm(Admin);"
        )
        self.attributes.add("_main_character", None, lockstring=lockstring)
        self.attributes.add("_playable_characters", [], lockstring=lockstring)
        self.attributes.add("_saved_protocol_flags", {}, lockstring=lockstring)
        self.create_log_folder()

    def create_log_folder(self):
        """
        Create a log folder for the account.

        """
        account_log_dir = f"{settings.ACCOUNT_LOG_DIR}/{self.key.lower()}/"
        os.makedirs(account_log_dir, exist_ok=True)
        self.attributes.add("_log_folder", f"accounts/{self.key.lower()}/")

    def at_disconnect(self, reason=None, **kwargs):
        """
        This method is called when a player disconnects from the game.

        Args:
            reason (str, optional): The reason for the disconnection.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        Notes:
            - This method updates the session count and logs the player's logout information.
        """
        count = self.sessions.count() - 1
        sessions = f"{count} session{'s' if count != 1 else ''} remaining"
        logger.send_mudinfo(
            _("|RLogged out: {key} ({sessions})|n").format(
                key=self.key, sessions=sessions
            )
        )

    def at_post_login(self, session=None, **kwargs):
        """
        This method is called after a successful login.

        Args:
            session (Session, optional): The session object representing the connection. Defaults to None.
            **kwargs: Additional keyword arguments.

        Notes:
            - Loads saved protocol flags, if any, and updates the session flags.
            - Informs the client of successful login through an OOB message.
            - Logs the login event.
            - Auto-connects to the last connected object or main character if enabled.
            - Cleans up the `_playable_characters` list.
            - Displays the character selection screen or account look.

        Returns:
            None
        """
        # Load saved protocol flags, if any
        protocol_flags = self.attributes.get("_saved_protocol_flags", {})
        if session and protocol_flags:
            session.update_flags(**protocol_flags)

        # Inform the client of successful login through an OOB message
        if session:
            session.msg(logged_in={})

        # Log the login event
        addr = session.address or "unknown"
        sessions_count = self.sessions.count()
        sessions_str = (
            f"{sessions_count} session{'s' if sessions_count != 1 else ''} total"
        )
        logger.send_mudinfo(
            ("|GLogged in: {key} ({addr}) ({sessions})|n").format(
                key=self.key, addr=addr, sessions=sessions_str
            )
        )

        if settings.AUTO_PUPPET_ON_LOGIN:
            # Auto-connect to the last connected object or main character
            puppet = self.db._main_character or self.db._last_puppet
            if puppet:
                try:
                    self.puppet_object(session, puppet)
                    return
                except RuntimeError:
                    pass

        # Clean up the _playable_characters list
        self.db._playable_characters = [
            char for char in self.db._playable_characters if char
        ]

        # Display the character selection screen or account look
        target = self.db._playable_characters if settings.AUTO_PUPPET_ON_LOGIN else None
        self.msg(self.at_look(target=target, session=session), session=session)

    def at_look(self, target=None, session=None, **kwargs):
        """
        Display the out-of-character appearance of the account.

        Args:
            target (object, optional): The target object to look at. Defaults to None.
            session (Session, optional): The session associated with the account. Defaults to None.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The out-of-character appearance of the account.

        """
        ooc_appearance_template = (
            "{fill}\n"
            "{header}\n"
            "\n"
            "{characters}\n\n"
            "|wCharacter Commands:|n\n"
            "  |wcreate  <name>|n - Create a character.\n"
            "  |wdelete  <name>|n - Delete a character.\n"
            "  |wplay    [name]|n - Connect to a character.\n"
            "  |wsetmain [name]|n - Set your main character.\n"
            "\n"
            "|wGeneral Commands:|n\n"
            "  |wlook|n           - Show this screen.\n"
            "  |woptions|n        - Show and change options.\n"
            "  |wpassword|n       - Change your password.\n"
            "  |wquit|n           - Quit the game.\n"
            "  |wwho|n            - Show who is online.\n"
            "{footer}"
            "{fill}\n"
        ).strip()

        if target and not is_iter(target):
            if hasattr(target, "return_appearance"):
                return target.return_appearance(self)
            else:
                return f"{target} has no in-game appearance."

        characters = self.db._playable_characters or []
        sessions = self.sessions.all()

        if not sessions:
            return ""

        txt_header = f"Account: |g{self.name}|n (you are Out-of-Character)"

        sess_strings = []
        width = 56
        for isess, sess in enumerate(sessions, start=1):
            ip_addr = (
                sess.address[0] if isinstance(sess.address, tuple) else sess.address
            )
            addr = f"{sess.protocol_flags['CLIENTNAME']} ({ip_addr})"
            sess_str = (
                f"|w* {isess}|n"
                if session and session.sessid == sess.sessid
                else f"  {isess}"
            )
            width = min(sess.protocol_flags["SCREENWIDTH"][0], 56)
            sess_strings.append(f"  {sess_str} {addr}")

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
                        sid = sessions.index(sess) + 1 if sess in sessions else None
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
                    char_strings.append(
                        f"  - {char.name}"
                        + (" (Main)" if char == self.db._main_character else "")
                    )
            txt_characters = (
                f"|wAvailable Characters: |n[{len(characters)}/{max_chars}]|n\n"
                + "\n".join(char_strings)
            )

        return ooc_appearance_template.format(
            fill="-" * width,
            header=txt_header,
            characters=txt_characters,
            footer="",
        )

    def create_character(self, **kwargs):
        """
        Create a new character for the account.

        Args:
            **kwargs: Additional keyword arguments to customize the character creation.

        Returns:
            tuple: A tuple containing the created character object and a list of any errors encountered during creation.
        """
        character_key = kwargs.pop("key", self.key)
        character_ip = kwargs.pop("ip", self.db.creator_ip)
        character_permissions = kwargs.pop("permissions", self.permissions)

        # Load the appropriate Character class
        character_typeclass = kwargs.pop("typeclass", None)
        character_typeclass = (
            character_typeclass
            if character_typeclass
            else settings.BASE_CHARACTER_TYPECLASS
        )
        Character = class_from_module(character_typeclass)

        if "location" not in kwargs:
            kwargs["location"] = ObjectDB.objects.get_id(settings.START_LOCATION)

        # Create the character
        character, errs = Character.create(
            character_key,
            self,
            ip=character_ip,
            typeclass=character_typeclass,
            permissions=character_permissions,
            **kwargs,
        )
        if character:
            # Establish main if no other characters exist.
            if not self.db._playable_characters:
                self.db._main_character = character

            # Update playable character list
            if character not in self.characters:
                self.db._playable_characters.append(character)

            # We need to set this to have @ic auto-connect to this character
            self.db._last_puppet = character
        return character, errs

    def _handle_self_puppeting(self, obj, session):
        if obj.sessions.count():
            if _MULTISESSION_MODE in (1, 3):
                txt1 = f"Sharing |c{obj.name}|n with another of your sessions."
                txt2 = (
                    f"|c{obj.name}|n|G is now shared from another of your sessions.|n"
                )
                self.msg(txt1, session=session)
                self.msg(txt2, session=obj.sessions.all())
            else:
                txt1 = f"Taking over |c{obj.name}|n from another of your sessions."
                txt2 = f"|c{obj.name}|n|R is now acted from another of your sessions.|n"
                self.msg(txt1, session=session)
                self.msg(txt2, session=obj.sessions.all())
                self.unpuppet_object(obj.sessions.get())

    def puppet_object(self, session, obj):
        # Safety checks
        if not obj:
            raise RuntimeError("Object not found")
        if not session:
            raise RuntimeError("Session not found")

        # Check if already puppeting the object
        if self.get_puppet(session) == obj:
            self.msg("You are already puppeting this object.")
            return

        # Check access permissions
        if not obj.access(self, "puppet"):
            self.msg(f"You don't have permission to puppet '{obj.key}'.")
            return

        # Check if the object is already puppeted
        if obj.account:
            if obj.account == self:
                self._handle_self_puppeting(obj, session)
            elif obj.account.is_connected and not self.is_superuser:
                self.msg(
                    _("|c{key}|R is already puppeted by another Account.").format(
                        key=obj.key
                    )
                )
                return

        # Cleanly unpuppet the previous object puppeted by this session
        if session.puppet:
            self.unpuppet_object(session)

        # Check the maximum number of simultaneous puppets
        if _MAX_NR_SIMULTANEOUS_PUPPETS is not None:
            already_puppeted = self.get_all_puppets()
            if (
                not self.is_superuser
                and not self.check_permstring("Developer")
                and obj not in already_puppeted
                and len(already_puppeted) >= _MAX_NR_SIMULTANEOUS_PUPPETS
            ):
                self.msg(
                    _(
                        f"You cannot control any more puppets (max {_MAX_NR_SIMULTANEOUS_PUPPETS})"
                    )
                )
                return

        # Perform the puppeting
        obj.at_pre_puppet(self, session=session)
        obj.tags.add("puppeted", category="account")
        obj.sessions.add(session)
        obj.account = self
        session.puid = obj.id
        session.puppet = obj
        obj.locks.cache_lock_bypass(obj)
        obj.at_post_puppet()
        SIGNAL_OBJECT_POST_PUPPET.send(sender=obj, account=self, session=session)

    def msg(self, text=None, from_obj=None, session=None, options=None, **kwargs):
        """
        Send a message to the account.

        Args:
            text (str, optional): The message text to send. Defaults to None.
            from_obj (object, optional): The object sending the message. Defaults to None.
            session (object or list, optional): The session(s) to send the message to. Defaults to None.
            options (dict, optional): Additional options for the message. Defaults to None.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        Raises:
            Exception: If an error occurs during message sending or receiving.

        Notes:
            - This method calls the `at_msg_send` hook for each sending object.
            - It calls the `at_msg_receive` hook for the account.
            - The message is sanitized before sending across the wire.
            - The message is sent to the specified session(s) and watcher(s).
        """
        if from_obj:
            # call hook
            for obj in make_iter(from_obj):
                try:
                    obj.at_msg_send(text=text, to_obj=self, **kwargs)
                except Exception:
                    # this may not be assigned.
                    logger.log_trace()
        try:
            if not self.at_msg_receive(text=text, **kwargs):
                # abort message to this account
                return
        except Exception:
            # this may not be assigned.
            pass

        kwargs["options"] = options

        if text is not None:
            if not (isinstance(text, str) or isinstance(text, tuple)):
                # sanitize text before sending across the wire
                try:
                    text = to_str(text)
                except Exception:
                    text = repr(text)
            kwargs["text"] = text

        # session relay
        sessions = make_iter(session) if session else self.sessions.all()
        for session in sessions:
            session.data_out(**kwargs)

        # Watcher relay
        for watcher in self.ndb._watchers or []:
            watcher.msg(text=kwargs["text"])


class Guest(DefaultGuest):
    """
    This class is used for guest logins. Unlike Accounts, Guests and their
    characters are deleted after disconnection.
    """

    pass
