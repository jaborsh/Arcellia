from typeclasses import mobs


class ValarianCastleGuard(mobs.Mob):
    def at_object_creation(self):
        self.db.desc = "Clad in the colors of the kingdom, the castle guard stands as an embodiment of vigilance and duty. Upon his broad shoulders rests a cape that flutters gently with every vigilant turn. Armor of interlocking steel, polished to a mirror's sheen, envelops him, accented by a surcoat bearing the royal crest, vivid against the metallic backdrop. A helm forged with expert care shadows his eyes, the visor a slit through which the world is both guarded and observed. At his side, a sword hangs in patient repose, its hilt a craftsmanship's labor, the blade an extension of the guard's sworn oath. His presence, both seen and unseen, is woven into the very fabric of the castle - a silent sentry who breathes life into the stone and timber of the ramparts he so steadfastly protects."
        self.home = self.location
