from typeclasses.containers import Container
from typeclasses.objects import Object


class BrokenBody(Object):  # (1,2)
    def at_object_creation(self):
        self.db.display_name = "|#9E768FBroken Body|n"
        self.db.desc = "The figure is a tragic centerpiece amidst the room's cartographic splendor. Seated with their cranium exposed to the whims of cruel fate, their visage is frozen in an eerie semblance of ponderous thought. The soft, vulnerable tissue of the brain is a stark contrast to the rigid discipline of the maps that encircle them. Traces of blood, now dry and darkened, have painted rivulets along their weathered skin - a macabre depiction of the body's fragility."
        self.db.senses = {
            "feel": "A visceral discomfort arises at the sight, a tension that coils in the pit of one's being, as if in the presence of nature's uncanny aberration.",
            "smell": "The metallic pungency of blood intermingles with the sterile scent of exposed cerebral matter.",
            "sound": "An unsettling silence emanates from the figure, their breaths having long since yielded to the quietude that now claims the air.",
            "taste": "Clinically bitter, the mind's flesh exudes an intangible flavor that speaks to innermost sanctums violated.",
        }
        self.db.interaction = "world.tutorial.interactions.broken_body"

    def at_server_reload(self):
        self.at_object_creation()


class WoodenChest(Container):
    def at_object_creation(self):
        self.db.display_name = "|YWooden Chest|n"
        self.db.desc = "Crafted from the heartwood of ancient trees, the chest's exterior is sheathed in grain patterns that swirl and weave across its surface like tales told in timber. The chest's sturdy form invites touch, the solid wood yielding ever so slightly to the caress of a curious hand. Stout, hand-carved legs support it, resembling the strong limbs of the very trees from whence it came. Its lid, hinged gracefully, appears to beckon one to witness the secrets nested within its hollow."
        self.db.senses = {
            "feel": "The chest's surface carries the subtle roughness of grain.",
            "smell": "It exudes a wholesome aroma of wood and resin, reminiscent of a forest at dawn.",
            "sound": "A soft creak accompanies the lifting of the lid.",
            "taste": "The air around it is laced with the faint, tannic flavor of bark and the earthiness of fallen leaves.",
        }
