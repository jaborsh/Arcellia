from textwrap import dedent

from world.xyzgrid.xyzroom import XYZRoom


class CreationRoom(XYZRoom):
    """
    Parent for all creation rooms.
    """

    appearance_template = dedent(
        """
        """
    )
