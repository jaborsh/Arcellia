from typeclasses import mobs
from typeclasses.mobs import GenderType


class QueenEveline(mobs.Mob):
    def at_object_creation(self):
        self.db.display_name = "|#9932CCQueen Eveline|n"
        self.gender = GenderType.FEMALE
        self.db.desc = "An enigmatic figure adorned in the regalia befitting her esteemed position. Her stature is one of dignified grace, commanding respect with an effortless poise that belies the strength forged from her rule. Flowing robes of state, a tapestry of the realm's finest silks, drape around her in cascades of color that shift with the light, each hue a chapter in the story of her sovereignty. Intricate embroidery, threaded with gold and gemstones, traces the history and triumphs of her lineage across the fabric of her garment. Upon her head, a crown sits with understated opulence, the stones set within it catching the eye with their lustrous depths. Her gaze is both kind and piercing, reflecting a sage wisdom that governs not just lands and laws, but the hearts of her people."
        self.db.senses = {
            "feel": "A formidable yet gentle aura envelops her, a juxtaposition that captures the simultaneous warmth and authority of her reign.",
            "smell": "The delicate fragrance of a sovereign, floral and refined, is marked with an undertone of the crisp parchment and ink of statecraft that occupies her daily life.",
            "sound": "Her voice when she speaks is lyrical yet decisive, a melodic command wrapped in the cadence of power and empathy.",
            "taste": "Her presence infuses the air with a subtle taste of complexity, as if the very essence of the land and its myriad flavors are personified in her demeanor.",
        }
        self.home = self.location


class CedricSterling(mobs.Mob):
    # Leader of the Knights
    def at_object_creation(self):
        self.db.display_name = "|#4682B4Cedric Sterling|n"
        self.gender = GenderType.MALE
        self.db.desc = "He is armored in a suit that gleams with a patina born of a well-attended history of service; each dent and scratch upon the metal speaks silently of victory and sacrifice. His surcoat, emblazoned with the insignia of his honored position, is both a banner and a target, worn with a pride that is both fierce and humble. Upon his head rests a helm, its plume catching the air with the flourish of a penned signature upon the page of the battlefield. His eyes, visible beneath the brim, burn with a fervent earnestness, reflective of ideals held since knighthood's first, tentative steps. At his hip, a sword."
        self.db.senses = {
            "feel": "The knight exudes a resolute energy, the air about him charged with the magnetism of a lifetime spent in the pursuit of valor and honor.",
            "smell": "Scents of steel and leather mix with the faint musk of horse and earth, an alchemy of elements from a life lived both in and for the saddle.",
            "sound": "A subtle timbre of authority resonates in his voice, while his movements create a symphony of chinks and clanks, a melody of readiness and durability.",
            "taste": "The very presence of the knight suggests a taste of iron resolve and the stoic salt of sweat-earned through training and the heat of combat.",
        }
        self.home = self.location


class SeraphinaLightbringer(mobs.Mob):
    # Priestess
    def at_object_creation(self):
        self.db.display_name = "|#FFFFFFSeraphina Lightbringer|n"
        self.gender = GenderType.FEMALE
        self.db.desc = "The holy practitioner, a shepherdess of the faith, moves with a quiet grace, her vestments speaking of long-held traditions and devout meditations. Fabric of the gentlest blue, suggestive of the firmament, falls in soft folds around her, edged with the silver of celestial purity - each wave and weave sanctified and purposeful. A pendant of her devotion rests gently upon her chest, a talisman aglow with the light of her beliefs, its touch upon her skin a reminder of the eternal and the ethereal. Her features carry the calm of one who has looked beyond the veil and communed with the divine, her eyes pools of compassionate wisdom. The touch of her hands, when offered in blessing or solace, is a balm to troubled spirits, her very presence a sanctum of solace and an invocation of inner sanctity."
        self.db.senses = {
            "feel": "A profound serenity emanates from her, a tranquility that enwraps one in the comfort of a faith deep and unshaken.",
            "smell": "Faint traces of floral incense linger about her, a reminder of the quiet spaces of worship and contemplation that are her sanctuary.",
            "sound": "Her utterances are a soft litany of hope and contemplation, a gentle cadence that seems to weave serenity into the very air.",
            "taste": "The presence of sacred offerings is ever present, the symbolic flavor of divine communion filling the spaces she graces.",
        }
        self.home = self.location


