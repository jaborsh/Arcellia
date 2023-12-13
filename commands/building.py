import re

from django.conf import settings
from django.db.models import Max, Min, Q
from parsing.colors import strip_ansi
from server.conf import logger

# from typeclasses.rooms import XYZRoom
from commands import building_menu
from commands.command import Command
from evennia import InterruptCommand
from evennia.commands.default import building, system
from evennia.contrib.grid.xyzgrid import commands as xyzcommands
from evennia.contrib.grid.xyzgrid.xyzroom import XYZRoom
from evennia.locks.lockhandler import LockException
from evennia.objects.models import ObjectDB
from evennia.utils import class_from_module, utils
from evennia.utils.eveditor import EvEditor
from evennia.utils.utils import dbref, inherits_from, list_to_string

CHAR_TYPECLASS = settings.BASE_CHARACTER_TYPECLASS
ROOM_TYPECLASS = settings.BASE_ROOM_TYPECLASS
EXIT_TYPECLASS = settings.BASE_EXIT_TYPECLASS

COMMAND_DEFAULT_CLASS = class_from_module(settings.COMMAND_DEFAULT_CLASS)
GOLD = "|#FFD700"

__all__ = (
    "CmdBuild",
    "CmdCopy",
    "CmdCpAttr",
    "CmdCreate",
    "CmdCreateExit",
    "CmdDescribe",
    "CmdDestroy",
    "CmdDetail",
    "CmdEdit",  # building_menu
    "CmdExamine",
    "CmdFind",
    "CmdLink",
    "CmdUnlink",
    "CmdLockstring",
    "CmdMap",
    "CmdMvAttr",
    "CmdRename",
    "CmdRoomState",
    "CmdSetAlias",
    "CmdSetAttribute",
    "CmdSetHome",
    "CmdSetGender",
    "CmdSpawn",
    "CmdTag",
    "CmdTickers",
    "CmdTunnel",
    "CmdTypeclass",
    "CmdWipe",
)


class CmdBuild(building.CmdDig):
    """
    Syntax: build[/switches] <roomname>[;alias;alias...][:typeclass]
            [= <exit_to_there>[;alias][:typeclass]]
            [, <exit_to_here>[;alias][:typeclass]]

    Switches:
       tel or teleport - move yourself to the new room

    Examples:
       build kitchen = north;n, south;s
       build house:myrooms.MyHouseTypeclass
       build sheer cliff;cliff;sheer = climb up, climb down

    This command is a convenient way to build rooms quickly; it creates the
    new room and you can optionally set up exits back and forth between your
    current room and the new one. You can add as many aliases as you
    like to the name of the room and the exits in question; an example
    would be 'north;no;n'.
    """

    key = "build"
    aliases = ["dig"]


class CmdCopy(building.CmdCopy):
    """
    Syntax: copy <original obj> [= <new name>][;alias;alias...]
            [:<new location>] [,<new name2> ...]

    Create one or more copies of an object. If you don't supply any targets,
    one exact copy of the original object will be created with the name *_copy.
    """

    key = "copy"


class CmdCpAttr(building.CmdCpAttr):
    """
    Syntax: cpattr[/switch] <obj>/<attr> = <obj1>/<attr1> [,<obj2>/<attr2>,<obj3>/<attr3>,...]
            cpattr[/switch] <obj>/<attr> = <obj1> [,<obj2>,<obj3>,...]
            cpattr[/switch] <attr> = <obj1>/<attr1> [,<obj2>/<attr2>,<obj3>/<attr3>,...]
            cpattr[/switch] <attr> = <obj1>[,<obj2>,<obj3>,...]

    Switches:
        move - delete the attribute from the source object after copying.

    Example:
      - cpattr coolness = Anna/chillout, Anna/nicety, Tom/nicety
            copies the coolness attribute (defined on yourself), to attributes
            on Anna and Tom.

    Copy the attribute one object to one or more attributes on another object.
    If you don't supply a source object, yourself is used.
    """

    key = "cpattr"
    aliases = ["copyattribute", "copyattr"]


class CmdCreate(building.CmdCreate):
    """
    Syntax: create[/drop] <objname>[;alias;alias...][:typeclass], <objname>...

    switch:
       drop - automatically drop the new object into your current
              location (this is not echoed). This also sets the new
              object's home to the current location rather than to you.

    Creates one or more new objects. If typeclass is given, the object
    is created as a child of this typeclass. The typeclass script is
    assumed to be located under types/ and any further
    directory structure is given in Python notation. So if you have a
    correct typeclass 'RedButton' defined in
    types/examples/red_button.py, you could create a new
    object of this type like this:

       create/drop button;red : examples.red_button.RedButton
    """

    key = "create"


