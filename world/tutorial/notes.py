class Figure:  # (1,2)
    desc = "The figure is a tragic centerpiece amidst the room's cartographic splendor. Seated with their cranium exposed to the whims of cruel fate, their visage is frozen in an eerie semblance of ponderous thought. The soft, vulnerable tissue of the brain is a stark contrast to the rigid discipline of the maps that encircle them. Traces of blood, now dry and darkened, have painted rivulets along their weathered skin - a macabre depiction of the body's fragility."
    feel = "A visceral discomfort arises at the sight, a tension that coils in the pit of one's being, as if in the presence of nature's uncanny aberration."
    smell = "The metallic pungency of blood intermingles with the sterile scent of exposed cerebral matter."
    sound = "An unsettling silence emanates from the figure, their breaths having long since yielded to the quietude that now claims the air."
    taste = "Climically bitter, the mind's flesh exudes an intangible flavor that speaks to innermost sanctums violated."


class GoblinCorpse:  # (2,2)
    desc = "A lone goblin figure lies crumbled upon the cold floor, their once deft hands now stilled by irreversible decree. Clad in the intricate garb of high ranking kin, the corpse seems almost in repose, as if they lay down willingly."
    feel = "A chill emanates from the goblin's final resting place, as if they very air mourns the loss of the curious intellect that once inhabited the small, wiry frame."
    smell = "The scient of the corpse has been cleansed by the briny environment, leaving only the faintest trace of the sharp, earthy odors that are characteristic of goblinkind."
    sound = "The stillness enveloping the figure is profound, the absence of their characteristic chatter amplifying the oppressive silence that has befallen the map room."
    taste = "A subtle taste of iron lingers in the air, an echo of the lifeblood that once coursed with vigor through the goblin's industrious heart."


class Scimitar:  # (1,3)
    pass


class Handaxe:  # (1,3)
    pass


class Crossbow:  # (1,3)
    pass


class ShortSword:  # (1,3)
    pass


class HealingPotion:  # (1,3) & (4,2)
    desc = "Contained within a delicate vial of translucent glass, a vibrant elixir swirls with the promise of restorative powers. The liquid's color is a mesmerizing ruby red. Tiny bubbles occasionally rise to the surface."


class ImpCorpse:  # (1,3)
    # has handaxe and crossbow
    pass


class ThrallCorpse:  # (1,3)
    # has shortsword, simple robe, and potion of healing
    pass


class Cultist:
    desc = "A menacing figure stands apart from the desolation, a stark anomaly in the oppressive gloom. The cultist, draped in tattered robes that hang from their frame like the shrouds of the fallen, mutter incantations in a chilling, discordant tone. Their face is obscured by a cowl from which the glint of their eyes pierce the murk, alight with fervor for an unfathomable rite. With measured intent, they move, hands traced with symbols that seem to writhe and pulse with a life of their own upon their flesh - a dark communition etched into their very being."
    feel = "The cultist exudes a malevolent chill, a menacing draft of rituals best left unspoken."
    smell = "An underlying scent of bitter herbs and the coppery essence of spilled lifeblood is carried faintly on their wake, filling the hold with an unsettling aroma."
    sound = "The soft drone of their low chant reverberates off the stone and iron, an ominous rhythm that seeps into the stillness."
    taste = "The taste of dread hangs sharp in the air as something sinister unfolds with each of their uttered syllables."


class Eirlys:  # (4,3)
    desc = "Imprisoned within the hold, she is a visage of striking contrast against the gloom. Her hair is as dark as the depths outside, flowing and untamed, a nightfall unto itself. Complexion fair as if untouched by the sun's kiss, her eyes, a piercing turquoise, burn with an unquenched resolve. Her form is poised with a dancer's elegance and her hands, unblemished by toil, move with a deliberate grace that speaks to a life far removed from the rusted bars that now define her world."
    feel = "A certain stillness clings to Eirlys, her stoic calm palpable against the skin in defiance of the suffocating air."
    smell = "Her being exudes a faint perfume of wildflowers, a soft note that persists despite the dank confines of the hold."
    sound = "The rustle of movement carries softly."
    taste = "Close to her, the usual staleness is subtly laced with the crispness of open fields, an aromatic memory clinging stubbornly to her presence."

    DarkSlateDress = "The forlorn garment, fashioned of a dark slate fabric, hangs in tattered elegance. Tailored to flatter yet endure, the dress bears the marks of its storied past. Its hem is jagged, worn down to threads that whisper of long travel and haste. Sleeves are patched with careful stitches, a narrative of survival and adaptability. Stains of an undetermined origin mar the bodice and lower skirts while the faint rings of salt left by seawater leave it intertwined with the tumultuous sea."


class SacrificialCorpse:  # (4,2)
    desc = "Splayed across the cold expanse of the altar lies the remains of a woman, her nude form presented as the culmination of a horrific rite. Pale skin marred by the cruel incisions of ritualistic fervor stands in contrast to the unfeeling stone beneath her. Her vacant eyes gaze upwards, reflecting none of the room's infernal scarlet, the life within them extinguished in pursuit of some maleficent purpose. Her body is still, every curve and line an unnerving still life, an offering to the insatiable appetites of otherworldly occupants."
    feel = "A chilling draft seems to emanate from the woman's body, the coldness of death palpably radiating from the altar."
    smell = "The sharp scent of blood mixes with the innate fragrance of humanity lost, a nasal assault."
    sound = "An oppressive silence enshrouds her, the absence of breath or heartbeat rendering the air unnaturally still."
    taste = "A bitter taste pervade her, as if the air itself mourns the sacrilege and absorbs the essence of life so cruelly taken."


class CartilaginousChest:  # (4,2)
    desc = "Before the altar rests a chest, unsettling in its organic composition. Crafted not of wood or metal, its exterior appears hewn from cartilage, the white surface interlaced with a network of fine, sinewy fibers that give it a grotesque semblance of life. The chest's form is strangely malleable to the touch, its hardened yet pliant material warping slightly under pressure. On malformed protuberances it stands, mimicing the function of feet, and its lid seems to mock the notion of invitation with its eerie, flesh-like constitution."
    feel = "The tactile experience of the chest is unnervingly visceral, akin to touching the hardened yet living tissue of some sea-dwelled creature."
    smell = "A faint marine odor emits from the chest, reminiscent of the tang of saltwater."
    sound = "Absent of any metallic hinges, the chest opens with a muffled creaking more organic than mechanical, like the stretching of a ligament or tendon."
    taste = "A briny taste, subtly flavored by a sea-born nature, mingling with the pungent aromas of the surrounding chamber."


class EldritchKey:  # (4,2)
    desc = "This curious artifact is an amalgam of geometric complexity and alien design. Its core is a shard of metal, the likes of which defy common understanding, thrumming with an uncanny vibration that resonates at the edge of perception. Enveloping the metal is a lattice of crystalline structures that pulse with a faint, otherworldly light. Threaded through this framework are filaments that appear to channel the strange energies throbbing within."
    feel = "The key's vibrations tingle against the skin, creating a subtle electric prickle that both alarms and beckons."
    smell = "It exudes a faint ozone scent, the sharpness of a storm's aftermath trapped within its form."
    sound = "A soft hum, like the distant sound of machinery at work, emanates from the key."
    taste = "An involuntary taste of metal lingers in the mouth, as if the key alchemizes the air around it into something ancient and arcane."