class ReginaldArundel(mobs.Mob):
    # Noble
    def at_object_creation(self):
        self.db.display_name = "|#FFD700Reginald Arundel|n"
        self.gender = GenderType.MALE
        self.db.desc = "A noble of discerning taste and elevated station subtly commands attention as he navigates the courtly sphere. He is adorned in refined garments that speak of his lineage and affluence, the fabric richly dyed and complemented by intricate embroidery that tells of his family's heraldry. Rings adorn his fingers, each a glittering testament to alliances and favors, while a delicate chain of office hints at responsibilities and a role in the governance of the realm. His hair is coiffed, a fashion statement as deliberate as the cut of his doublet, and his posture is one of innate confidence, acquired through a lifetime of privilege and expectation. The noble's movements are measured, each gesture calibrated for impact, his manner as much a cloak of entitlement as the finely woven cloak that drapes his shoulders."
        self.db.senses = {
            "feel": "An air of self-assurance surrounds the noble, an intangible yet palpable atmosphere of breeding and cultural gravitas.",
            "smell": "A well-chosen fragrance accentuates his presence, a blend of rare spices and oils that leave a trail of sophistication in his wake.",
            "sound": "The timbre of his voice carries a cultivated resonance, articulating each word with the precision and command of one accustomed to being heard.",
            "taste": "His bearing suggests a life refined by lavish feasts and vintage wines, the taste of opulence never far from the lips of those who hold dominion.",
        }
        self.home = self.location


class AriaWhisperwind(mobs.Mob):
    # Sells spirits
    def at_object_creation(self):
        self.db.display_name = "|#00FF00Aria Whisperwind|n"
        self.gender = GenderType.FEMALE
        self.db.desc = "The female spirit-tuner moves through the world with a mystic's grace, her role as an interpreter of the ethereal realms etched in the very air that swirls around her. Cloaked in garments that shimmer with a spectral luminescence, her attire seems woven from the essence of the otherworldly, the threads capturing whispers of light and shadow. Her eyes, when met, are deep pools reflecting an understanding of the arcane, orbs that have gazed upon the unseen and returned with secrets held close. About her wrists and neck, jewelry of delicate filigree chimes with the softest of melodies, each note a key that unlocks the barriers between worlds."
        self.db.senses = {
            "feel": "A cool, tingling energy emanates from her, as if her being is in constant communion with the elements unseen by mortal eyes.",
            "smell": "Her aura bears an almost electrical ozone scent, mixed with the groundedness of earth and the freshness of open skies.",
            "sound": "There is a melodic undercurrent to her voice, a vibration that resonates with the unheard music of the spirit world.",
            "taste": "Her essence carries the mystifying taste of a world beyond, as if one could sample the periphery of the arcane on the tongue.",
        }
        self.home = self.location


class EzekielGrimblade(mobs.Mob):
    # Undead Hunter
    def at_object_creation(self):
        self.db.display_name = "|xEzekiel Grimblade|n"
        self.gender = GenderType.MALE
        self.db.desc = "The undead hunter is a figure of steely resolve, clad in attire that merges functionality with an almost clerical austerity. Dark leathers, reinforced with chainmail at the vulnerable points, gird him against the dangers of his grim vocation. His cloak, fastened with a clasp in the shape of a protective sigil, billows like a shadow made manifest. Vials of sacred oils and consecrated waters are strapped across his chest, a warrior's panoply against the restless dead. His eyes carry the weight of countless vigils and confrontations, yet they burn with an unyielding light - the beacon of his unwavering purpose. In his hands, weapons are an extension of his will, be they stakes honed from hallowed wood or blades etched with runes of banishment. Every line of his form speaks to an existence spent on the precipice between life and the unspeakable abyss, a sentinel who holds back the night with blade and faith."
        self.db.senses = {
            "feel": "The hunter exudes a grim determination, the ambient air charged with a vigilance borne from nights immersed in shadows and silence.",
            "smell": "The pungent mix of garlic, herbs, and the metallic tang of weaponry envelops him, the olfactory signature of one who is perpetually battle-ready.",
            "sound": "Each movement is accompanied by the quiet whisper of leather and the faint clink of his armaments, a symphony of readiness and restraint.",
            "taste": "There's an undertone of ash and hallowed ground, the residue of his confrontations with the unholy, lingering in the air.",
        }
        self.home = self.location