class CmdCreateExit(xyzcommands.CmdXYZOpen):
    """
    Syntax: createexit <new exit>[;alias;..][:typeclass]
                 [,<return exit>[;alias;..][:typeclass]]] = <destination>
            createexit <new exit>[;alias;..][:typeclass]
                 [,<return exit>[;alias;..][:typeclass]]] = (X,Y,Z)

    Handles the creation of exits. If a destination is given, the exit
    will point there. The destination can also be given as an (X,Y,Z)
    coordinate on the XYZGrid - this command is used to link non-grid rooms to
    the grid and vice-versa.

    The <return exit> argument sets up an exit at the destination leading back
    to the current room. Apart from (X,Y,Z) coordinate, destination name can be
    given both as a #dbref and a name, if that name is globally unique.

    Examples:
        createexit kitchen = Kitchen
        createexit north, south = Town Center
        createexit cave mouth;cave = (3, 4, the small cave)
    """

    key = "createexit"

    def parse(self):
        building.ObjManipCommand.parse(self)

        self.location = self.caller.location
        if not self.args or not self.rhs:
            self.caller.msg(
                "Usage: createexit <new exit>[;alias...][:typeclass]"
                "[,<return exit>[;alias..][:typeclass]]] "
                "= <destination or (X,Y,Z)>"
            )
            raise InterruptCommand
        if not self.location:
            self.caller.msg("You cannot create an exit from a None-location.")
            raise InterruptCommand

        if all(char in self.rhs for char in ("(", ")", ",")):
            # search by (X,Y) or (X,Y,Z)
            inp = self.rhs.strip("()")
            X, Y, *Z = inp.split(",", 2)
            if not Z:
                self.caller.msg(
                    "A full (X,Y,Z) coordinate must be given for the destination."
                )
                raise InterruptCommand
            Z = Z[0]
            # search by coordinate
            X, Y, Z = str(X).strip(), str(Y).strip(), str(Z).strip()
            try:
                self.destination = XYZRoom.objects.get_xyz(xyz=(X, Y, Z))
            except XYZRoom.DoesNotExist:
                self.caller.msg(f"Found no target XYZRoom at ({X},{Y},{Z}).")
                raise InterruptCommand
        else:
            # regular search query
            self.destination = self.caller.search(self.rhs, global_search=True)
            if not self.destination:
                raise InterruptCommand

        self.exit_name = self.lhs_objs[0]["name"]
        self.exit_aliases = self.lhs_objs[0]["aliases"]
        self.exit_typeclass = self.lhs_objs[0]["option"]


def _desc_load(caller):
    return caller.db.evmenu_target.db.desc or ""


def _desc_save(caller, buf):
    """
    Save line buffer to the desc prop. This should
    return True if successful and also report its status to the user.
    """
    caller.db.evmenu_target.db.desc = buf
    caller.msg("Saved.")
    return True


def _desc_quit(caller):
    caller.attributes.remove("evmenu_target")
    caller.msg("Exited editor.")


class CmdDescribe(COMMAND_DEFAULT_CLASS):
    """
    Syntax: desc[/switch] [<obj> =] <description>

    Switches:
      edit - Open up a line editor for more advanced editing.
      del - Delete the description of an object. If another state is given, its
            description will be deleted.
      spring | summer | autumn | winter - room description to use in respective
                                          in-game season
      <other> - room description to use with an arbitrary room state.

    Sets the description an object. If an object is not given,
    describe the current room, potentially showing any additional stateful
    descriptions. The room states only work with rooms.

    Examples:
        desc/winter A cold winter scene.
        desc/edit/summer
        desc/burning This room is burning!
        desc A normal room with no state.
        desc/del/burning

    Rooms will automatically change season as the in-game time changes. You can
    set a specific room-state with the |wroomstate|n command.

    """

    key = "describe"
    aliases = ["desc"]
    switch_options = None
    locks = "cmd:perm(desc) or perm(Builder)"
    help_category = "Building"

    def parse(self):
        super().parse()

        self.delete_mode = "del" in self.switches
        self.edit_mode = not self.delete_mode and "edit" in self.switches

        self.object_mode = "=" in self.args

        # all other switches are names of room-states
        self.roomstates = [
            state for state in self.switches if state not in ("edit", "del")
        ]

    def edit_handler(self):
        if self.rhs:
            self.msg(
                "|rYou may specify a value, or use the edit switch, but not both.|n"
            )
            return
        if self.args:
            obj = self.caller.search(self.args)
        else:
            obj = self.caller.location or self.msg("|rYou can't describe oblivion.|n")
        if not obj:
            return

        if not (obj.access(self.caller, "control") or obj.access(self.caller, "edit")):
            self.caller.msg(
                f"You don't have permission to edit the description of {obj.key}."
            )
            return

        self.caller.db.eveditor_target = obj
        self.caller.db.eveditor_roomstates = self.roomstates
        # launch the editor
        EvEditor(
            self.caller,
            loadfunc=_desc_load,
            savefunc=_desc_save,
            quitfunc=_desc_quit,
            key="desc",
            persistent=True,
        )
        return

    def show_stateful_descriptions(self):
        location = self.caller.location
        room_states = location.room_states
        season = location.get_season()
        time_of_day = location.get_time_of_day()
        stateful_descs = location.all_desc()

        output = [
            f"Room {location.get_display_name(self.caller)} "
            f"Season: {season}. Time: {time_of_day}. "
            f"States: {', '.join(room_states) if room_states else 'None'}"
        ]
        other_active = False
        for state, desc in stateful_descs.items():
            if state is None:
                continue
            if state == season or state in room_states:
                output.append(f"Room state |w{state}|n |g(active)|n:\n{desc}")
                other_active = True
            else:
                output.append(f"Room state |w{state}|n:\n{desc}")

        active = " |g(active)|n" if not other_active else ""
        output.append(f"Room state |w(default)|n{active}:\n{location.db.desc}")

        sep = "\n" + "-" * 78 + "\n"
        self.caller.msg(sep.join(output))

    def func(self):
        caller = self.caller
        if not self.args and "edit" not in self.switches and "del" not in self.switches:
            if caller.location:
                # show stateful descs on the room
                self.show_stateful_descriptions()
                return
            else:
                caller.msg("You have no location to describe!")
                return

        if self.edit_mode:
            self.edit_handler()
            return

        if self.object_mode:
            # We are describing an object
            target = caller.search(self.lhs)
            if not target:
                return
            desc = self.rhs or ""
        else:
            # we are describing the current room
            target = caller.location or self.msg(
                "|rYou don't have a location to describe.|n"
            )
            if not target:
                return
            desc = self.args

        roomstates = self.roomstates
        if target.access(self.caller, "control") or target.access(self.caller, "edit"):
            if not roomstates or not hasattr(target, "add_desc"):
                # normal description
                target.db.desc = desc
                caller.msg(
                    f"The description was set on {target.get_display_name(caller)}."
                )
            elif roomstates:
                for roomstate in roomstates:
                    if self.delete_mode:
                        target.remove_desc(roomstate)
                        caller.msg(
                            f"The {roomstate}-description was deleted, if it existed."
                        )
                    else:
                        target.add_desc(desc, room_state=roomstate)
                        caller.msg(
                            f"The {roomstate}-description was set on"
                            f" {target.get_display_name(caller)}."
                        )
            else:
                target.db.desc = desc
                caller.msg(
                    f"The description was set on {target.get_display_name(caller)}."
                )
        else:
            caller.msg(
                "You don't have permission to edit the description "
                f"of {target.get_display_name(caller)}."
            )


