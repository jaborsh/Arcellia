from typeclasses import mobs


class QueenEveline(mobs.Mob):
    def at_object_creation(self):
        self.db.display_name = "|#9932CCQueen Eveline|n"
        self.db.desc = "An enigmatic figure adorned in the regalia befitting her esteemed position. Her stature is one of dignified grace, commanding respect with an effortless poise that belies the strength forged from her rule. Flowing robes of state, a tapestry of the realm's finest silks, drape around her in cascades of color that shift with the light, each hue a chapter in the story of her sovereignty. Intricate embroidery, threaded with gold and gemstones, traces the history and triumphs of her lineage across the fabric of her garment. Upon her head, a crown sits with understated opulence, the stones set within it catching the eye with their lustrous depths. Her gaze is both kind and piercing, reflecting a sage wisdom that governs not just lands and laws, but the hearts of her people."
        self.db.senses = {
            "feel": "A formidable yet gentle aura envelops her, a juxtaposition that captures the simultaneous warmth and authority of her reign.",
            "smell": "The delicate fragrance of a sovereign, floral and refined, is marked with an undertone of the crisp parchment and ink of statecraft that occupies her daily life.",
            "sound": "Her voice when she speaks is lyrical yet decisive, a melodic command wrapped in the cadence of power and empathy.",
            "taste": "Her presence infuses the air with a subtle taste of complexity, as if the very essence of the land and its myriad flavors are personified in her demeanor.",
        }
        self.home = self.location


class ValarianCastleGuard(mobs.Mob):
    def at_object_creation(self):
        self.db.desc = "Clad in the colors of the kingdom, the castle guard stands as an embodiment of vigilance and duty. Upon his broad shoulders rests a cape that flutters gently with every vigilant turn. Armor of interlocking steel, polished to a mirror's sheen, envelops him, accented by a surcoat bearing the royal crest, vivid against the metallic backdrop. A helm forged with expert care shadows his eyes, the visor a slit through which the world is both guarded and observed. At his side, a sword hangs in patient repose, its hilt a craftsmanship's labor, the blade an extension of the guard's sworn oath. His presence, both seen and unseen, is woven into the very fabric of the castle - a silent sentry who breathes life into the stone and timber of the ramparts he so steadfastly protects."
        self.db.senses = {
            "feel": "The unmistakable sensations of security and steadfast resolve radiate from the guardsman, a physical embodiment of the castle's protective will.",
            "smell": "Scents of oiled leather and cold metal mingle in his presence, underlaid by the austere aroma of discipline and honor.",
            "sound": "The subtle clinking of his armor accompanies his movements, a metallic whisper that underscores the constant dance of vigilance and restraint.",
            "taste": "In the air around him lingers a taste as sharp as steel, as staunch and unyielding as his unwavering commitment to the post.",
        }
        self.home = self.location
