from typeclasses import rooms


class CreationRoom(rooms.XYRoom):
    """
    Parent for all creation rooms.
    """

    pass


class CreationRoomIntro(CreationRoom):
    """
    This is the introduction room for character creation.
    """

    pass


class CreationRoomRace(CreationRoom):
    """
    This is the room where characters select their race.
    """

    pass


class CreationRoomClass(CreationRoom):
    """
    This is the room where characters select their class.
    """

    pass


class CreationRoomBackground(CreationRoom):
    """
    This is the room where characters select their background.
    """

    pass


class CreationRoomAppearance(CreationRoom):
    """
    This is the room where characters select their appearance.
    """

    pass


class CreationRoomAttributes(CreationRoom):
    """
    This is the room where characters select their attributes.
    """

    pass