class CmdDestroy(building.CmdDestroy):
    """
    Syntax: destroy[/switches] [obj, obj2, obj3, [dbref-dbref], ...]

    Switches:
       override - The destroy command will usually avoid accidentally
                  destroying account objects. This switch overrides this safety.
       force    - destroy without confirmation.

    Examples:
       destroy house, roof, door, 44-78
       destroy 5-10, flower, 45
       destroy/force north

    Destroys one or many objects. If dbrefs are used, a range to delete can be
    given, e.g. 4-10. Also the end points will be deleted. This command
    displays a confirmation before destroying, to make sure of your choice.
    You can specify the /force switch to bypass this confirmation.
    """

    key = "destroy"


class CmdDetail(Command):
    """
    sets a detail on a room

    Usage:
        detail[/del] <key> [= <description>]
        detail <key>;<alias>;... = description

    Example:
        detail
        detail walls = The walls are covered in ...
        detail castle;ruin;tower = The distant ruin ...
        detail/del wall
        detail/del castle;ruin;tower

    This command allows to show the current room details if you enter it
    without any argument.  Otherwise, sets or deletes a detail on the current
    room, if this room supports details like an extended room. To add new
    detail, just use the @detail command, specifying the key, an equal sign
    and the description.  You can assign the same description to several
    details using the alias syntax (replace key by alias1;alias2;alias3;...).
    To remove one or several details, use the @detail/del switch.

    """

    key = "detail"
    locks = "cmd:perm(Builder)"
    help_category = "Building"

    def func(self):
        location = self.caller.location
        if not self.args:
            details = location.db.details
            if not details:
                self.msg(
                    f"|rThe room {location.get_display_name(self.caller)} doesn't have any"
                    " details.|n"
                )
            else:
                details = sorted(
                    ["|y{}|n: {}".format(key, desc) for key, desc in details.items()]
                )
                self.msg("Details on Room:\n" + "\n".join(details))
            return

        if not self.rhs and "del" not in self.switches:
            detail = location.return_detail(self.lhs)
            if detail:
                self.msg("Detail '|y{}|n' on Room:\n{}".format(self.lhs, detail))
            else:
                self.msg("Detail '{}' not found.".format(self.lhs))
            return

        method = "add_detail" if "del" not in self.switches else "remove_detail"
        if not hasattr(location, method):
            self.caller.msg("Details cannot be set on %s." % location)
            return
        for key in self.lhs.split(";"):
            # loop over all aliases, if any (if not, this will just be
            # the one key to loop over)
            getattr(location, method)(key, self.rhs)
        if "del" in self.switches:
            self.caller.msg(f"Deleted detail '{self.lhs}', if it existed.")
        else:
            self.caller.msg(f"Set detail '{self.lhs}': '{self.rhs}'")


class CmdEdit(COMMAND_DEFAULT_CLASS):
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
            menu = building_menu.RoomBuildingMenu(caller, obj, title=title, width=width)
        else:
            obj_name = obj.get_display_name(caller)
            return self.msg(f"|r{obj_name} cannot be edited currently.|n")

        menu.open()


class CmdExamine(building.CmdExamine):
    """
    Syntax: examine [<object>[/attrname]]
            examine [*<account>[/attrname]]

    Switch:
        account - examine an Account (same as adding *)
        object - examine an Object (useful when OOC)
        script - examine a Script
        channel - examine a Channel

    The examine command shows detailed game info about an
    object and optionally a specific attribute on it.
    If object is not specified, the current location is examined.
    """

    key = "examine"
    aliases = ["ex", "exam"]


