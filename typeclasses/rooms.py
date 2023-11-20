"""
Room

Rooms are simple containers that has no location of their own.

"""

from textwrap import dedent

from evennia.objects.objects import DefaultRoom
from evennia.utils.utils import iter_to_str

from .objects import ObjectParent


class Room(ObjectParent, DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    # populated by `return_appearance`
    appearance_template = dedent(
        """
        {name}

            {desc}

            {exits}
        
        {characters}
        
        {things}
        """
    )

    def get_display_exits(self, looker, **kwargs):
        """
        Get the 'exits' component of the object description. Called by `return_appearance`.

        Args:
            looker (Object): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The exits display data.

        """

        def _filter_visible(obj_list):
            return (
                obj for obj in obj_list if obj != looker and obj.access(looker, "view")
            )

        exits = _filter_visible(self.contents_get(content_type="exit"))
        exit_names = iter_to_str(
            exit.get_display_name(looker, **kwargs) for exit in exits
        )

        return (
            f"|wObvious Exits: {exit_names}"
            if exit_names
            else "|wObvious Exits: None|n"
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

        # populate the appearance_template string.
        return self.format_appearance(
            self.appearance_template.format(
                name=self.get_display_name(looker, **kwargs),
                desc=self.get_display_desc(looker, **kwargs),
                exits=self.get_display_exits(looker, **kwargs),
                characters=self.get_display_characters(looker, **kwargs),
                things=self.get_display_things(looker, **kwargs),
            ),
            looker,
            **kwargs,
        )

    pass