class ThornIronforge(mobs.Mob):
    # Blacksmith
    def at_object_creation(self):
        self.db.display_name = "|#704214Thorn Ironforge|n"
        self.gender = GenderType.MALE
        self.db.desc = "Clad in a leather apron that bears the proud marks of his trade - scorches, smudges, and the occasional singe - his attire is as practical as it is emblematic of his work. Robust muscles ripple along his arms, a testament to the physical nature of his craft, and his hands, calloused and strong, grip his tools with an easy authority honed by years at the anvil. His face, often smudged with soot, is alight with the intense focus of one whose work is both art and necessity. Strands of hair that escape from under his cap catch the light of the forge, framing a visage of steadfast concentration. The rhythm of his hammer on metal is the heartbeat of the smithy, each strike a note in the melody of creation."
        self.db.senses = {
            "feel": "The warmth from the forge envelops him, a tangible reminder of the fire's role in transforming raw substance into items of strength and utility.",
            "smell": "The mingling scents of coal, sweat, and iron fill the smithy, evoking the essence of hard work and the satisfaction of shaping the world's strong bones.",
            "sound": "His workshop is alive with the rich clamor of industry—the roar of the flames, the hiss of quenched steel, and the steadfast pound of the hammer.",
            "taste": "A metallic tang hovers in the air, a flavor as ancient as the earth's minerals that are coaxed into new forms by his skilled hands.",
        }
        self.home = self.location


class EvelynGraceworn(mobs.Mob):
    # Deathbed Companion
    def at_object_creation(self):
        self.db.display_name = "|#483D8BEvelyn Graceworn|n"
        self.gender = GenderType.FEMALE
        self.db.desc = "She moves with an otherworldly poise, garbed in layers of lavish ebony fabrics that play with the light as if drinking in the darkness and weaving it into elegance. Her figure, statuesque and enigmatic, carries the mystique of one who speaks softly yet is heard above the clamor. Delicate lace adorns her wrists and throat, the designs reminiscent of the intricate complexities of existence itself. The graceful arc of her neck bears an unassuming pendant, which seems a repository for silent, ancient wisdom rather than a simple adornment. Her silken hair, the color of the deepest midnight, cascades over her shoulders, a veil that hints at secrets untold. In the pools of her iridescent eyes, a hidden depth suggests an existence that surpasses the mere here and now, a subtle glimmer of something more, veiled behind the facade of her earthly beauty."
        self.db.senses = {
            "feel": "An air of serene composure surrounds her, a gentle yet firm countenance that belies the profound presence she carries.",
            "smell": "The scent about her is that of rare and delicate perfume, a bouquet that might be found only in the hidden crevices of a twilight garden.",
            "sound": "Her voice, when she chooses to speak, is melodic and measured, carrying the resonance of timeless whispers.",
            "taste": "The presence of such a figure imparts a taste of mystery, like the faintest hint of an unknown spice that teases the palate with its complexity.",
        }
        self.home = self.location


class LoreleiStormrider(mobs.Mob):
    # Adventurer
    def at_object_creation(self):
        self.db.display_name = "|#4169E1Lorelei Stormrider|n"
        self.gender = GenderType.FEMALE
        self.db.desc = "Sun-kissed skin bears the marks of the elements, while her keen eyes shimmer with the reflection of distant horizons and untold tales. Her attire is a practical medley of leather and sturdy fabrics, with hidden pockets and clever folds that betray a life on the road. A weathered, wide-brimmed hat is perched upon her head, shading her face and holding back hair that's tousled from the kiss of the winds. Boots, scuffed and well-worn, recount miles traveled and terrains conquered. Each movement is fluid, born of necessity and adaptation, and around her waist, tools of the trade dangle - compass, dagger, and a rope coiled with the wisdom of countless ascents and descents."
        self.db.senses = {
            "feel": "She carries an infectious energy, the tangible excitement of adventure that hangs around her like the very air of uncharted lands.",
            "smell": "The scent of earth and open skies is woven into his garments, a perfume that speaks of campfires and wild forests.",
            "sound": "The cadence of her voice is rich with enthusiasm, accented by the subtle symphony of gear that chimes with her every step.",
            "taste": "A taste of the untamed wild lingers in proximity to her, as if one could sample the freedom of exploration on the edges of shared conversation.",
        }
        self.home = self.location


