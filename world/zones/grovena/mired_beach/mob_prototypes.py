from world.zones.grovena.mired_beach import clothing_prototypes

MIRED_BEACH_VEILED_WOMAN = {
    "prototype_parent": "xyz_mob",
    "prototype_key": "mired_beach_veiled_woman",
    "typeclass": "world.xyzgrid.xyzmob.XYZMob",
    "key": "woman",
    "display_name": "|CVeiled Woman|n",
    "desc": "Her slender frame is poised beneath the shadow of a voluminous teal hood, which casts her sharp, calculating features into the veils of obscurity. Faint wisps of silver hair escape the hood, framing a face lined with secrets and scars, while her eyes, like twin embers smoldering within a sea of fog, seem to pierce through the very fabric of the soul. Her posture speaks of control, a delicate balance between grace and an untamed, almost dangerous power brimming beneath her reserved demeanor.",
    "senses": {
        "feel": "The air around her is cool and still, almost untouched by warmth or softness.",
        "smell": "A faint scent of cold iron and distant, rain-drenched fields clings to her presence.",
        "sound": "Her movements are nearly silent, save for the soft rustle of cloth against her skin, like whispers against stone.",
        "taste": "The air around her tastes metallic, like the edge of a blade, sharp and lingering.",
    },
    "inventory": {
        "clothing": [clothing_prototypes.MIRED_BEACH_VEILED_WOMAN_ROBE],
    },
}


MIRED_BEACH_MOBS = {
    (0, 1): [
        MIRED_BEACH_VEILED_WOMAN,
    ],
}