class CmdFind(building.CmdFind):
    """
    Syntax: find[/switches] <name or dbref or *account> [= dbrefmin[-dbrefmax]]
            locate - this is a shorthand for using the /loc switch.

    Switches:
        room       - only look for rooms (location=None)
        exit       - only look for exits (destination!=None)
        char       - only look for characters (BASE_CHARACTER_TYPECLASS)
        exact      - only exact matches are returned.
        loc        - display object location if exists and match has one result
        startswith - search for names starting with the string, rather than containing

    Searches the database for an object of a particular name or exact #dbref.
    Use *accountname to search for an account. The switches allows for
    limiting object matches to certain game entities. Dbrefmin and dbrefmax
    limits matches to within the given dbrefs range, or above/below if only
    one is given.
    """

    key = "find"
    aliases = ["search", "locate", "where"]

    def func(self):
        """Search functionality"""
        caller = self.caller
        switches = self.switches

        if not self.args or (not self.lhs and not self.rhs):
            caller.msg("Usage: find <string> [= low [-high]]")
            return

        if (
            "locate" in self.cmdstring
        ):  # Use option /loc as a default for locate command alias
            switches.append("loc")

        searchstring = self.lhs

        try:
            # Try grabbing the actual min/max id values by database aggregation
            qs = ObjectDB.objects.values("id").aggregate(low=Min("id"), high=Max("id"))
            low, high = sorted(qs.values())
            if not (low and high):
                raise ValueError(
                    f"{self.__class__.__name__}: Min and max ID not returned by aggregation;"
                    " falling back to queryset slicing."
                )
        except Exception as e:
            logger.log_trace(e)
            # If that doesn't work for some reason (empty DB?), guess the lower
            # bound and do a less-efficient query to find the upper.
            low, high = 1, ObjectDB.objects.all().order_by("-id").first().id

        if self.rhs:
            try:
                # Check that rhs is either a valid dbref or dbref range
                bounds = tuple(
                    sorted(
                        dbref(x, False) for x in re.split("[-\s]+", self.rhs.strip())
                    )
                )

                # dbref() will return either a valid int or None
                assert bounds
                # None should not exist in the bounds list
                assert None not in bounds

                low = bounds[0]
                if len(bounds) > 1:
                    high = bounds[-1]

            except AssertionError:
                caller.msg("Invalid dbref range provided (not a number).")
                return
            except IndexError as e:
                logger.log_err(
                    f"{self.__class__.__name__}: Error parsing upper and lower bounds of query."
                )
                logger.log_trace(e)

        low = min(low, high)
        high = max(low, high)

        is_dbref = utils.dbref(searchstring)
        is_account = searchstring.startswith("*")

        restrictions = ""
        if self.switches:
            restrictions = ", %s" % ", ".join(self.switches)

        if is_dbref or is_account:
            if is_dbref:
                # a dbref search
                result = caller.search(searchstring, global_search=True, quiet=True)
                string = "|wExact dbref match|n(#%i-#%i%s):" % (low, high, restrictions)
            else:
                # an account search
                searchstring = searchstring.lstrip("*")
                result = caller.search_account(searchstring, quiet=True)
                string = "|wMatch|n(#%i-#%i%s):" % (low, high, restrictions)

            if "room" in switches:
                result = result if inherits_from(result, ROOM_TYPECLASS) else None
            if "exit" in switches:
                result = result if inherits_from(result, EXIT_TYPECLASS) else None
            if "char" in switches:
                result = result if inherits_from(result, CHAR_TYPECLASS) else None

            if not result:
                string += "\n   |RNo match found.|n"
            elif not low <= int(result[0].id) <= high:
                string += (
                    f"\n   |RNo match found for '{searchstring}' in #dbref interval.|n"
                )
            else:
                result = result[0]
                string += f"\n   {result.get_display_name(caller)} - {result.path}|n"
                if "loc" in self.switches and not is_account and result.location:
                    string += (
                        f" (|wlocation|n: {result.location.get_display_name(caller)}|n)"
                    )
        else:
            # Not an account/dbref search but a wider search; build a queryset.
            # Searches for key and aliases
            if "exact" in switches:
                keyquery = Q(db_key__iexact=searchstring, id__gte=low, id__lte=high)
                aliasquery = Q(
                    db_tags__db_key__iexact=searchstring,
                    db_tags__db_tagtype__iexact="alias",
                    id__gte=low,
                    id__lte=high,
                )
            elif "startswith" in switches:
                keyquery = Q(
                    db_key__istartswith=searchstring, id__gte=low, id__lte=high
                )
                aliasquery = Q(
                    db_tags__db_key__istartswith=searchstring,
                    db_tags__db_tagtype__iexact="alias",
                    id__gte=low,
                    id__lte=high,
                )
            else:
                keyquery = Q(db_key__icontains=searchstring, id__gte=low, id__lte=high)
                aliasquery = Q(
                    db_tags__db_key__icontains=searchstring,
                    db_tags__db_tagtype__iexact="alias",
                    id__gte=low,
                    id__lte=high,
                )

            # Keep the initial queryset handy for later reuse
            result_qs = ObjectDB.objects.filter(keyquery | aliasquery).distinct()
            nresults = result_qs.count()

            # Use iterator to minimize memory ballooning on large result sets
            results = result_qs.iterator()

            # Check and see if type filtering was requested; skip it if not
            if any(x in switches for x in ("room", "exit", "char")):
                obj_ids = set()
                for obj in results:
                    if (
                        ("room" in switches and inherits_from(obj, ROOM_TYPECLASS))
                        or ("exit" in switches and inherits_from(obj, EXIT_TYPECLASS))
                        or ("char" in switches and inherits_from(obj, CHAR_TYPECLASS))
                    ):
                        obj_ids.add(obj.id)

                # Filter previous queryset instead of requesting another
                filtered_qs = result_qs.filter(id__in=obj_ids).distinct()
                nresults = filtered_qs.count()

                # Use iterator again to minimize memory ballooning
                results = filtered_qs.iterator()

            # still results after type filtering?
            if nresults:
                if nresults > 1:
                    header = f"{nresults} Matches"
                else:
                    header = "One Match"

                string = f"|w{header}|n(#{low}-#{high}{restrictions}):"
                res = None
                for res in results:
                    string += f"\n  {res.get_display_name(caller)}"
                    if res.location:
                        string += f" - {res.location.get_display_name(caller)}"
                if (
                    "loc" in self.switches
                    and nresults == 1
                    and res
                    and getattr(res, "location", None)
                ):
                    string += (
                        f" (|wlocation|n: |g{res.location.get_display_name(caller)}|n)"
                    )
            else:
                string = f"|wNo Matches|n(#{low}-#{high}{restrictions}):"
                string += f"\n   |RNo matches found for '{searchstring}'|n"

        # send result
        caller.msg(string.strip())