class EldricShadowweaver(mobs.Mob):
    # Sorcerer
    def at_object_creation(self):
        self.db.display_name = "|#800080Eldric Shadowweaver|n"
        self.gender = GenderType.MALE
        self.db.desc = "He dons robes that seem spun from the very night sky, adorned with symbols and runes that pulse with a subtle inner light. His fingers, delicate and precise, are often seen tracing sigils in the air, weaving spells with the fluid grace of an ancient language. His eyes, gleaming with an uncanny intellect, hold depths that promise both the allure and peril of forbidden lore. Around his neck hangs an amulet of obscure origin, its stone alive with an otherworldly hum. Silver hair falls in a cascade over his shoulders, each strand seemingly charged with the static of a thousand learned secrets."
        self.db.senses = {
            "feel": "A palpable vibration of potential energy emanates from him, as if the very fabric of the cosmos bends subtly in his presence.",
            "smell": "A hint of ozone, punctuated by the ancient tang of incense and old parchment, swirls invisibly around him.",
            "sound": "His voice carries the timbre of authority and enigma, each uttered incantation harmonizing with the unseen frequencies of magic.",
            "taste": "The air around him is tinged with the sharpness of alchemical components and the elusive essence of a reality that extends beyond the tangible.",
        }
        self.home = self.location


class IsoldeNightshade(mobs.Mob):
    # Advisor
    def at_object_creation(self):
        self.db.display_name = "|#006400Isolde Nightshade|n"
        self.gender = GenderType.FEMALE
        self.db.desc = "A lady of discerning intellect and quiet authority navigates the intricate weavings of court and counsel with an assured grace. She is garbed not in finery, but in the elegantly understated attire of her office, marked by sharp lines and the subtle, rich hues that speak of her sober responsibilities. Her attire is scrupulously chosen for function and form, adorned with minimal jewelry that nonetheless indicates her station - a brooch here, a simple ring there, each piece a quiet testament to her esteem. With her hair pinned back in a fashion both practical and becoming, it allows her keen eyes to survey the court's happenings unobstructed. Precision and forethought mark her every gesture, her every utterance measured, weighted with the consideration of potential futures - a beacon of sagacity in the fluid dance of palace intrigue."
        self.db.senses = {
            "feel": "She exudes a firm resolve that tempers the air around her, a sense of unyielding stability amidst the courtly flux.",
            "smell": "A refined scent emanates from her, a blend of ink and parchment merged subtly with the delicate aroma of her personal tea blend.",
            "sound": "Her voice is a study in moderation, clear and composed, each word delivered with an economy that bespeaks her acumen.",
            "taste": "In her presence, one can almost perceive the taste of wisdom and strategy, the imperceptible flavor of prescience and deliberation.",
        }
        self.home = self.location


class SilasShadowsteel(mobs.Mob):
    # Silent Guard/Assassin
    def at_object_creation(self):
        self.db.display_name = "|xSilas Shadowsteel|n"
        self.gender = GenderType.MALE
        self.db.desc = "He is a figure of stoic vigilance, his visage an impassive mask that reveals neither thought nor emotion. Clad in armor that is both utilitarian and imposing, it merges seamlessly with the shadows of his silent watch. Each piece of his gear is chosen for silence and efficacy - darkened to prevent unwanted glints, oiled to silence any betraying creaks. His helm, with its narrow slit, reduces the world to a fragment worth defending, while muting his presence to a mere wraith in the peripheral vision of those he safeguards. Boots padded for quietude carry him like a whisper across the stone floors, and at his hip, weapons lie dormant, their lethality sheathed in the stillness of his stance."
        self.db.senses = {
            "feel": "A tacit aura encircles him, a sense of watchfulness that envelops like the cool shroud of dusk.",
            "smell": "He carries the scent of the materials with which he is clad—leather and metal, the faintest trace of oil used in their maintenance.",
            "sound": "The silence that is his namesake, a hushed breath of air that could be mistaken for stillness itself.",
            "taste": "A ghostly hint of vigilance seems to linger in the air, as if one could taste the quietude and resolve that he embodies.",
        }
        self.home = self.location


