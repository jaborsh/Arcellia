"""
Object

The Object is the "naked" base class for things in the game world.

Note that the default Character, Room and Exit does not inherit from
this Object, but from their respective default implementations in the
evennia library. If you want to use this class as a parent to change
the other types, you can do so by adding this as a multiple
inheritance.

"""

from django.utils.translation import gettext as _
from evennia.objects.objects import DefaultObject
from evennia.prototypes import spawner
from evennia.utils import logger
from evennia.utils.funcparser import ACTOR_STANCE_CALLABLES, FuncParser
from evennia.utils.utils import (
    lazy_property,
    make_iter,
    to_str,
)

from handlers.appearance import AppearanceHandler
from utils.text import wrap

PARSER = FuncParser(ACTOR_STANCE_CALLABLES)


class ObjectParent:
    """
    This is a mixin that can be used to override *all* entities inheriting at
    some distance from DefaultObject (Objects, Exits, Characters and Rooms).

    Just add any method that exists on `DefaultObject` to this class. If one
    of the derived classes has itself defined that same hook already, that will
    take precedence.
    """

    @property
    def display_name(self):
        return self.attributes.get("display_name", self.name)

    @display_name.setter
    def display_name(self, value: str):
        self.db.display_name = value

    @property
    def senses(self):
        return self.attributes.get("senses", {})

    @property
    def feel(self):
        return self.senses.get("feel", "You feel nothing interesting.")

    @feel.setter
    def feel(self, value: str):
        self.senses["feel"] = value

    @property
    def smell(self):
        return self.senses.get("smell", "You smell nothing interesting.")

    @smell.setter
    def smell(self, value: str):
        self.senses["smell"] = value

    @property
    def sound(self):
        return self.senses.get("sound", "You hear nothing interesting.")

    @sound.setter
    def sound(self, value: str):
        self.senses["sound"] = value

    @property
    def taste(self):
        return self.senses.get("taste", "You taste nothing interesting.")

    @taste.setter
    def taste(self, value: str):
        self.senses["taste"] = value