class CmdLink(building.CmdLink):
    """
    Syntax: link[/switches] <object> = <target>
            link[/switches] <object> =
            link[/switches] <object>

    Switch:
      twoway - connect two exits. For this to work, BOTH <object>
               and <target> must be exit objects.

    If <object> is an exit, set its destination to <target>. Two-way operation
    instead sets the destination to the *locations* of the respective given
    arguments.

    The second form (a lone =) sets the destination to None (same as
    the unlink command) and the third form (without =) just shows the
    currently set destination.
    """

    key = "link"


class CmdUnlink(building.CmdUnLink):
    """
    Syntax: unlink <Object>

    Unlinks an object, for example an exit, disconnecting
    it from whatever it was connected to.
    """

    key = "unlink"


class CmdLockstring(building.CmdLock):
    """
    Syntax: lock <object or *account>[ = <lockstring>]
            lock[/switch] <object or *account>/<access_type>

    Switch:
        del - delete given access type
        view - view lock associated with given access type (default)

    If no lockstring is given, shows all locks on
    object.

    Lockstring is of the form
       access_type:[NOT] func1(args)[ AND|OR][ NOT] func2(args) ...]
    Where func1, func2 ... valid lockfuncs with or without arguments.
    Separator expressions need not be capitalized.

    For example:
       'get: id(25) or perm(Admin)'

    The 'get' lock access_type is checked e.g. by the 'get' command.
    An object locked with this example lock will only be possible to pick up
    by Admins or by an object with id=25.

    You can add several access_types after one another by separating
    them by ';', i.e:
       'get:id(25); delete:perm(Builder)'
    """

    key = "lockstring"

    def func(self):
        """Sets up the command"""

        caller = self.caller
        if not self.args:
            string = "Syntax: lockstring <object>[ = <lockstring>] or lock[/switch] <object>/<access_type>"
            caller.msg(string)
            return

        if "/" in self.lhs:
            # call of the form lock obj/access_type
            objname, access_type = [p.strip() for p in self.lhs.split("/", 1)]
            obj = None
            if objname.startswith("*"):
                obj = caller.search_account(objname.lstrip("*"))
            if not obj:
                obj = caller.search(objname)
                if not obj:
                    return
            has_control_access = obj.access(caller, "control")
            if access_type == "control" and not has_control_access:
                # only allow to change 'control' access if you have 'control' access already
                caller.msg("You need 'control' access to change this type of lock.")
                return

            if not (has_control_access or obj.access(caller, "edit")):
                caller.msg("You are not allowed to do that.")
                return

            lockdef = obj.locks.get(access_type)

            if lockdef:
                if "del" in self.switches:
                    obj.locks.delete(access_type)
                    string = "deleted lock %s" % lockdef
                else:
                    string = lockdef
            else:
                string = f"{obj} has no lock of access type '{access_type}'."
            caller.msg(string)
            return

        if self.rhs:
            # we have a = separator, so we are assigning a new lock
            if self.switches:
                swi = ", ".join(self.switches)
                caller.msg(
                    f"Switch(es) |w{swi}|n can not be used with a "
                    "lock assignment. Use e.g. "
                    "|wlockstring/del objname/locktype|n instead."
                )
                return

            objname, lockdef = self.lhs, self.rhs
            obj = None
            if objname.startswith("*"):
                obj = caller.search_account(objname.lstrip("*"))
            if not obj:
                obj = caller.search(objname)
                if not obj:
                    return
            if not (obj.access(caller, "control") or obj.access(caller, "edit")):
                caller.msg("You are not allowed to do that.")
                return
            ok = False
            lockdef = re.sub(r"\'|\"", "", lockdef)
            try:
                ok = obj.locks.add(lockdef)
            except LockException as e:
                caller.msg(str(e))
            if "cmd" in lockdef.lower() and inherits_from(
                obj, "evennia.objects.objects.DefaultExit"
            ):
                # special fix to update Exits since "cmd"-type locks won't
                # update on them unless their cmdsets are rebuilt.
                obj.at_init()
            if ok:
                caller.msg(f"Added lockstring '{lockdef}' to {obj}.")
            return

        # if we get here, we are just viewing all locks on obj
        obj = None
        if self.lhs.startswith("*"):
            obj = caller.search_account(self.lhs.lstrip("*"))
        if not obj:
            obj = caller.search(self.lhs)
        if not obj:
            return
        if not (obj.access(caller, "control") or obj.access(caller, "edit")):
            caller.msg("You are not allowed to do that.")
            return
        caller.msg("\n".join(obj.locks.all()))


class CmdMap(xyzcommands.CmdMap):
    """
    Syntax: map [Zcoord]
            map list

    Show a map of an area.
    """

    locks = "cmd:perm(Builder)"
    help_category = "Building"


class CmdMvAttr(building.CmdMvAttr):
    """
    Syntax: mvattr[/switch] <obj>/<attr> = <obj1>/<attr1> [,<obj2>/<attr2>,<obj3>/<attr3>,...]
            mvattr[/switch] <obj>/<attr> = <obj1> [,<obj2>,<obj3>,...]
            mvattr[/switch] <attr> = <obj1>/<attr1> [,<obj2>/<attr2>,<obj3>/<attr3>,...]
            mvattr[/switch] <attr> = <obj1>[,<obj2>,<obj3>,...]

    Switches:
      copy - Don't delete the original after moving.

    Move an attribute from one object to one or more attributes on another
    object. If you don't supply a source object, yourself is used.
    """

    key = "mvattr"
    aliases = ["moveattr"]