class BrynnMarketwell(mobs.Mob):
    # Vendor
    def at_object_creation(self):
        self.db.display_name = "|#FFA500Brynn Marketwell|n"
        self.gender = GenderType.FEMALE
        self.db.desc = "A vendor presides over her cache of curiosities, each selected with an intuitive eye for the exquisite. Her visage reflects tales of the many halls and corridors she's traversed; her hair, a woven crown of braids befitting her station as merchant queen. Her hands, adorned with rings of intricate design, flutter like birds over the objects of her trade, each gesture a brushstroke in the art of deal-making. She wears a dress of earthen hues, a fine yet practical attire, accented with a sash of embroidered silk that catches the light with subtlety. Upon her shoulders, a shawl of fine lace lies draped, softening the lines of commerce with a hint of grace and poise."
        self.db.senses = {
            "feel": "Around her lingers the tactile allure of her offerings—the softness of velvets, the cool touch of metals, and the comforting heft of bound tomes.",
            "smell": "The ambient fragrances of polished wood and dried herbs mingle with a personal note of lavender from her shawl.",
            "sound": "Her voice, a conspiratorial whisper, offers tales and legends of each piece she sells, weaving a tapestry of sound that entices and enchants.",
            "taste": "A subtlety flavors the air, like the delicate pleasure of freshly baked bread from the kitchens, echoing the delectable diversity of her goods.",
        }
        self.home = self.location


class SableBlackthorn(mobs.Mob):
    # Dung-Eater
    def at_object_creation(self):
        self.db.display_name = "|#800000Sable Blackthorn|n"
        self.gender = GenderType.MALE
        self.db.desc = "His clothing, though well-worn from journeys untold, retains an air of calculated carelessness; the dark leathers and cloak he dons are a practical uniform for skullduggery and escape. A glint of mischief dances in his narrowed eyes, which seem always appraising, always calculating. Silent and supple boots carry him with a predator's grace. An array of hidden sheaths and pockets betray a readiness for any eventuality, housing an assortment of blades and lockpicks. A shadow of stubble darkens his jawline, adding a roguish edge to his rakish allure."
        self.db.senses = {
            "feel": "A frisson of danger seems to cling to him, a palpable tension that thrills as much as it warns.",
            "smell": "The subtle blend of leather and steel mixes with the faintest hint of tobacco, a scent that speaks to late nights huddled in shadowed corners.",
            "sound": "His footfalls betray no sound, yet there's a certain presence in his silence, a whisper of threat that follows his every step.",
            "taste": "The very air around him tastes of intrigue, each breath a mingled essence of adventure and the unknown.",
        }
        self.home = self.location


class CastleValariaGuard(mobs.Mob):
    def at_object_creation(self):
        self.gender = GenderType.MALE
        self.db.desc = "Clad in the colors of the kingdom, the castle guard stands as an embodiment of vigilance and duty. Upon his broad shoulders rests a cape that flutters gently with every vigilant turn. Armor of interlocking steel, polished to a mirror's sheen, envelops him, accented by a surcoat bearing the royal crest, vivid against the metallic backdrop. A helm forged with expert care shadows his eyes, the visor a slit through which the world is both guarded and observed. At his side, a sword hangs in patient repose, its hilt a craftsmanship's labor, the blade an extension of the guard's sworn oath. His presence, both seen and unseen, is woven into the very fabric of the castle - a silent sentry who breathes life into the stone and timber of the ramparts he so steadfastly protects."
        self.db.senses = {
            "feel": "The unmistakable sensations of security and steadfast resolve radiate from the guardsman, a physical embodiment of the castle's protective will.",
            "smell": "Scents of oiled leather and cold metal mingle in his presence, underlaid by the austere aroma of discipline and honor.",
            "sound": "The subtle clinking of his armor accompanies his movements, a metallic whisper that underscores the constant dance of vigilance and restraint.",
            "taste": "In the air around him lingers a taste as sharp as steel, as staunch and unyielding as his unwavering commitment to the post.",
        }
        self.home = self.location
