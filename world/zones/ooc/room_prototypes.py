from evennia.utils import dedent

ROOM_PROTOTYPES = {
    (0, 0): {
        "prototype_parent": "xyz_room",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "key": "|CStaff Room|n",
        "desc": dedent(
            """
            A curious sanctuary hidden away from the din and tumult of Arcellia lies before you. It is a chamber at once grand and modest, where the veil between the magical and the mundane is drawn aside.
            
            A large hearth dominates one corner, but the flames that leap within it seem less concerned with warmth and more with casting a gentle, reassuring glow. In its light, a long, polished table gleams, cluttered with scattered remnants of discussions past - scrolls half-unfurled, quills long since abandoned, and goblets untouched save for a sip or two of some honeyed elixir.
            """
        ),
        # "senses": {
        #     "feel": "A frigid draft meanders through the space, carrying the unwelcome embrace of the grave.",
        #     "smell": "The brine of the ocean mingles with the melancholy perfume of untreated wood and forlorn dreams.",
        #     "sound": "The muted groans of the ship's hull, a morose lullaby to the departed, fills the eerie silence.",
        #     "taste": "The air bears the faint brine of tears unwept, a taste of salt upon the tongue.",
        # },
        # "details": {
        #     "bunks": "A singular bunk stands apart, of furnishing sparse and unadorned; it is here the sole waking soul finds themselves, untethered from death's silent banquet."
        # },
    },
}
