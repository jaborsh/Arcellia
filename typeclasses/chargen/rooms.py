from textwrap import dedent

from typeclasses import rooms


class CreationRoom(rooms.XYRoom):
    """
    Parent for all creation rooms.
    """

    appearance_template = dedent(
        """
        """
    )