class CmdRename(building.ObjManipCommand):
    """
    Syntax: rename [*]<obj> <new name>[;alias,alias,...]

    Rename an object to something new. Use *obj to rename an account.

    Note: What is written as the 'new name' will be the object's new display
          string. Any aliases provided will not be shown visibly, but can be
          used to reference the item.
    """

    key = "rename"
    locks = "perm(Builder)"
    help_category = "Building"

    def func(self):
        caller = self.caller
        args = self.args.strip().split(" ", 1)
        if len(args) < 2:
            caller.msg("Syntax: rename <obj> <new name>[;alias,alias,...]")
            return

        obj_name, rest = args
        if ";" in rest:
            new_name, aliases = rest.split(";", 1)
            aliases = [strip_ansi(alias.strip()) for alias in aliases.split(",")]
        else:
            new_name = rest
            aliases = None

        if not new_name:
            caller.msg("No new name given.")
            return

        if new_name.startswith("|") and not new_name.endswith("|n"):
            new_name += "|n"

        new_key = strip_ansi(new_name)
        if obj_name.startswith("*"):
            # rename an account
            obj = caller.account.search(obj_name.lstrip("*"))
            if not obj:
                return

            if aliases:
                caller.msg("Accounts cannot have aliases.")
                return

            if not (obj.access(caller, "control") or obj.access(caller, "edit")):
                caller.msg(f"You don't have permission to rename {obj.username}.")
                return

            logger.log_sec(
                f"Rename: {caller} renamed {obj.username} to {new_key} (Account)."
            )
            caller.msg(f"Account {obj.username} renamed to {new_key}.")
            obj.username = new_key
            obj.save()
            obj.msg(f"Your account was renamed to {obj.username}.")
        else:
            # rename an object
            obj = caller.search(obj_name)
            if not obj:
                return

            if not (obj.access(caller, "control") or obj.access(caller, "edit")):
                caller.msg(f"You don't have permission to rename {obj.name}.")
                return

            if inherits_from(obj, "typeclasses.characters.Character"):
                aliases = None
                logger.log_sec(
                    f"Rename: {caller} renamed {obj.name} to {new_name} (Character)."
                )

            obj.key = new_key
            obj.display_name = new_name
            astring = ""
            if aliases:
                obj.aliases.clear()
                [obj.aliases.add(alias) for alias in aliases]
                astring = " (aliases: %s)" % ", ".join(aliases)

            if obj.destination:
                obj.flush_from_cache(force=True)

            type = obj.typeclass_path.split(".")[-1] or "Object"
            caller.msg(f"{type} {obj_name} renamed to {new_name}{astring}.")
            obj.msg(f"You've been renamed to {new_name}{astring}.")


class CmdRoomState(Command):
    """
    Toggle and view room state for the current room.

    Usage:
        roomstate [<roomstate>]

    Examples:
        roomstate spring
        roomstate burning
        roomstate burning      (a second time toggles it off)

    If the roomstate was already set, it will be disabled. Use
    without arguments to see the roomstates on the current room.

    """

    key = "roomstate"
    locks = "cmd:perm(Builder)"
    help_category = "Building"

    def parse(self):
        super().parse()
        self.room = self.caller.location
        if not self.room or not hasattr(self.room, "room_states"):
            self.caller.msg(
                "You have no current location, or it doesn't support room states."
            )
            raise InterruptCommand()

        self.room_state = self.args.strip().lower()

    def func(self):
        caller = self.caller
        room = self.room
        room_state = self.room_state

        if room_state:
            # toggle room state
            if room_state in room.room_states:
                room.remove_room_state(room_state)
                caller.msg(f"Cleared room state '{room_state}' from this room.")
            else:
                room.add_room_state(room_state)
                caller.msg(f"Added room state '{room_state}' to this room.")
        else:
            # view room states
            room_states = list_to_string(
                [f"'{state}'" for state in room.room_states]
                if room.room_states
                else ("None",)
            )
            caller.msg(
                "Room states (not counting automatic time/season) on"
                f" {room.get_display_name(caller)}:\n {room_states}"
            )


class CmdSetAlias(building.CmdSetObjAlias):
    """
    Syntax: setalias <obj> [= [alias[,alias,alias,...]]]
            setalias <obj> =
            setalias/category <obj> = [alias[,alias,...]]:<category>

    Switches:
        category - requires ending input with :category, to store the
                 given aliases with the given category.

    Assigns aliases to an object so it can be referenced by more
    than one name. Assign empty to remove all aliases from object. If
    assigning a category, all aliases given will be using this category.

    Observe that this is not the same thing as personal aliases
    created with the 'nick' command! Aliases set with alias are
    changing the object in question, making those aliases usable
    by everyone.
    """

    key = "setalias"
    aliases = []


class CmdSetAttribute(building.CmdSetAttribute):
    """
    Syntax: set[/switch] <obj>/<attr>[:category] = <value>
            set[/switch] <obj>/<attr>[:category] =            # delete attribute
            set[/switch] <obj>/<attr>[:category]              # view attribute
            set[/switch] *<account>/<attr>[:category] = <value>

    Switch:
        edit: Open the line editor (string values only)
        script: If we're trying to set an attribute on a script
        channel: If we're trying to set an attribute on a channel
        account: If we're trying to set an attribute on an account
        room: Setting an attribute on a room (global search)
        exit: Setting an attribute on an exit (global search)
        char: Setting an attribute on a character (global search)
        character: Alias for char, as above.

    Example:
        set self/foo = "bar"
        set/delete self/foo
        set self/foo = $dbref(#53)

    Sets attributes on objects. The second example form above clears a
    previously set attribute while the third form inspects the current value of
    the attribute (if any). The last one (with the star) is a shortcut for
    operating on a player Account rather than an Object.

    If you want <value> to be an object, use $dbef(#dbref) or
    $search(key) to assign it. You need control or edit access to
    the object you are adding.

    The most common data to save with this command are strings and
    numbers. You can however also set Python primitives such as lists,
    dictionaries and tuples on objects (this might be important for
    the functionality of certain custom objects).  This is indicated
    by you starting your value with one of |c'|n, |c"|n, |c(|n, |c[|n
    or |c{ |n.

    Once you have stored a Python primitive as noted above, you can include
    |c[<key>]|n in <attr> to reference nested values in e.g. a list or dict.

    Remember that if you use Python primitives like this, you must
    write proper Python syntax too - notably you must include quotes
    around your strings or you will get an error.
    """

    key = "set"
    aliases = ["setattribute", "setattrib", "setattr"]


