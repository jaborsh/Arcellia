from typeclasses.objects import Object


class BrokenBody(Object):  # (1,2)
    def at_object_creation(self):
        self.db.display_name = "|#9E768FBroken Body|n"
        self.db.desc = "The figure is a tragic centerpiece amidst the room's cartographic splendor. Seated with their cranium exposed to the whims of cruel fate, their visage is frozen in an eerie semblance of ponderous thought. The soft, vulnerable tissue of the brain is a stark contrast to the rigid discipline of the maps that encircle them. Traces of blood, now dry and darkened, have painted rivulets along their weathered skin - a macabre depiction of the body's fragility."
        self.db.senses = {
            "feel": "A visceral discomfort arises at the sight, a tension that coils in the pit of one's being, as if in the presence of nature's uncanny aberration.",
            "smell": "The metallic pungency of blood intermingles with the sterile scent of exposed cerebral matter.",
            "sound": "An unsettling silence emanates from the figure, their breaths having long since yielded to the quietude that now claims the air.",
            "taste": "Climically bitter, the mind's flesh exudes an intangible flavor that speaks to innermost sanctums violated.",
        }
        self.db.interaction = "world.tutorial.interactions.broken_body"

    def at_server_reload(self):
        self.at_object_creation()
