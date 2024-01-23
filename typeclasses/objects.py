"""
Object

The Object is the "naked" base class for things in the game world.

Note that the default Character, Room and Exit does not inherit from
this Object, but from their respective default implementations in the
evennia library. If you want to use this class as a parent to change
the other types, you can do so by adding this as a multiple
inheritance.

"""
import re

import inflect
from django.utils.translation import gettext as _
from evennia.objects.objects import DefaultObject
from evennia.utils import lazy_property
from handlers import traits
from parsing.text import strip_ansi

_INFLECT = inflect.engine()


class ObjectParent:
    """
    This is a mixin that can be used to override *all* entities inheriting at
    some distance from DefaultObject (Objects, Exits, Characters and Rooms).

    Just add any method that exists on `DefaultObject` to this class. If one
    of the derived classes has itself defined that same hook already, that will
    take precedence.

    """


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
    def base(self):
        return traits.TraitHandler(self, db_attribute_key="base")

    @property
    def display_name(self):
        return self.attributes.get("display_name", self.name)

    @display_name.setter
    def display_name(self, value: str):
        self.db.display_name = value

    @property
    def senses(self):
        return self.attributes.get("senses", {})

    @senses.setter
    def senses(self, sense: str, value: str):
        self.db.senses[sense] = value

    @property
    def feel(self):
        return self.senses.get("feel", "You feel nothing interesting.")

    @property
    def smell(self):
        return self.senses.get("smell", "You smell nothing interesting.")

    @property
    def sound(self):
        return self.senses.get("sound", "You hear nothing interesting.")

    @property
    def taste(self):
        return self.senses.get("taste", "You taste nothing interesting.")

    @property
    def weight(self):
        return self.base.get("weight") or 0

    @weight.setter
    def weight(self, value):
        self.base.add("weight", value)

    def get_display_name(self, looker=None, **kwargs):
        """
        Displays the name of the object in a viewer-aware manner.

        Args:
            looker (TypedObject): The object or account that is looking
                at/getting inforamtion for this object. If not given, `.name` will be
                returned, which can in turn be used to display colored data.

        Returns:
            str: A name to display for this object. This can contain color codes and may
                be customized based on `looker`. By default this contains the `.key` of the object,
                followed by the DBREF if this user is privileged to control said object.

        Notes:
            This function could be extended to change how object names appear to users in character,
            but be wary. This function does not change an object's keys or aliases when searching,
            and is expected to produce something useful for builders.

        """
        if looker and self.locks.check_lockstring(looker, "perm(Builder)"):
            return "{}(#{})".format(self.display_name, self.id)
        return self.display_name

    def get_numbered_name(self, count, looker, **kwargs):
        """
        Return the numbered (singular, plural) forms of this object's key. This
        is by default called by return_appearance and is used for grouping
        multiple same-named of this object. Note that this will be called on
        *every* member of a group even though the plural name will be only shown
        once. Also the singular display version, such as 'an apple', 'a tree'
        is determined from this method.

        Args:
            count (int): Number of objects of this type
            looker (Object): Onlooker. Not used by default.

        Keyword Args:
            key (str): Optional key to pluralize. If not given, the object's `.name` property is
                used.

        Returns:
            tuple: This is a tuple `(str, str)` with the singular and plural forms of the key
                including the count.

        Examples:
            obj.get_numbered_name(3, looker, key="foo") -> ("a foo", "three foos")
        """

        plural_category = "plural_key"
        key = kwargs.get("key", self.display_name)

        # Regular expression for color codes
        color_code_pattern = (
            r"(\|(r|g|y|b|m|c|w|x|R|G|Y|B|M|C|W|X|\d{3}|#[0-9A-Fa-f]{6}))"
        )
        color_code_positions = [
            (m.start(0), m.end(0)) for m in re.finditer(color_code_pattern, key)
        ]

        # Split the key into segments of text and color codes
        segments = []
        last_pos = 0
        for start, end in color_code_positions:
            segments.append(key[last_pos:start])  # Text segment
            segments.append(key[start:end])  # Color code
            last_pos = end
        segments.append(key[last_pos:])  # Remaining text after last color code

        # Apply pluralization and singularization to each text segment
        plural_segments = []
        singular_segments = []
        for segment in segments:
            if re.match(color_code_pattern, segment):
                # Color code remains unchanged for both plural and singular segments
                plural_segments.append(segment)
                singular_segments.append(segment)
            else:
                # Apply pluralization to text segment
                plural_segment = (
                    _INFLECT.plural(segment, count) if segment.strip() else segment
                )
                plural_segments.append(plural_segment)

                # Apply singularization to text segment
                if len(singular_segments) == 2:
                    # Special handling when singular_segments has exactly two elements
                    segment = _INFLECT.an(segment) if segment.strip() else segment
                    split_segment = segment.split(" ")
                    singular_segment = (
                        strip_ansi(split_segment[0])
                        + singular_segments[1]
                        + " "
                        + " ".join(split_segment[1:])
                    )
                    singular_segments[1] = ""
                else:
                    singular_segment = segment
                singular_segments.append(singular_segment)

        plural = "".join(plural_segments)
        singular = "".join(singular_segments)

        # Alias handling as in the original function
        if not self.aliases.get(plural, category=plural_category):
            self.aliases.clear(category=plural_category)
            self.aliases.add(plural, category=plural_category)
            self.aliases.add(singular, category=plural_category)

        return singular, plural

    def announce_move_to(
        self, source_location, msg=None, mapping=None, move_type="move", **kwargs
    ):
        """
        Called after the move if the move was not quiet. At this point
        we are standing in the new location.
        """

        if not source_location and self.location.has_account:
            string = _("You now have {name} in your possession.").format(
                name=self.get_display_name(self.location)
            )
            self.location.msg(string)
            return

        origin = source_location
        destination = self.location
        exits = []
        if origin:
            exits = [
                o
                for o in destination.contents
                if o.location is destination and o.destination is origin
            ]

        if exits:
            if exits[0].get_display_name(self.location) in [
                "north",
                "west",
                "south",
                "east",
                "northeast",
                "northwest",
                "southwest",
                "southeast",
            ]:
                exit_traversed = f"the {exits[0].get_display_name(self.location)}"
            elif exits[0].get_display_name(self.location) in ["up"]:
                exit_traversed = "above"
            elif exits[0].get_display_name(self.location) in ["down"]:
                exit_traversed = "below"
            else:
                exit_traversed = f"{exits[0].get_display_name(self.location)}"
            string = _("{object} arrives from {exit_traversed}.")
        elif origin:
            string = _("{object} arrives from {origin}.")
        else:
            string = _("{object} arrives to {destination}.")

        if not mapping:
            mapping = {}

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
        Called if the move is to be announced. This is
        called while we are still standing in the old
        location.
        """
        if not self.location:
            return
        if msg:
            string = msg
        else:
            string = "{object} leaves {exit_traversed}."

        location = self.location
        exits = [
            o
            for o in location.contents
            if o.location is location and o.destination is destination
        ]

        if not mapping:
            mapping = {}

        mapping.update(
            {
                "object": self,
                "exit_traversed": exits[0].get_display_name(self.location)
                if exits
                else "an unknown exit",
            }
        )

        location.msg_contents(
            (string, {"type": move_type}),
            exclude=(self,),
            from_obj=self,
            mapping=mapping,
        )