class CmdSetHome(building.CmdSetHome):
    """
    Syntax: sethome <obj> [= <home_location>]
            sethome <obj>

    The "home" location is a "safety" location for objects; they
    will be moved there if their current location ceases to exist. All
    objects should always have a home location for this reason.
    It is also a convenient target of the "home" command.

    If no location is given, just view the object's home location.
    """

    key = "sethome"


class CmdSetGender(Command):
    """
    Syntax: setgender <target> <gender>

    Genders Available:
        male       (he, him, his)
        female     (she, her, hers)
        neutral    (it, its)
        ambiguous  (they, them, their, theirs)
    """

    key = "setgender"
    locks = "cmd:perm(Builder)"
    help_category = "Building"

    gender_map = {
        "m": "male",
        "f": "female",
        "n": "neutral",
        "a": "ambiguous",
    }

    def func(self):
        caller = self.caller
        args = self.args.split(" ", 1)
        if len(args) < 2:
            return caller.msg(
                "Syntax: gender [m]ale || [f]emale || [n]eutral || [a]mbiguous"
            )

        target, gender = args
        target = caller.search(target, global_search=True)
        if not target:
            return

        if not (target.access(caller, "control") or target.access(caller, "edit")):
            return caller.msg(
                f"You don't have permission to regender {target.display_name}."
            )

        if gender[0] not in ("m", "f", "n", "a"):
            return caller.msg(
                "Syntax: gender [m]ale || [f]emale || [n]eutral || [a]mbiguous"
            )

        target.gender = self.gender_map[gender[0]]
        caller.msg(
            f"{target.display_name} has been assigned the {target.gender} gender."
        )
        target.msg(f"You've been assigned the {target.gender} gender.")


class CmdSpawn(building.CmdSpawn):
    """
    Syntax: spawn[/noloc] <prototype_key>
            spawn[/noloc] <prototype_dict>

            spawn/search [prototype_keykey][;tag[,tag]]
            spawn/list [tag, tag, ...]
            spawn/list modules    - list only module-based prototypes
            spawn/show [<prototype_key>]
            spawn/update <prototype_key>

            spawn/save <prototype_dict>
            spawn/edit [<prototype_key>]
            olc     - equivalent to spawn/edit

    Switches:
        noloc - allow location to be None if not specified explicitly. Otherwise,
                location will default to caller's current location.
        search - search prototype by name or tags.
        list - list available prototypes, optionally limit by tags.
        show, examine - inspect prototype by key. If not given, acts like list.
        raw - show the raw dict of the prototype as a one-line string for manual editing.
        save - save a prototype to the database. It will be listable by /list.
        delete - remove a prototype from database, if allowed to.
        update - find existing objects with the same prototype_key and update
                 them with latest version of given prototype. If given with /save,
                 will auto-update all objects with the old version of the prototype
                 without asking first.
        edit, menu, olc - create/manipulate prototype in a menu interface.

    Example:
        spawn GOBLIN
        spawn {"key":"goblin", "typeclass":"monster.Monster", "location":"#2"}
        spawn/save {"key": "grunt", prototype: "goblin"};;mobs;edit:all()
    \f
    Dictionary keys:
      |wprototype_parent|n - name of parent prototype to use. Required if
                             typeclass is not set. Can be a path or a list for
                             multiple inheritance (inherits left to right). If
                             set one of the parents must have a typeclass.
      |wtypeclass       |n - string. Required if prototype_parent is not set.
      |wkey             |n - string, the main object identifier
      |wlocation        |n - this should be a valid object or #dbref
      |whome            |n - valid object or #dbref
      |wdestination     |n - only valid for exits (object or dbref)
      |wpermissions     |n - string or list of permission strings
      |wlocks           |n - a lock-string
      |waliases         |n - string or list of strings.
      |wndb_|n<name>       - value of a nattribute (ndb_ is stripped)

      |wprototype_key|n    - name of this prototype. Unique. Used to
                             store/retrieve from db and update existing
                             prototyped objects if desired.
      |wprototype_desc|n   - desc of this prototype. Used in listings
      |wprototype_locks|n  - locks of this prototype. Limits who may use prototype
      |wprototype_tags|n   - tags of this prototype. Used to find prototype

      any other keywords are interpreted as Attributes and their values.

    The available prototypes are defined globally in modules set in
    settings.PROTOTYPE_MODULES. If spawn is used without arguments it
    displays a list of available prototypes.
    """

    key = "spawn"
    aliases = ["olc"]


class CmdTag(building.CmdTag):
    """
    Syntax: tag[/del] <obj> [= <tag>[:<category>]]
            tag/search <tag>[:<category]

    Switches:
        search - return all objects with a given Tag
        del - remove the given tag. If no tag is specified,
              clear all tags on object.

    Manipulates and lists tags on objects. Tags allow for quick
    grouping of and searching for objects.  If only <obj> is given, list all
    tags on the object.  If /search is used, list objects with the given tag.
    The category can be used for grouping tags themselves, but it should be
    used with restrain - tags on their own are usually enough to for most
    grouping schemes.
    """

    key = "tag"
    aliases = ["tags"]

    key = "tickers"
    help_category = "Building"
    locks = "cmd:perm(tickers) or perm(Builder)"


