from enum import Enum
from textwrap import dedent

from commands.default_cmdsets import MobCmdSet

from typeclasses import objects


class GenderType(Enum):
    MALE = "male"
    FEMALE = "female"
    AMBIGUOUS = "ambiguous"


class Mob(objects.Object):
    """
    This Mobile defaults to reimplementing some of the base Object's hook
    methods with the following functionality:
    """

    _content_types = ("mob",)

    ##############
    # Properties #
    ##############
    @property
    def gender(self):
        return self.attributes.get("gender", GenderType.AMBIGUOUS).value

    @gender.setter
    def gender(self, value: Enum):
        self.db.gender = value

    def at_object_creation(self):
        """
        Called the first time the object is created. We set up the base
        properties and flags here.
        """
        self.cmdset.add(MobCmdSet, persistent=True)

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
                    "control:perm(Admin)",  # edit locks/permissions, delete
                    "examine:perm(Builder)",  # examine properties
                    "view:all()",  # look at object (visibility)
                    "edit:perm(Admin)",  # edit properties/attributes
                    "delete:perm(Admin)",  # delete object
                    "get:superuser()",  # pick up object
                    "drop:superuser()",  # drop only that which you hold
                    "call:false()",  # allow to call commands on this object
                    "tell:perm(Admin)",  # allow emits to this object
                    "puppet:pperm(Developer)",
                    "teleport:perm(Admin)",
                    "teleport_here:perm(Admin)",
                ]
            )
        )  # lock down puppeting only to staff by default

    appearance_template = dedent(
        """
            {desc}
        """
    )

    def return_appearance(self, looker, **kwargs):
        """
        Main callback used by 'look' for the object to describe itself.
        This formats a description. By default, this looks for the `appearance_template`
        string set on this class and populates it with formatting keys
            'name', 'desc', 'exits', 'characters', 'things' as well as
            (currently empty) 'header'/'footer'. Each of these values are
            retrieved by a matching method `.get_display_*`, such as `get_display_name`,
            `get_display_footer` etc.

        Args:
            looker (Object): Object doing the looking. Passed into all helper methods.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call. This is passed into all helper methods.

        Returns:
            str: The description of this entity. By default this includes
                the entity's name, description and any contents inside it.

        Notes:
            To simply change the layout of how the object displays itself (like
            adding some line decorations or change colors of different sections),
            you can simply edit `.appearance_template`. You only need to override
            this method (and/or its helpers) if you want to change what is passed
            into the template or want the most control over output.

        """

        if not looker:
            return ""

        return self.format_appearance(
            self.appearance_template.format(
                desc=self.get_display_desc(looker, **kwargs),
            ),
            looker,
            **kwargs,
        )
