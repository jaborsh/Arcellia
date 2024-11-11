"""
At_initial_setup module template

Custom at_initial_setup method. This allows you to hook special
modifications to the initial server startup process. Note that this
will only be run once - when the server starts up for the very first
time! It is called last in the startup process and can thus be used to
overload things that happened before it.

The module must contain a global function at_initial_setup().  This
will be called without arguments. Note that tracebacks in this module
will be QUIETLY ignored, so make sure to check it well to make sure it
does what you expect it to.

"""

from django.conf import settings
from django.utils.translation import gettext as _
from evennia.objects.models import ObjectDB
from evennia.server.initial_setup import (
    _get_superuser_account,
    collectstatic,
    reset_server,
)
from evennia.server.models import ServerConfig
from evennia.utils import create, dedent, logger

STAFF_ROOM_DESC = dedent(
    _(
        """
        A curious sanctuary hidden away from the din and tumult of Arcellia lies before you. It is a chamber at once grand and modest, where the veil between the magical and the mundane is drawn aside.
        
        A large hearth dominates one corner, but the flames that leap within it seem less concerned with warmth and more with casting a gentle, reassuring glow. In its light, a long, polished table gleams, cluttered with scattered remnants of discussions past - scrolls half-unfurled, quills long since abandoned, and goblets untouched save for a sip or two of some honeyed elixir.
        """
    )
)

MAP_X_TAG_CATEGORY = "room_x_coordinate"
MAP_Y_TAG_CATEGORY = "room_y_coordinate"
MAP_Z_TAG_CATEGORY = "room_z_coordinate"


def create_objects():
    """
    Creates the #1 account and Limbo room.

    """

    logger.log_info(
        "Initial setup: Creating objects (Account #1 and Staff room) ..."
    )

    # Set the initial User's account object's username on the #1 object.
    # This object is pure django and only holds name, email and password.
    superuser = _get_superuser_account()

    # Create an Account 'user profile' object to hold eventual
    # mud-specific settings for the AccountDB object.
    account_typeclass = settings.BASE_ACCOUNT_TYPECLASS

    # run all creation hooks on superuser (we must do so manually
    # since the manage.py command does not)
    superuser.swap_typeclass(account_typeclass, clean_attributes=True)
    superuser.basetype_setup()
    superuser.at_account_creation()
    superuser.locks.add(
        "examine:perm(Developer);edit:false();delete:false();boot:false();msg:all()"
    )
    # this is necessary for quelling to work correctly.
    superuser.permissions.add("Developer")

    # Limbo is the default "nowhere" starting room

    # Create the in-game god-character for account #1 and set
    # it to exist in Limbo.
    try:
        superuser_character = ObjectDB.objects.get(id=1)
    except ObjectDB.DoesNotExist:
        superuser_character, errors = superuser.create_character(
            key=superuser.username,
            nohome=True,
            description=_("This is User #1."),
        )
        if errors:
            raise Exception(str(errors))

    superuser_character.locks.add(
        "examine:perm(Developer);edit:false();delete:false();boot:false();msg:all();puppet:false()"
    )
    # we set this low so that quelling is more useful
    superuser_character.permissions.add("Developer")
    superuser_character.save()

    superuser.attributes.add("_first_login", True)
    superuser.attributes.add("_last_puppet", superuser_character)

    room_typeclass = "world.xyzgrid.xyzroom.XYZRoom"
    try:
        staff_room = ObjectDB.objects.get(id=2)
    except ObjectDB.DoesNotExist:
        tags = (
            (str(0), MAP_X_TAG_CATEGORY),
            (str(0), MAP_Y_TAG_CATEGORY),
            (str("OOC"), MAP_Z_TAG_CATEGORY),
        )
        staff_room = create.create_object(
            room_typeclass, _("Staff Room"), tags=tags, nohome=True
        )

    staff_room.db_typeclass_path = room_typeclass
    staff_room.db.desc = STAFF_ROOM_DESC.strip()
    staff_room.save()

    # # Now that the Staff Room exists, try to set the user up there (unless
    # # the creation hooks already fixed this).
    if not superuser_character.location:
        superuser_character.location = staff_room
    if not superuser_character.home:
        superuser_character.home = staff_room


def at_initial_setup():
    from world.xyzgrid.launchcmd import (
        _option_add as xyzgrid_add,
    )
    from world.xyzgrid.launchcmd import (
        _option_init as xyzgrid_init,
    )
    from world.xyzgrid.xyzgrid import get_xyzgrid

    xyzgrid_init()
    xyzgrid_add(
        "world.zones.ooc.map",
        "world.chargen.map",
        "world.zones.emberlyn.map",
        "world.zones.emberlyn.emberlyn_beach.map",
        "world.zones.emberlyn.emberlyn_catacombs.map",
    )
    get_xyzgrid().spawn(xyz=("*", "*", "*"))


def handle_setup(last_step=None):
    """
    Main logic for the module. It allows for restarting the
    initialization at any point if one of the modules should crash.

    Args:
        last_step (str, None): The last stored successful step, for starting
            over on errors. None if starting from scratch. If this is 'done',
            the function will exit immediately.

    """
    # setup sequence
    setup_sequence = {
        "create_objects": create_objects,
        "at_initial_setup": at_initial_setup,
        "collectstatic": collectstatic,
        "done": reset_server,
    }

    if last_step in ("done", -1):
        # this means we don't need to handle setup since
        # it already ran sucessfully once. -1 is the legacy
        # value for existing databases.
        return

    # determine the sequence so we can skip ahead
    steps = list(setup_sequence)
    steps = steps[steps.index(last_step) + 1 if last_step is not None else 0 :]

    # step through queue from last completed function. Once completed,
    # the 'done' key should be set.
    for stepname in steps:
        try:
            setup_sequence[stepname]()
        except Exception:
            # we re-raise to make sure to stop startup
            raise
        else:
            # save the step
            ServerConfig.objects.conf("last_initial_setup_step", stepname)
            if stepname == "done":
                # always exit on 'done'
                break