class CmdTickers(system.CmdTickers):
    """
    Syntax: tickers

    Note: Tickers are created, stopped and manipulated in Python code
    using the TickerHandler. This is merely a convenience function for
    inspecting the current status.
    """

    key = "tickers"
    help_category = "Building"


class CmdTunnel(building.CmdTunnel):
    """
    Syntax: tunnel[/switch] <direction>[:typeclass] [= <roomname>[;alias;alias;...][:typeclass]]

    Switches:
        oneway - do not create an exit back to the current location
        tel - teleport to the newly created room

    Example:
        tunnel n
        tunnel n = house;mike's place;green building

    This is a simple way to build using pre-defined directions:
     |wn,ne,e,se,s,sw,w,nw|n (north, northeast etc)
     |wu,d|n (up and down)
     |wi,o|n (in and out)
     |went,ex|n (enter and exit)

    The full names (north, in, southwest, etc) will always be put as
    main name for the exit, using the abbreviation as an alias (so an
    exit will always be able to be used with both "north" as well as
    "n" for example). Opposite directions will automatically be
    created back from the new room unless the /oneway switch is given.
    For more flexibility and power in creating rooms, use dig.
    """

    key = "tunnel"
    aliases = "tun"

    # store the direction, full name and its opposite
    directions = {
        "n": ("north", "s"),
        "ne": ("northeast", "sw"),
        "e": ("east", "w"),
        "se": ("southeast", "nw"),
        "s": ("south", "n"),
        "sw": ("southwest", "ne"),
        "w": ("west", "e"),
        "nw": ("northwest", "se"),
        "u": ("up", "d"),
        "d": ("down", "u"),
        "i": ("in", "o"),
        "o": ("out", "i"),
        "ent": ("enter", "ex"),
        "ex": ("exit", "ent"),
    }

    def func(self):
        """Implements the tunnel command"""

        if not self.args or not self.lhs:
            string = (
                "Syntax: tunnel[/switch] <direction>[:typeclass] [= <roomname>"
                "[;alias;alias;...][:typeclass]]"
            )
            self.caller.msg(string)
            return

        # If we get a typeclass, we need to get just the exitname
        exitshort = self.lhs.split(":")[0]

        if exitshort not in self.directions:
            string = (
                "tunnel can only understand the following directions: %s."
                % ",".join(sorted(self.directions.keys()))
            )
            string += "\n(use dig for more freedom)"
            self.caller.msg(string)
            return

        # retrieve all input and parse it
        exitname, backshort = self.directions[exitshort]
        backname = self.directions[backshort][0]

        # if we received a typeclass for the exit, add it to the alias(short name)
        if ":" in self.lhs:
            # limit to only the first : character
            exit_typeclass = ":" + self.lhs.split(":", 1)[-1]
            # exitshort and backshort are the last part of the exit strings,
            # so we add our typeclass argument after
            exitshort += exit_typeclass
            backshort += exit_typeclass

        roomname = "Some place"
        if self.rhs:
            roomname = self.rhs  # this may include aliases; that's fine.

        telswitch = ""
        if "tel" in self.switches:
            telswitch = "/teleport"
        backstring = ""
        if "oneway" not in self.switches:
            backstring = f", {backname};{backshort}"

        # build the string we will use to call dig
        digstring = f"build{telswitch} {roomname} = {exitname};{exitshort}{backstring}"
        self.execute_cmd(digstring)


class CmdTypeclass(building.CmdTypeclass):
    """
    Syntax: typeclass[/switch] <object> [= typeclass.path]
            typeclass/prototype <object> = prototype_key

            typeclasses or typeclass/list/show [typeclass.path]
            swap - this is a shorthand for using /force/reset flags.
            update - this is a shorthand for using the /force/reload flag.

    Switch:
        show, examine - display the current typeclass of object (default) or,
                        if given a typeclass path, show the docstring of that
                        typeclass.
        update - *only* re-run at_object_creation on this object
                 meaning locks or other properties set later may remain.
        reset - clean out *all* the attributes and properties on the object,
                basically making this a new clean object. This will also
                reset cmdsets!
        force - change to the typeclass also if the object already has a
                typeclass of the same name.
        list - show available typeclasses. Only typeclasses in modules actually
               imported or used from somewhere in the code will show up here
               (those typeclasses are still available if you know the path)
        prototype - clean and overwrite the object with the specified
                    prototype key - effectively making a whole new object.

    Example:
        type button = examples.red_button.RedButton
        type/prototype button=a red button

    If the typeclass_path is not given, the current object's typeclass is
    assumed.

    View or set an object's typeclass. If setting, the creation hooks of the
    new typeclass will be run on the object. If you have clashing properties on
    the old class, use /reset. By default you are protected from changing to a
    typeclass of the same name as the one you already have - use /force to
    override this protection.

    The given typeclass must be identified by its location using python
    dot-notation pointing to the correct module and class. If no typeclass is
    given (or a wrong typeclass is given). Errors in the path or new typeclass
    will lead to the old typeclass being kept. The location of the typeclass
    module is searched from the default typeclass directory, as defined in the
    server settings.
    """

    key = "typeclass"
    aliases = ["type", "parent", "swap", "update", "typeclasses"]


class CmdWipe(building.CmdWipe):
    """
    Syntax: wipe <object>[/<attr>[/<attr>...]]

    Example:
        wipe box
        wipe box/colour

    Wipes all of an object's attributes, or optionally only those
    matching the given attribute-wildcard search string.
    """

    key = "wipe"