class Object(ObjectParent, DefaultObject):
    """
    This is the root typeclass object, implementing an in-game Evennia
    game object, such as having a location, being able to be
    manipulated or looked at, etc. If you create a new typeclass, it
    must always inherit from this object (or any of the other objects
    in this file, since they all actually inherit from BaseObject, as
    seen in src.object.objects).

    The BaseObject class implements several hooks tying into the game
    engine. By re-implementing these hooks you can control the
    system. You should never need to re-implement special Python
    methods, such as __init__ and especially never __getattribute__ and
    __setattr__ since these are used heavily by the typeclass system
    of Evennia and messing with them might well break things for you.


    * Base properties defined/available on all Objects

     key (string) - name of object
     name (string)- same as key
     dbref (int, read-only) - unique #id-number. Also "id" can be used.
     date_created (string) - time stamp of object creation

     account (Account) - controlling account (if any, only set together with
                       sessid below)
     sessid (int, read-only) - session id (if any, only set together with
                       account above). Use `sessions` handler to get the
                       Sessions directly.
     location (Object) - current location. Is None if this is a room
     home (Object) - safety start-location
     has_account (bool, read-only)- will only return *connected* accounts
     contents (list of Objects, read-only) - returns all objects inside this
                       object (including exits)
     exits (list of Objects, read-only) - returns all exits from this
                       object, if any
     destination (Object) - only set if this object is an exit.
     is_superuser (bool, read-only) - True/False if this user is a superuser

    * Handlers available

     aliases - alias-handler: use aliases.add/remove/get() to use.
     permissions - permission-handler: use permissions.add/remove() to
                   add/remove new perms.
     locks - lock-handler: use locks.add() to add new lock strings
     scripts - script-handler. Add new scripts to object with scripts.add()
     cmdset - cmdset-handler. Use cmdset.add() to add new cmdsets to object
     nicks - nick-handler. New nicks with nicks.add().
     sessions - sessions-handler. Get Sessions connected to this
                object with sessions.get()
     attributes - attribute-handler. Use attributes.add/remove/get.
     db - attribute-handler: Shortcut for attribute-handler. Store/retrieve
            database attributes using self.db.myattr=val, val=self.db.myattr
     ndb - non-persistent attribute handler: same as db but does not create
            a database entry when storing data

    * Helper methods (see src.objects.objects.py for full headers)

     search(ostring, global_search=False, attribute_name=None,
             use_nicks=False, location=None, ignore_errors=False, account=False)
     execute_cmd(raw_string)
     msg(text=None, **kwargs)
     msg_contents(message, exclude=None, from_obj=None, **kwargs)
     move_to(destination, quiet=False, emit_to_obj=None, use_destination=True)
     copy(new_key=None)
     delete()
     is_typeclass(typeclass, exact=False)
     swap_typeclass(new_typeclass, clean_attributes=False, no_default=True)
     access(accessing_obj, access_type='read', default=False)
     check_permstring(permstring)

    * Hooks (these are class methods, so args should start with self):

     basetype_setup()     - only called once, used for behind-the-scenes
                            setup. Normally not modified.
     basetype_posthook_setup() - customization in basetype, after the object
                            has been created; Normally not modified.

     at_object_creation() - only called once, when object is first created.
                            Object customizations go here.
     at_object_post_creation() - only called once, when object is first
                                created. Additional setup involving e.g.
                                prototype-set attributes can go here.
     at_object_post_spawn() - called when object is spawned from a prototype
                              or updated by the spawner to apply prototype
                              changes.
     at_object_delete() - called just before deleting an object. If returning
                            False, deletion is aborted. Note that all objects
                            inside a deleted object are automatically moved
                            to their <home>, they don't need to be removed here.


     at_init()            - called whenever typeclass is cached from memory,
                            at least once every server restart/reload
     at_cmdset_get(**kwargs) - this is called just before the command handler
                            requests a cmdset from this object. The kwargs are
                            not normally used unless the cmdset is created
                            dynamically (see e.g. Exits).
     at_pre_puppet(account)- (account-controlled objects only) called just
                            before puppeting
     at_post_puppet()     - (account-controlled objects only) called just
                            after completing connection account<->object
     at_pre_unpuppet()    - (account-controlled objects only) called just
                            before un-puppeting
     at_post_unpuppet(account) - (account-controlled objects only) called just
                            after disconnecting account<->object link
     at_server_reload()   - called before server is reloaded
     at_server_shutdown() - called just before server is fully shut down

     at_access(result, accessing_obj, access_type) - called with the result
                            of a lock access check on this object. Return value
                            does not affect check result.

     at_pre_move(destination)             - called just before moving object
                        to the destination. If returns False, move is cancelled.
     announce_move_from(destination)         - called in old location, just
                        before move, if obj.move_to() has quiet=False
     announce_move_to(source_location)       - called in new location, just
                        after move, if obj.move_to() has quiet=False
     at_post_move(source_location)          - always called after a move has
                        been successfully performed.
     at_object_leave(obj, target_location)   - called when an object leaves
                        this object in any fashion
     at_object_receive(obj, source_location) - called when this object receives
                        another object

     at_traverse(traversing_object, source_loc) - (exit-objects only)
                              handles all moving across the exit, including
                              calling the other exit hooks. Use super() to retain
                              the default functionality.
     at_post_traverse(traversing_object, source_location) - (exit-objects only)
                              called just after a traversal has happened.
     at_failed_traverse(traversing_object)      - (exit-objects only) called if
                       traversal fails and property err_traverse is not defined.

     at_msg_receive(self, msg, from_obj=None, **kwargs) - called when a message
                             (via self.msg()) is sent to this obj.
                             If returns false, aborts send.
     at_msg_send(self, msg, to_obj=None, **kwargs) - called when this objects
                             sends a message to someone via self.msg().

     return_appearance(looker) - describes this object. Used by "look"
                                 command by default
     at_desc(looker=None)      - called by 'look' whenever the
                                 appearance is requested.
     at_get(getter)            - called after object has been picked up.
                                 Does not stop pickup.
     at_drop(dropper)          - called when this object has been dropped.
     at_say(speaker, message)  - by default, called if an object inside this
                                 object speaks

    """

    @lazy_property
    def appearance(self):
        return AppearanceHandler(self)

    def get_display_name(self, looker=None, **kwargs):
        return self.appearance.get_display_name(looker, **kwargs)

    def get_display_desc(self, looker=None, **kwargs):
        return self.appearance.get_display_desc(looker, **kwargs)

    def get_display_exits(self, looker=None, **kwargs):
        return self.appearance.get_display_exits(looker, **kwargs)

    def get_display_characters(self, looker=None, **kwargs):
        return self.appearance.get_display_characters(looker, **kwargs)

    def get_display_things(self, looker=None, **kwargs):
        return self.appearance.get_display_things(looker, **kwargs)

    def get_numbered_name(self, count, looker=None, **kwargs):
        return self.appearance.get_numbered_name(count, looker, **kwargs)

    def return_appearance(self, looker=None, **kwargs):
        return self.appearance.return_appearance(looker, **kwargs)

    def at_object_post_spawn(self, prototype=None):
        spawns = self.attributes.get("spawn", {})
        if spawns:
            self.spawn_clothing(spawns.get("clothing", []))
            self.spawn_equipment(spawns.get("equipment", []))
            self.spawn_inventory(spawns.get("inventory", []))
            self.spawn_stats(spawns.get("stats", {}))
            self.spawn_weapons(spawns.get("weapons", []))
            self.attributes.remove("spawn")

    def basetype_setup(self):
        """
        This sets up the default properties of an Object, just before
        the more general at_object_creation.

        You normally don't need to change this unless you change some
        fundamental things like names of permission groups.

        """
        # the default security setup fallback for a generic
        # object. Overload in child for a custom setup. Also creation
        # commands may set this (create an item and you should be its
        # controller, for example)

        self.locks.add(
            ";".join(
                [
                    "attack:false()",  # attacks against this object
                    "call:true()",  # allow to call commands on this object
                    "control:perm(Developer)",  # edit locks/permissions, delete
                    "delete:perm(Admin)",  # delete object
                    "drop:holds()",  # drop only that which you hold
                    "edit:perm(Admin)",  # edit properties/attributes
                    "examine:perm(Builder)",  # examine properties
                    "get:all()",  # pick up object
                    "puppet:pperm(Developer)",
                    "teleport:true()",
                    "teleport_here:true()",
                    "tell:perm(Admin)",  # allow emits to this object
                    "view:all()",  # look at object (visibility)
                ]
            )
        )  # lock down puppeting only to staff by default

    def at_look(self, target, **kwargs):
        """
        Called when this object performs a look. It allows to
        customize just what this means. It will not itself
        send any data.

        Args:
            target (DefaultObject): The target being looked at. This is
                commonly an object or the current location. It will
                be checked for the "view" type access.
            **kwargs: Arbitrary, optional arguments for users
                overriding the call. This will be passed into
                return_appearance, get_display_name and at_desc but is not used
                by default.

        Returns:
            str: A ready-processed look string potentially ready to return to the looker.

        """
        if not target.access(self, "view"):
            try:
                return "Could not find '%s'." % target.get_display_name(
                    self, **kwargs
                )
            except AttributeError:
                return "Could not find '%s'." % target.key

        description = target.return_appearance(self, **kwargs)

        # the target's at_desc() method.
        # this must be the last reference to target so it may delete itself when acted on.
        target.at_desc(looker=self, **kwargs)

        return description

    def announce_move_to(
        self,
        source_location,
        msg=None,
        mapping=None,
        move_type="move",
        **kwargs,
    ):
        """
        Announces the movement of the object to a new location.

        Args:
            source_location (Object): The previous location of the object.
            msg (str, optional): Additional message to include in the announcement.
            mapping (dict, optional): Mapping of variables for string formatting.
            move_type (str, optional): Type of movement (e.g., "move", "teleport").

        Returns:
            None
        """
        if not source_location and self.location.has_account:
            self.location.msg(
                _("You now have {name} in your possession.").format(
                    name=self.get_display_name(self.location)
                )
            )
            return

        origin = source_location
        destination = self.location
        exits = [
            o
            for o in destination.contents
            if o.location is destination and o.destination is origin
        ]

        if exits:
            exit_name = exits[0].get_display_name(self.location)
            if exit_name in [
                "north",
                "west",
                "south",
                "east",
                "northeast",
                "northwest",
                "southwest",
                "southeast",
            ]:
                exit_traversed = f"the {exit_name}"
            elif exit_name == "up":
                exit_traversed = "above"
            elif exit_name == "down":
                exit_traversed = "below"
            else:
                exit_traversed = exit_name
            string = _("{object} arrives from {exit_traversed}.")
        elif origin:
            string = _("{object} arrives from somewhere.")
        else:
            string = _("{object} arrives from {destination}.")

        mapping = mapping or {}
        mapping.update(
            {
                "object": self,
                "exit_traversed": exit_traversed if exits else "nowhere",
                "origin": origin or "nowhere",
                "destination": destination or "nowhere",
            }
        )

        destination.msg_contents(
            (string, {"type": move_type}),
            exclude=(self,),
            from_obj=self,
            mapping=mapping,
        )

    def announce_move_from(
        self, destination, msg=None, mapping=None, move_type="move", **kwargs
    ):
        """
        Announces the movement of the object from its current location to a destination.

        Args:
            destination (object): The destination object where the object is moving to.
            msg (str, optional): The message to be displayed when announcing the movement. If not provided,
                a default message will be used.
            mapping (dict, optional): A dictionary containing additional variables to be used in the message
                string. These variables can be referenced using placeholders in the message string.
            move_type (str, optional): The type of movement being performed. Defaults to "move".
            **kwargs: Additional keyword arguments that can be used to customize the behavior of the method.

        Returns:
            None

        """
        if not self.location:
            return

        string = msg or "{object} leaves {exit_traversed}."
        location = self.location
        exits = [
            o
            for o in location.contents
            if o.location is location and o.destination is destination
        ]

        mapping = mapping or {}
        mapping.update(
            {
                "object": self,
                "exit_traversed": (
                    exits[0].get_display_name(self.location)
                    if exits
                    else "in a poof of smoke"
                ),
            }
        )

        location.msg_contents(
            (string, {"type": move_type}),
            exclude=(self,),
            from_obj=self,
            mapping=mapping,
        )

    def msg(
        self, text=None, from_obj=None, session=None, options=None, **kwargs
    ):
        """
        Emits something to a session attached to the object.

        Keyword Args:
            text (str or tuple): The message to send. This
                is treated internally like any send-command, so its
                value can be a tuple if sending multiple arguments to
                the `text` oob command.
            from_obj (DefaultObject, DefaultAccount, Session, or list): object that is sending. If
                given, at_msg_send will be called. This value will be
                passed on to the protocol. If iterable, will execute hook
                on all entities in it.
            session (Session or list): Session or list of
                Sessions to relay data to, if any. If set, will force send
                to these sessions. If unset, who receives the message
                depends on the MULTISESSION_MODE.
            options (dict): Message-specific option-value
                pairs. These will be applied at the protocol level.
            **kwargs (string or tuples): All kwarg keys not listed above
                will be treated as send-command names and their arguments
                (which can be a string or a tuple).

        Notes:
            The `at_msg_receive` method will be called on this Object.
            All extra kwargs will be passed on to the protocol.

        """
        # try send hooks
        if from_obj:
            for obj in make_iter(from_obj):
                try:
                    obj.at_msg_send(text=text, to_obj=self, **kwargs)
                except Exception:
                    logger.log_trace()
        kwargs["options"] = options
        try:
            if not self.at_msg_receive(text=text, from_obj=from_obj, **kwargs):
                # if at_msg_receive returns false, we abort message to this object
                return
        except Exception:
            logger.log_trace()

        if text:
            parse_caller = from_obj if from_obj else self
            if isinstance(text, tuple):
                text = (
                    PARSER.parse(text[0], caller=parse_caller, receiver=self),
                    *text[1:],
                )
            elif isinstance(text, str):
                text = PARSER.parse(text, caller=parse_caller, receiver=self)
            else:
                try:
                    text = to_str(text)
                except Exception:
                    text = repr(text)

            if kwargs.get("wrap") == "say":
                msg = text[0]
                pre_text = msg.split('"')[0] + '"'
                msg = '"'.join(msg.split('"')[1:])
                msg = wrap(
                    msg, text_width=kwargs.get("width", None), pre_text=pre_text
                )
                text = msg

            kwargs["text"] = text

        # relay to session(s)
        sessions = make_iter(session) if session else self.sessions.all()
        for session in sessions:
            session.data_out(**kwargs)

        for watcher in self.ndb._watchers or []:
            if kwargs.get("text", None):
                watcher.msg(text=kwargs["text"])

    def spawn_clothing(self, clothing):
        for prot in clothing:
            matching_clothes = [
                obj
                for obj in self.contents
                if obj.tags.has(prot["prototype_key"], "from_prototype")
            ]
            if matching_clothes:
                spawner.batch_update_objects_with_prototype(
                    prot, objects=matching_clothes, exact=False
                )
            else:
                prot["home"] = self
                prot["location"] = self
                obj = spawner.spawn(prot)[0]
                self.clothing.wear(obj)

    def spawn_equipment(self, equipment):
        for prot in equipment:
            matching_equipment = [
                obj
                for obj in self.contents
                if obj.tags.has(prot["prototype_key"], "from_prototype")
            ]
            if matching_equipment:
                spawner.batch_update_objects_with_prototype(
                    prot, objects=matching_equipment, exact=False
                )
            else:
                prot["home"] = self
                prot["location"] = self
                obj = spawner.spawn(prot)[0]
                self.equipment.wear(obj)

    def spawn_inventory(self, inventory):
        for prot in inventory:
            matching_inventory = [
                obj
                for obj in self.contents
                if obj.tags.has(prot["prototype_key"], "from_prototype")
            ]
            if matching_inventory:
                spawner.batch_update_objects_with_prototype(
                    prot, objects=matching_inventory, exact=False
                )
            else:
                prot["home"] = self
                prot["location"] = self
                spawner.spawn(prot)

    def spawn_stats(self, stats):
        for key, value in stats.items():
            self.stats.add(
                key,
                key.capitalize(),
                trait_type=value["trait_type"],
                base=value["base"],
                min=value["min"],
                max=value["max"],
            )

    def spawn_weapons(self, weapons):
        for prot in weapons:
            matching_weapons = [
                obj
                for obj in self.contents
                if obj.tags.has(prot["prototype_key"], "from_prototype")
            ]
            if matching_weapons:
                spawner.batch_update_objects_with_prototype(
                    prot, objects=matching_weapons, exact=False
                )
            else:
                prot["home"] = self
                prot["location"] = self
                obj = spawner.spawn(prot)[0]
                self.equipment.wear(obj)


class InteractiveObject(Object):
    """
    An interactive object.
    """

    def at_object_creation(self):
        self.locks.add("get:false()")
