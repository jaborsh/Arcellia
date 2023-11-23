from evennia.contrib.grid.xyzgrid import xymap_legend


def assign_parents(prototypes):
    for key, prot in prototypes.items():
        if len(key) == 2:
            if prot.get("typeclass") == "world.valaria.castle.rooms.ThroneRoom":
                prot["prototype_parent"] = THRONE_ROOM
            prot["prototype_parent"] = ROOM_PARENT
        else:
            prot["prototype_parent"] = EXIT_PARENT


ROOM_PARENT = {
    "typeclass": "world.valaria.castle.rooms.CastleRoom",
}
THRONE_ROOM = {
    "typeclass": "world.valaria.castle.rooms.ThroneRoom",
}
EXIT_PARENT = {
    "typeclass": "typeclasses.exits.XYExit",
}

CASTLE_FLOOR0 = r"""
 + 0 1 2 3 4

 4   T
     u
 3 #-#   #-#
     |   |
 2   #-#-#
       |
 1     #
       |
 0     #         

 + 0 1 2 3 4 
"""


class TransitionToFloor1(xymap_legend.MapTransitionNode):
    target_map_xyz = (1, 2, "castle_floor1")


LEGEND_FLOOR0 = {"T": TransitionToFloor1}

PROTOTYPES_FLOOR0 = {
    (2, 0): {
        "key": "|233Castle Valaria - Entrance|n",
        "desc": "Grandeur incarnate rises: the castle stands majestic, its formidably thick stone walls asserting a silent strength that has withstood the test of many ages. Turrets tower toward the sky, tip-capped with conical roofs of gleaming |#b43757slate|n that catch the light, commanding the landscape with a noble elegance. Crenelations along the battlements sketch a jagged silhouette against the vista, like the spine of a slumbering dragon. Grand are the gates, forged from resolute iron and bound in timeworn oak, adorned with intricate ironwork that tells of crafts long past. Ivy clings to the weathered facade, a tender marriage of nature with the stalwart bulwark, while wildflowers dare to bloom in the crevices where wind-swept seeds have found a home.\n\n    <morning>|#FFFFFFAs the day breaks, the castle is kissed by the tender caress of morning light, gilding its high towers with a soft, golden hue.|n</morning><afternoon>|#F4A460With the afternoon sun overhead, the castle's silhouette casts a regal shadow over the lands, its presence felt far and wide across the realm.|n</afternoon><evening>|#FFD700As evening approaches, the walls shimmer with the glow of which lanterns, kindled to life by unseen hands; a beacon of warm light against the encroaching dusk.|n</evening><night>|#6495EDUnder the cloak of night, the castle is a silhouette against the tapestry of stars; moonlight drapes over it, an ethereal gown of silver threads.|n</night>",
        "senses": {
            "feel": "A gentle breeze carries the unmistakable solidity and coolness of stone mingled with the warmth of sun-caressed metalwork.",
            "smell": "The air is fragrant with the nearby gardens, blending the scent of roses with the earthy aroma of moss-clad stone.",
            "sound": "The distant echo of guards' footfalls merges with the lyrical twitter of birds perched upon the battlements.",
            "taste": "The taste of the air betrays a subtle minerality, as though one can savor the ancient stones themselves.",
        },
        "details": {
            "windows": "Each window is a testament to craftsmanship, its myriad pieces forming picturesque scenes that chronicle the history and mythology of this storied realm."
        },
    },
    (2, 1): {
        "key": "|233Castle Valaria - Grand Hall|n",
        "desc": "Within the heart of the castle lies the great hall, a space of such extraordinary proportion and splendor that it seems designed by the hand of some divine architect. Lofty ceilings arch overhead, buttressed by mighty columns that speak of an ancient strength and an elegance that defies the ages. The walls are lined with tapestries that dance softly in the sighing breath of the hall, their threads spun from the very essence of color and spectacle, depicting the realm's illustrious history. A vast fireplace dominates one end of the hall, its flames a cavorting ballet that brings warmth and light to all corners of the expanse. Long tables fashioned from the forests' finest timber stretch down the hall, their surfaces polished to a radiant sheen that beckons feasts of splendor and camaraderie.\n\n    <morning>|#FFFFFFMorning rays filter through high windows, casting luminous beams that play upon the marble floor, illuminating the hall in an ethereal glow.|n</morning><afternoon>|#F4A460In the afternoon, the hall basks in full splendor as sunlight pours in, animating the stones and wood with a golden vitality that pulses with the day's vigor.|n</afternoon><evening>|#FFD700As evening unfurls, chandeliers of wrought iron and crystal ignite, their many candles shedding a soft light that gilds every goblet and platter.|n</evening><night>|#6495EDNight cloaks the hall in a serene quietude, with the echoed chime of a lone bell signalling the end of the day as shadows merge into the safety of the hearth's embrace.|n</night>",
        "senses": {
            "feel": "The hall's grandeur envelopes one in warmth, the clink of cutlery and the rustle of rich fabrics a tactile symphony.",
            "smell": "Aromatic clusters of herbs hang from the rafters, mingling with the scent of beeswax from the candles and the smoky whisper of the fire.",
            "sound": "The air carries the harmonious blend of minstrels' melodies, soft chatter, and the resonant timbre of toasts declared boldly.",
            "taste": "The lingering taste of decadent feasts past seems to suffuse the air, teasing the palate with the promise of sumptuous flavors.",
        },
        "details": {
            "fireplace": "This monolithic hearth, carved from stone encrusted with veins of quartz, stands as a guardian of warmth, its every flicker a painter of shadows and comfort."
        },
    },
    (2, 2): {
        "key": "|233Castle Valaria - Grand Hall|n",
        "desc": "Within the heart of the castle lies the great hall, a space of such extraordinary proportion and splendor that it seems designed by the hand of some divine architect. Lofty ceilings arch overhead, buttressed by mighty columns that speak of an ancient strength and an elegance that defies the ages. The walls are lined with tapestries that dance softly in the sighing breath of the hall, their threads spun from the very essence of color and spectacle, depicting the realm's illustrious history. A vast fireplace dominates one end of the hall, its flames a cavorting ballet that brings warmth and light to all corners of the expanse. Long tables fashioned from the forests' finest timber stretch down the hall, their surfaces polished to a radiant sheen that beckons feasts of splendor and camaraderie.\n\n    <morning>|#FFFFFFMorning rays filter through high windows, casting luminous beams that play upon the marble floor, illuminating the hall in an ethereal glow.|n</morning><afternoon>|#F4A460In the afternoon, the hall basks in full splendor as sunlight pours in, animating the stones and wood with a golden vitality that pulses with the day's vigor.|n</afternoon><evening>|#FFD700As evening unfurls, chandeliers of wrought iron and crystal ignite, their many candles shedding a soft light that gilds every goblet and platter.|n</evening><night>|#6495EDNight cloaks the hall in a serene quietude, with the echoed chime of a lone bell signalling the end of the day as shadows merge into the safety of the hearth's embrace.|n</night>",
        "senses": {
            "feel": "The hall's grandeur envelopes one in warmth, the clink of cutlery and the rustle of rich fabrics a tactile symphony.",
            "smell": "Aromatic clusters of herbs hang from the rafters, mingling with the scent of beeswax from the candles and the smoky whisper of the fire.",
            "sound": "The air carries the harmonious blend of minstrels' melodies, soft chatter, and the resonant timbre of toasts declared boldly.",
            "taste": "The lingering taste of decadent feasts past seems to suffuse the air, teasing the palate with the promise of sumptuous flavors.",
        },
        "details": {
            "fireplace": "This monolithic hearth, carved from stone encrusted with veins of quartz, stands as a guardian of warmth, its every flicker a painter of shadows and comfort."
        },
    },
    (3, 2): {
        "key": "|233Castle Valaria - Lower Eastern Wing|n",
        "desc": "The lower eastern wing of the castle, a secluded quarter, whispers tales of contemplation and repose. Here, the corridors are narrower, the ceilings lower, the ambience intimate. The stone underfoot is worn smooth by the passage of countless soles, a mosaic of the castle's secret life. Along the walls, sconces hold candles that flicker and kiss the stone with wavering light. Small alcoves punctuate the passageway, each cradling a statue carved from marble or alabaster, an assembly of silent observers to the wings quietude. The air is cooler here, insulated from the bustle of the grander chambers, and windows appear intermittently, granting views of the verdant expanse beyond the walls - a pastoral interlude.\n\n    <morning>|#FFFFFFWith the morning's debut, the eastern wing awakens softly as light begins to trickle through the leaded panes, greeting the day with a hushed expectancy.|n</morning><afternoon>|#F4A460In the afternoon light, the wing's stones are touched with a tender warmth, offering solace from the day's high sun, a welcome haven.|n</afternoon><evening>|#FFD700Come evening, the corridor glows with the amber hue of candlelight, as if holding onto the last whispers of the day before it departs into memory.|n</evening><night>|#6495EDThe shroud of night endows the eastern wing with a tranquil stillness, the windows now portraits of the obsidian sky, brushed with silver by the moon's caress.|n</night>",
        "senses": {
            "feel": "There's a stillness in the air, like a carefully kept secret, accompanied by the soft touch of cool stones against one's palms.",
            "smell": "The scent is a mixture of beeswax, faint traces of incense from ceremonies of yore, and the deep, engulfing aroma of aged wood.",
            "sound": "Sounds are muted here, one's own footsteps a gentle echo that fades into the tranquil silence of the wing.",
            "taste": "The taste of the ambient air carries the faintest hint of herbs from the kitchens, mixed with the untouched freshness of old stone and timber.",
        },
        "details": {
            "statue": "Each statue, whether of sage or sylph, bears the mark of an artisan's lifelong dedication, a silent testament to the wing's serene spirit."
        },
    },
    (3, 3): {
        "key": "|233Castle Valaria - Living Quarters|n",
        "desc": "Nestled beneath the opulent layers of the castle's sprawling wings, the servant living quarters present a world apart - a realm of utility and compact comfort. The rooms, though modest in their adornment, possess a sort of dignified humility, the bare stone walls sometimes graced with simple hangings that add a touch of color to the otherwise austere palette. Wooden beams crisscross the ceilings, bearing the weight of grandeur with silent resilience. Beds are neatly arranged, each with a woolen blanket folded at the foot, providing a promise of rest after a day's toil. Trunks and small personal belongings occupy the spaces between duties and dreams, while lanterns and candles cast pools of warm light, warding off the chill of the stones.\n\n    <morning>|#FFFFFFAs dawn's early light filters in through the small windows, it dances across the simple furnishings, casting long, hopeful shadows that signify a new day's beginning.|n</morning><afternoon>|#F4A460The afternoon's sun reaches sparingly into the living quarters, offering a brief daily gift of natural warmth to those who serve with steadfast dedication.|n</afternoon><evening>|#FFD700Evening brightens the modest spaces briefly with the soft glow of twilight, before lamps are lit, signifying the change from work to well-earned repose.|n</evening><night>|#6495EDThe deep calm of night settles over the living quarters, a time for whispers of home and tales of the day before slumber takes hold beneath the castle's protective embrace.|n</night>",
        "senses": {
            "feel": "The quarters are filled with the familiar texture of rough-spun fabric and the solid presence of practical furniture.",
            "smell": "The air bears the clean scent of laundered linens mixed with the subtle, comforting aroma of woodsmoke from the hearth.",
            "sound": "Muffled laughter and murmured conversations drift through the air, soundtracks to camaraderie and shared lives of service.",
            "taste": "There exists a persistent, homely taste of freshly baked bread from the kitchens, permeating even the quietest corners.",
        },
        "details": {
            "beds": "Each bed is a simple frame of sturdy wood, topped with a straw mattress that offers a humble but welcome respite to those who have spent their day in the castle's service."
        },
    },
    (4, 3): {
        "key": "|233Castle Valaria - Armory|n",
        "desc": "The castle's armory is a vault-like chamber of solemn grandeur, a shrine to the martial spirit that guards the realm. Its walls, lined with racks and stands, hold a gleaming array of weaponry and armament, each piece polished to a fearsome perfection. Swords with hilts wrought in intricate patterns rest beside shields emblazoned with the symbols of the monarchy, whilst suits of armour stand sentinel in their silent ranks, hollow knights awaiting the call to service. At the centre of the room, a grand table of dark oak serves for the examination and repair of weaponry, tools of the armorer's trade meticulously arranged upon its surface. Torches ensconced in iron brackets thrust their fiery tongues into the air, casting an orange glow onto the metalwork, making the steel shimmer with latent potential.\n\n    <morning>|#FFFFFFMorning light fights a valiant battle to pierce the small, high-set windows, touching only the tips of the armory's contents with a glimmer of daybreak.|n</morning><afternoon>|#F4A460As the afternoon reigns, the armory remains shrouded in a constant chiaroscuro of light and shadow, the flicker of torchlight enhancing the dramatic atmosphere.|n</afternoon><evening>|#FFD700The evening sees the armory become a theater of orange light, each helm and breastplate casting mysterious shadows across the stone floor.|n</evening><night>|#6495EDWith night's descent, the armory turns into a cavern of echoes and whispers, the metalwork bathed in a spectral glow from the torches that ward off the darkness.|n</night>",
        "senses": {
            "feel": "The air is heavy with the weight of metals and the oily tang of well-maintained gear.",
            "smell": "Scents of iron, leather, and the sharp tang of whetstones merge into a pungent reminder of battle readiness.",
            "sound": "There is a near-silent reverence here, broken only by the occasional rasp of a blade being sharpened or the soft clink of chain mail being sorted.",
            "taste": "The mouth detects the faint metallic taste that lingers in the air, as if the very essence of the steel has infused the atmosphere.",
        },
        "details": {
            "sword": "One particular sword, with a handle wrapped in dragon-skin and a blade as cold as the night, commands respect as a masterpiece of craftsmanship and deadly beauty."
        },
    },
    (1, 2): {
        "key": "|233Castle Valaria - Lower Western Wing|n",
        "desc": "The lower western wing of the castle exudes the antiquity of its foundations - a space wrapped in the soft, continuous hum of industrious undertakings. Here, the stones of the hallway are more uneven, trod by the many servants making their silent circuits. The air is slightly warmer, owing to this wing's proximity to the kitchens, and the unmistakable rhythmic thud of pestle in mortar resonates softly through the walls. This wing is home to various workrooms: candle-lit chambers filled with looms, spinning wheels, and the subdued chatter of artisans at their craft. Great barrels and chests line portions of the corridor, brimming with goods and awaiting distribution. These intimate, low-ceilinged spaces are punctuated by the occasional window, through which one can glimpse the warming glow of sunset imbuing the air with an amber tranquility.\n\n    <morning>|#FFFFFFIn the morning's early hours, the western wing stirs to life as faint rays of light bestow a modest blessing on the day's first labors.|n</morning><afternoon>|#F4A460Bathed in the afternoon glow, the wing resonates with industry, the muffled sounds of productivity filling the air as daylight supports the hands at work.|n</afternoon><evening>|#FFD700Towards evening, the glow of workroom fires reflects upon the stones, casting a homely golden light as the day's endeavors wind down.|n</evening><night>|#6495EDNight finds the western wing quiet, save for the dedicated few who work by lantern light, their silhouettes a dance of dedication against the walls.|n</night>",
        "senses": {
            "feel": "The stone underfoot conveys a coolness that contrasts with the warmth rising from the bustling activities within.",
            "smell": "An olfactory tapestry of beeswax, fresh textiles, and simmering stews from nearby quarters intertwine in the air.",
            "sound": "Softly, the drone of diligent work fills the hall, a harmonious marriage of clattering, scraping, and steadfast breaths.",
            "taste": "The taste in the air carries a homely richness, seasoned with the sweat of hard work and the ambient flavors from the kitchens.",
        },
        "details": {
            "loom": "A particularly ornate loom occupies one chamber, its intricate mechanisms a symphony of threads, the shuttle darting in a dance as old as time."
        },
    },
    (1, 3): {
        "key": "|233Castle Valaria - Dining Room|n",
        "desc": "An exquisite space for repast and revelry, where opulence and appetite convene in splendid ceremony. An impressive long table of polished mahogany dominates the center of the room, the wood glowing with a deep, lustrous patina that reflects the history of feasts enjoyed upon its surface. Tall, arched windows draped in luxurious velvet look out upon the castle grounds, their panes capturing the shifting light of the outside world. Above, a grand chandelier hangs like a constellation wrought by mortal hands, its countless crystals shimmering with captured light. The walls bear portraits of regal ancestries, a silent gallery of eyes that have watched over centuries of stately banquets. Heavy damask tablecloths and fine porcelain create a tableau of elegance waiting to be animated by the clinking of glassware and the melody of convivial conversation.\n\n    <morning>|#FFFFFFMorning's touch shyly enters through the windows, flirting with crystal and cutlery, casting tentative shadows upon the silver and the china.|n</morning><afternoon>|#F4A460The room is drenched in afternoon splendor, each sunbeam playing joyfully upon the varnished surfaces, embodying the day's spirited heart.|n</afternoon><evening>|#FFD700As the day succumbs to evening, lanterns and sconces blossom with flame, lending the room an intimate, golden peace that anticipates the night's feast.|n</evening><night>|#6495EDIn the cloak of night, the dining room becomes an island of warmth and luminescence, the chatter and laughter within ensuring that no shadow may linger too long.|n</night>",
        "senses": {
            "feel": "The rich texture of the room encompasses one, from the weight of the embroidered tablecloths to the smooth coolness of silverware in hand.",
            "smell": "The mingled aromas of savory dishes being prepared in the wings converge with the subtle fragrance of beeswax candles burning steadily.",
            "sound": "Sounds carry the anticipatory notes of silver bells announcing courses, accompanied by the harmonious symphony of high spirits.",
            "taste": "The air seems charged with the essence of culinary masterpieces yet to be unveiled, tantalizing one's palate before a bite is ever taken.",
        },
        "details": {
            "chandelier": "This majestic chandelier, a crowning glory of craftsmanship, holds scores of candles that shed a radiant light, flickering like stars in a room bound heavens."
        },
    },
    (0, 3): {
        "key": "|233Castle Valaria - Kitchen|n",
        "desc": "A veritable crucible of culinary achievement bubbles and churns with an orchestrated frenzy, as cooks and servants dart amidst the steam and sizzle. Great ovens, their mouths agape with roaring fire, expel the rich scents of roasting meats and fresh bread. Stone counters are awash with a colorful array of produce from the castle's own grounds - roots, herbs, and fruits, an edible mosaic greeted by keen blades and skilled hands. Huge cauldrons hang over open flames, their contents simmering with promise, while kitchen boys turn spits, their faces aglow with heat and exertion. Pots and pans of copper and iron, polished and dented with honorable service, clang in a percussive accompaniment to the ballet of gastronomy that unfolds in this bustling heart of the castle.\n\n    <morning>|#FFFFFFIn the morning, the kitchen is rife with the breaking of bread and the crackle of bacon in pans, as shafts of light cut through rising mists of promise.|n</morning><afternoon>|#F4A460By afternoon, the space is awash in golden daylight and warmth, the sounds of preparation crescendoing toward the evening's grand repast.|n</afternoon><evening>|#FFD700As evening encroaches, torches and hearth-fires illuminate earnest faces, reflecting off gleaming utensils and glinting in the eyes of the guardians of sustenance.|n</evening><night>|#6495EDWhen night descends, the kitchen's embers glow softly in the dark, a bastion of simmering pots and the occasional late-night sweetmeat being crafted in quietude.|n</night>",
        "senses": {
            "feel": "The overwhelming heat emanates from every surface, tempered by the occasional brush of cool air when the pantry door swings open.",
            "smell": "A riotous blend of aromas fills the air: spices and meats, sweet confections and aromatic broths, creating an intoxicating bouquet of nourishment.",
            "sound": "Clattering dishes, the staccato tap of chopping knives, and the commanding shouts of the head cook form the ceaseless, lively score of the kitchen.",
            "taste": "The taste of the air is rich with a thousand unfolding delights, a prelude to the feasts crafted within these busy walls.",
        },
        "details": {
            "cauldron": "Amidst the culinary chaos, a grand cauldron bubbles with the heady stock for the evening's soup, its iron sides seasoned from decades of service."
        },
    },
    ("*", "*"): {},
    ("*", "*", "*"): {},
}

assign_parents(PROTOTYPES_FLOOR0)

XYMAP_DATA_FLOOR0 = {
    "zcoord": "castle_floor0",
    "map": CASTLE_FLOOR0,
    "legend": LEGEND_FLOOR0,
    "prototypes": PROTOTYPES_FLOOR0,
}

CASTLE_FLOOR1 = r"""    
                 
 + 0 1 2 3 4 5 6 

 3   T   #     
     d   |     
 2 #-#---#---#-#
     |   |   |
 1   # #-#-# #
             |
 0           #

 + 0 1 2 3 4 5 6 
                 
"""


class TransitionToFloor0(xymap_legend.MapTransitionNode):
    target_map_xyz = (1, 3, "castle_floor0")


LEGEND_FLOOR1 = {"T": TransitionToFloor0}

PROTOTYPES_FLOOR1 = {
    (3, 2): {
        "key": "|233Castle Valaria - Roundtable Lobby|n",
        "desc": "A circular chamber at the heart of the castle ensconces a renowned roundtable, a spectacle of such exquisite craftsmanship that it has been hailed as one of the most beautiful sights beheld by humankind. This is a sanctum of symmetry and unity, where arched doorways echo the table's curve, leading the eyes perpetually inward. The table itself is a masterpiece of inlaid woods - oak, ash, and cherry forming intricate patterns and designs that evoke the realm's lore and landscape. Carvings along its edge tell tales of unity and peace, while the surface reflects the ambient light in a soft sheen that could rival the glint of sunlight on calm waters. Above, a dome of stained glass casts prismatic hues upon the occupants, garments and goblets alike awash with celestial color.\n\n    Around the perimeter of the room stand statues of legendary figures, each carved from white marble with such lifelike detail that they seem poised to step down from their plinths and join the council. One statue, depicting a philosopher of ancient times, is particularly revered - a figure of wisdom, with eyes that seem to shimmer with an inner light and a presence that commands silent respect.\n\n    <morning>|#FFFFFFWith the morning's advent, delicate rays illuminate the roundtable, blessing its surface with the purity and promise of daybreak.|n</morning><afternoon>|#F4A460Come afternoon, the room is resplendent, the table awash in a gilded glory that befits its legendary status amongst the wonders of the world.|n</afternoon><evening>|#FFD700As evening descends, the chandeliers above are kindled, their soft light embracing the table and statues alike in a radiant, golden embrace.|n</evening><night>|#6495EDNight softens the lobby, the table a beacon of tranquility under the watchful gaze of the marble council, bathed in the gentle luminescence of the moon.|n</night>",
        "senses": {
            "feel": "The air here is suffused with a sense of momentous occasions, the touch of polished stone and timber resonant with history.",
            "smell": "A subtle fragrance of beeswax polish mingles with the distant incense from the chapel, enhancing the sanctity of the chamber.",
            "sound": "The chamber carries the gentle, almost hallowed echoes of footsteps and hushed conversation, as if the very room itself is listening.",
            "taste": "In the air lingers a certain freshness, untainted and pure, as though it tastes of the enduring legacy embodied by the roundtable.",
        },
        "details": {
            "roundtable": "The roundtable, with its array of natural hues and the sheen of its polished grains, seems a microcosm of the world it serves, an unbroken continuum of beauty and diplomacy.",
            "statue": "The philosopher's statue exudes an aura of contemplation, with robes falling in marble folds so fine they appear to ripple with an unseen breeze.",
            "table": "The roundtable, with its array of natural hues and the sheen of its polished grains, seems a microcosm of the world it serves, an unbroken continuum of beauty and diplomacy.",
        },
    },
    (5, 2): {
        "key": "|233Castle Valaria - Upper Eastern Wing|n",
        "desc": "Each doorway is a portal to solace or scholarship, the halls adorned with delicate friezes that recount the quieter tales of the realm's lore. Windows here are more abundant, affording breathtaking vistas of the rising sun which bathes the wing in a gentle radiance. The wood of the floors, polished by countless thoughtful paces, shimmers with the depth of dark honey, while plush rugs mute the footfalls of those who seek the quietude of this lofty retreat. Occasionally, one may hear the rustle of parchment or the whisper of fabric against stone, the only evidence of the scholars and nobles who contemplate within these hallowed confines.\n\n    <morning>|#FFFFFFIn the clarity of morning, these heights revel in the embrace of early light, the sun's caress chasing away the last vestiges of twilight.|n</morning><afternoon>|#F4A460By afternoon, the light here is brilliant and clear, granting the austere beauty of the wing a radiance as if it, too, has absorbed the sun's wisdom.|n</afternoon><evening>|#FFD700As the evening approaches, the shadows grow long and soft, an invitation to reflection among those who dwell amidst the wing's quiet grandeur.|n</evening><night>|#6495EDThe hush of night is profound in the upper east wing, the silence broken only by the occasional turning of a page or the soft closing of a shutters.|n</night>",
        "senses": {
            "feel": "The air holds a scholarly chill, tempered by the warmth of hearths crackling in secluded corners.",
            "smell": "Wafts of ink and old tomes mix with the fresh breeze that meanders through the windows, a scent of knowledge and the world beyond.",
            "sound": "The sound of solitude is a constant companion, punctuated by the rare, discreet murmur of voices discussing matters of state or philosophy.",
            "taste": "There's a rarefied taste in the air, one of dust motes and the tang of ancient wood - a flavor as old as the secrets the wing keeps.",
        },
        "details": {
            "window": "A particular window framed in latticed ironwork offers a commanding view of the dawning sky, the glass tinged with the faintest color of optimism."
        },
    },
    (6, 2): {
        "key": "|233Castle Valaria - Eastern Study|n",
        "desc": "Nestled within the castle's upper east wing, the eastern study is a bastion of thought and repose. Rich mahogany bookshelves, arranged in labyrinthine rows, rise towards the beamed ceiling, each tome a sentinel guarding the wisdom of the ages. A large oriel window projects outward, encased in a filigree of stone, offering a panoramic prospect of the undulating landscape beyond. Intricate tapestries and soft paintings adorn the remaining walls, a testament to the pursuit of beauty as well as intellect. The room is anchored by a grand desk of polished burl wood, its surface an ocean of possibility amid the sea of learning that surrounds it. Carefully placed lamps cast circles of amber light, creating islands of warmth where scholars might ponder and scribes pen their meticulous script.\n\n    <morning>|#FFFFFFMorning light floods the study with a tranquil clarity, each ray enlivening the dust motes into a delicate dance above the well-worn pages.|n</morning><afternoon>|#F4A460In the afternoon, the sun graces the study with a serene brilliance, highlighting the gilded spines of books and the deep patina of the desk.|n</afternoon><evening>|#FFD700As dusk commences its descent, the study takes on a hushed glow, lamps awakened to hold back the encroaching twilight that presses against the pane.|n</evening><night>|#6495EDNighttime envelops the study in a velvety quiet, only the flickering of lamp flames breaching the studious solitude that blankets the room.|n</night>",
        "senses": {
            "feel": "The study envelops its visitors in an atmosphere of concentrated endeavor, the weight of knowledge as palpable as the leather-bound books in one's grasp.",
            "smell": "Odors of polished wood, leather, and venerable paper intertwine, an olfactory library as complex as the texts it arises from.",
            "sound": "Silence reigns supreme, respectfully punctuated by the soft turning of pages and the occasional scratch of quill on parchment.",
            "taste": "The air imparts an almost tangible taste of ink and aged paper, with a whisper of the outside air's freshness when the window is ajar.",
        },
        "details": {
            "desk": "The desk stands as the study's centerpiece, its surface scarred by years of scholarly labor, yet rich with the sheen of care and the promise of discovery.",
            "bookshelf": "On the bookshelf rests a singular atlas, its maps drawn with such precision and artistry that they sing an ode to the cartographer's craft and the explorer's spirit.",
        },
    },
    (5, 0): {
        "key": "|233Castle Valaria - Storage Closet|n",
        "desc": "In the shadowed recesses of the castle's lower corridors, there lies a storage closet oft overlooked and seldom remembered. It is a small, forlorn alcove, where dust reigns like a melancholy monarch over a kingdom of discarded objects. The air is dank, heavy with the scent of mildew and the mustiness of neglect. Shelves, once neatly ordered, now sag under the weight of old linens and tarnished serving ware that have lost their luster and purpose. Forgotten toys share space with cracked leather boots and outdated finery, each item bearing the patina of disuse. Cobwebs festoon the corners, their gossamer strands testament to the undisturbed quiet that pervades this narrow chamber, a repository of items that time - and their owners - seem to have unceremoniously left behind.\n\n    <morning>|#FFFFFFMorning light scarcely dares to touch this place, the faint beam that does enter through a crevice too weak to contest the gloom.|n</morning><afternoon>|#F4A460The afternoon offers no respite from the perennial twilight within, the closet remaining indifferent to the passage of sun across the sky.|n</afternoon><evening>|#FFD700Even as evening descends, its soft glow fails to penetrate the seam of the door, leaving the storage space in its perpetual dusk.|n</evening><night>|#6495EDAt night, the closet shares in the castle's slumber, a sleep unvisited by dreams or the silver reassurances of the moon's light.|n</night>",
        "senses": {
            "feel": "The air is tinged with the lingering sadness of disuse, each breath a reminder of the vibrant past now reduced to silence and shadow.",
            "smell": "Musty and forgotten, the scents of old wood and fabric meld together, painting an aroma of abandonment.",
            "sound": "The silence here is complete, save for the occasional skitter of a mouse or the distant drip of water, each sound an echo in a hollow space.",
            "taste": "A faint taste of dust and decay lingers on the tongue, the flavor of an absence unfilled and a history unattended.",
        },
        "details": {
            "linen": "A stack of linens, frayed and faded, lies untouched, their fibers interwoven with the quiet desolation of the closet."
        },
    },
    (5, 1): {
        "key": "|233Castle Valaria - Small Library|n",
        "desc": "Tucked away in the quieter echelons of the castle, a small library stands as a humble sanctuary of literature and solitude. This chamber, though modest in size, holds an aura of dense erudition; rows of well-stocked shelves burdened with a collection that spans the width and depth of realms both real and imagined. The hushed tones of russet and mahogany that grace the bookcases lend the space a sense of warmth and refuge. A solitary window permits rays of light to spill upon reading nooks that seem to wait with patient stillness for a curious soul to claim their embrace. Diminished echoes of the castle's life beyond these walls serve as the softest soundtrack to the quiet rustling of pages and the occasional creak of wood as readers shift their weight into the embrace of knowledge found within these tomes.\n\n    <morning>|#FFFFFFMorning's optimism gently fills the library, casting light upon verses and prose, inviting the day's first seeker of wisdom.|n</morning><afternoon>|#F4A460The sun at its zenith sends a battalion of light through the window, traversing the room like a spotlight on certain chosen volumes.|n</afternoon><evening>|#FFD700Candles are lit in the evening, their tender glow a halo around each reader's head, anointing them with the sanctity of the written word.|n</evening><night>|#6495EDWhen the outside world dons its nocturnal veil, the library becomes a vessel of timelessness, cocooned in the soft, golden light of lamps nurturing night owls in their literary vigils.|n</night>",
        "senses": {
            "feel": "The weight of accumulated knowledge permeates the air, settling on the skin like a fine, intellectual mist.",
            "smell": "Scents of leather-bound tomes and the dry mustiness of paper aged like fine wine envelop the room in an intoxicating embrace.",
            "sound": "One can hear the whispers of history and fantasy alike in the light flutter of pages turned by gentle fingertips.",
            "taste": "The taste of the library is one of ink and time, a flavor that encourages the palette of the mind to hunger for more.",
        },
        "details": {
            "bookcase": "A particular bookcase, marginally more ornate than its brethren, harbors first editions and rare manuscripts, their spines a catalog of the library's quiet pride.",
            "reading nook": "One nook cradles a wingback chair upholstered in emerald velvet, an invitation to settle within its folds and away from the world's cares.",
        },
    },
    (1, 2): {
        "key": "|233Castle Valaria - Upper Western Wing|n",
        "desc": "The upper western wing of the castle is a tableau of elegance and reprieve, wealthily adorned yet whispering of tranquility. Here, the walls are hung with sumptuous tapestries that capture the aura of sunset even when the sun has journeyed away, their threads a rich narrative of the lands' splendors. The flooring, an arrangement of polished parquet, reflects the soft luminescence of sconces that grace the walls at regular intervals. Doors inlaid with marquetry depicting the flora and fauna of the realm hint at the prestige and comfort of the private chambers and salons they guard. The air here harbors a stillness, as if it resides just a measure removed from the time's steady march, welcoming those who seek the quiet dignity of seclusion and reflection amidst the upper echelons of nobility.\n\n    <morning>|#FFFFFFThe first gentle stirrings of morning coax shafts of light to play upon the inlaid doors, offering a silent benediction to the day's infancy.|n</morning><afternoon>|#F4A460Come afternoon, the golden wash of the sun's high journey bathes the wing in a light that rivals the luxury of its own adornments.|n</afternoon><evening>|#FFD700Twilight graces the western wing with a serene beauty, the sky's painted colors seeping through windows as though to share in the wing's repose.|n</evening><night>|#6495EDIn the time of night, the glow of sconces softens the grandeur to a comforting murmur of light, cradling the wing's inhabitants in peaceful splendor.|n</night>",
        "senses": {
            "feel": "The temperature is kept pleasantly moderate, the air touched with a gentle draft that carries echoes of the day's warmth or the evening's cool.",
            "smell": "A delicate fragrance of lavender and polished wood provides an understated olfactory backdrop to the wing's opulent quietude.",
            "sound": "The wing's auditory tapestry is woven from soft murmurs of conversation, the faint rustle of silk, and the remote strains of a lute played in a distant corner.",
            "taste": "One might almost taste the subtle richness of the wing, a flavor not of food but of the very essence of crafted luxury and storied legacy.",
        },
        "details": {
            "inlaid door": "An exquisite door features a pastoral scene so delicately inlaid that one feels they could step through it and into the meadows it portrays.",
            "tapestry": "A particular tapestry depicts the legendary twilight descent of celestial beings, their forms woven with threads of silver and blue, shimmering softly in the wing's ambient light.",
        },
    },
    (1, 1): {
        "key": "|233Castle Valaria - Upper Western Wing|n",
        "desc": "The upper western wing of the castle is a tableau of elegance and reprieve, wealthily adorned yet whispering of tranquility. Here, the walls are hung with sumptuous tapestries that capture the aura of sunset even when the sun has journeyed away, their threads a rich narrative of the lands' splendors. The flooring, an arrangement of polished parquet, reflects the soft luminescence of sconces that grace the walls at regular intervals. Doors inlaid with marquetry depicting the flora and fauna of the realm hint at the prestige and comfort of the private chambers and salons they guard. The air here harbors a stillness, as if it resides just a measure removed from the time's steady march, welcoming those who seek the quiet dignity of seclusion and reflection amidst the upper echelons of nobility.\n\n    <morning>|#FFFFFFThe first gentle stirrings of morning coax shafts of light to play upon the inlaid doors, offering a silent benediction to the day's infancy.|n</morning><afternoon>|#F4A460Come afternoon, the golden wash of the sun's high journey bathes the wing in a light that rivals the luxury of its own adornments.|n</afternoon><evening>|#FFD700Twilight graces the western wing with a serene beauty, the sky's painted colors seeping through windows as though to share in the wing's repose.|n</evening><night>|#6495EDIn the time of night, the glow of sconces softens the grandeur to a comforting murmur of light, cradling the wing's inhabitants in peaceful splendor.|n</night>",
        "senses": {
            "feel": "The temperature is kept pleasantly moderate, the air touched with a gentle draft that carries echoes of the day's warmth or the evening's cool.",
            "smell": "A delicate fragrance of lavender and polished wood provides an understated olfactory backdrop to the wing's opulent quietude.",
            "sound": "The wing's auditory tapestry is woven from soft murmurs of conversation, the faint rustle of silk, and the remote strains of a lute played in a distant corner.",
            "taste": "One might almost taste the subtle richness of the wing, a flavor not of food but of the very essence of crafted luxury and storied legacy.",
        },
        "details": {
            "inlaid door": "An exquisite door features a pastoral scene so delicately inlaid that one feels they could step through it and into the meadows it portrays.",
            "tapestry": "A particular tapestry depicts the legendary twilight descent of celestial beings, their forms woven with threads of silver and blue, shimmering softly in the wing's ambient light.",
        },
    },
    (0, 2): {
        "key": "|233Castle Valaria - Royal Bedchamber|n",
        "desc": "As if hewn from dreams and draped in the velvet cloak of night, the royal bedchamber stands as the silent keeper of rest and respite for the sovereigns. Canopy bed, grand and foreboding, is festooned with rich drapes that pool onto the floor in opulent abandon, while plush down pillows whisper promises of comfort. Walls softened by the glow of candlelight are adorned with ancestral portraits and intricate tapestries that chart the lineage's triumphs. Beside the great hearth, a pair of regal armchairs invites quiet reflection, their upholstery matching the deep, royal hues of the chamber's palette. Above, the ceiling is a frescoed masterpiece, offering celestial views that inspire the minds of those who slumber below. The very air in the chamber seems thick with the weight of history, each gilded cornice and carved balustrade contributing to the sanctity of this innermost sanctum.\n\n    <morning>|#FFFFFFThe chamber greets the morning with a subtlety befitting its station, the weak light filtered through heavy curtains hinting at the day's genesis outside its walls.|n</morning><afternoon>|#F4A460In the full bloom of afternoon, stray beams of light catch on the edges of gold leaf and the facets of crystal, a quiet acknowledgment of the sun's high reign.|n</afternoon><evening>|#FFD700When evening encroaches, the chamber succumbs to a golden serenity, the soft glow of firelight casting dancing shadows across plush fabrics and polished wood.|n</evening><night>|#6495EDThe night bestows upon the bedchamber a crown of silence, with just the moon paying homage through the rare sliver of an uncurtained window.|n</night>",
        "senses": {
            "feel": "An enveloping warmth pervades the room, a gentle touch that soothes the soul and promises repose.",
            "smell": "The chamber exudes an aroma of fragrant wood and subtle floral notes, a scented testament to its regal occupants.",
            "sound": "Silence here is layered, wrapping its inhabitants in a blanket of peace, broken only by the occasional crackle from the fireplace.",
            "taste": "The air carries a faint hint of honey and spices, vestiges of royal feasts that seem to seep through the very walls.",
        },
        "details": {
            "bed": "The bed, an anchor of magnificence within the chamber, boasts posts of carved mahogany that soar towards the canopy, a testament to royalty's embrace.",
            "ceiling": "Upon the ceiling unfolds a fresco where gods and mortals alike traverse azure skies, a nightly panorama for the eyes of those who lie in contemplation below.",
        },
    },
    (2, 1): {
        "key": "|233Castle Valaria - Balcony|n",
        "desc": "Perched high above the bustling grandeur of the great hall, an ornate balcony presents itself as a silent observer to the tapestry of life beneath. Its stone balustrade, intricate as lace, is weathered by the soft caresses of countless celebrations held below. Marble underfoot reflects the myriad of lights, from the flickering candles to the grand chandeliers of the space it surveys. Here, courtiers may withdraw to whisper secrets or gaze down upon the revelry with a detached amusement, their laughter mingling with the echoes of mirth from the festivities. Slender columns rise to support a latticed canopy, providing shelter and a frame for the vastness of the sky above, which plays its own celestial dramas for those privileged enough to pause and look upward from the merriment.\n\n    <morning>|#FFFFFFIn the tender light of morning, the balcony observes the hushed preparations below, the gentle hum of the day's awakening a soft hymn to new beginnings.|n</morning><afternoon>|#F4A460Under the afternoon sky, the balcony stands bathed in splendor, its shadow a slow-moving dial across the mosaic of activities unfurling in the great hall.|n</afternoon><evening>|#FFD700With evening's progression, the lanterns of the hall are reflected upon the marble, as though the balcony were privy to the stars alighting upon the earth.|n</evening><night>|#6495EDWhen night descends, the balcony becomes a nebulous boundary between the raucous joy of the hall and the silent majesty of the infinite heavens above.|n</night>",
        "senses": {
            "feel": "The coolness of the stone beneath one's hands contrasts with the warmth rising from the celebrations below, a blend of excitement and aloofness.",
            "smell": "A wafting breeze carries the intermingled fragrances of feasting and perfumes from the great hall, offering an aerial bouquet to those above.",
            "sound": "Laughter and music drift upward in a harmonious tide, the sounds of jubilance rising to fill every nook of the lofty perch.",
            "taste": "The essence of mirth seems almost tangible in the air, a subtle flavor that teases the senses with hints of the opulence below.",
        },
        "details": {
            "balustrade": "The balustrade, with its delicate traceries, casts an ever-changing pattern of shadows upon the balcony floor - an eternal dance of stone and light.",
            "canopy": "The latticed canopy, curling with the grace of ivy and the potency of old vines, shelters from the elements while framing a patchwork view of the open sky.",
        },
    },
    (3, 1): {
        "key": "|233Castle Valaria - Balcony|n",
        "desc": "Perched high above the bustling grandeur of the great hall, an ornate balcony presents itself as a silent observer to the tapestry of life beneath. Its stone balustrade, intricate as lace, is weathered by the soft caresses of countless celebrations held below. Marble underfoot reflects the myriad of lights, from the flickering candles to the grand chandeliers of the space it surveys. Here, courtiers may withdraw to whisper secrets or gaze down upon the revelry with a detached amusement, their laughter mingling with the echoes of mirth from the festivities. Slender columns rise to support a latticed canopy, providing shelter and a frame for the vastness of the sky above, which plays its own celestial dramas for those privileged enough to pause and look upward from the merriment.\n\n    <morning>|#FFFFFFIn the tender light of morning, the balcony observes the hushed preparations below, the gentle hum of the day's awakening a soft hymn to new beginnings.|n</morning><afternoon>|#F4A460Under the afternoon sky, the balcony stands bathed in splendor, its shadow a slow-moving dial across the mosaic of activities unfurling in the great hall.|n</afternoon><evening>|#FFD700With evening's progression, the lanterns of the hall are reflected upon the marble, as though the balcony were privy to the stars alighting upon the earth.|n</evening><night>|#6495EDWhen night descends, the balcony becomes a nebulous boundary between the raucous joy of the hall and the silent majesty of the infinite heavens above.|n</night>",
        "senses": {
            "feel": "The coolness of the stone beneath one's hands contrasts with the warmth rising from the celebrations below, a blend of excitement and aloofness.",
            "smell": "A wafting breeze carries the intermingled fragrances of feasting and perfumes from the great hall, offering an aerial bouquet to those above.",
            "sound": "Laughter and music drift upward in a harmonious tide, the sounds of jubilance rising to fill every nook of the lofty perch.",
            "taste": "The essence of mirth seems almost tangible in the air, a subtle flavor that teases the senses with hints of the opulence below.",
        },
        "details": {
            "balustrade": "The balustrade, with its delicate traceries, casts an ever-changing pattern of shadows upon the balcony floor - an eternal dance of stone and light.",
            "canopy": "The latticed canopy, curling with the grace of ivy and the potency of old vines, shelters from the elements while framing a patchwork view of the open sky.",
        },
    },
    (4, 1): {
        "key": "|233Castle Valaria - Balcony|n",
        "desc": "Perched high above the bustling grandeur of the great hall, an ornate balcony presents itself as a silent observer to the tapestry of life beneath. Its stone balustrade, intricate as lace, is weathered by the soft caresses of countless celebrations held below. Marble underfoot reflects the myriad of lights, from the flickering candles to the grand chandeliers of the space it surveys. Here, courtiers may withdraw to whisper secrets or gaze down upon the revelry with a detached amusement, their laughter mingling with the echoes of mirth from the festivities. Slender columns rise to support a latticed canopy, providing shelter and a frame for the vastness of the sky above, which plays its own celestial dramas for those privileged enough to pause and look upward from the merriment.\n\n    <morning>|#FFFFFFIn the tender light of morning, the balcony observes the hushed preparations below, the gentle hum of the day's awakening a soft hymn to new beginnings.|n</morning><afternoon>|#F4A460Under the afternoon sky, the balcony stands bathed in splendor, its shadow a slow-moving dial across the mosaic of activities unfurling in the great hall.|n</afternoon><evening>|#FFD700With evening's progression, the lanterns of the hall are reflected upon the marble, as though the balcony were privy to the stars alighting upon the earth.|n</evening><night>|#6495EDWhen night descends, the balcony becomes a nebulous boundary between the raucous joy of the hall and the silent majesty of the infinite heavens above.|n</night>",
        "senses": {
            "feel": "The coolness of the stone beneath one's hands contrasts with the warmth rising from the celebrations below, a blend of excitement and aloofness.",
            "smell": "A wafting breeze carries the intermingled fragrances of feasting and perfumes from the great hall, offering an aerial bouquet to those above.",
            "sound": "Laughter and music drift upward in a harmonious tide, the sounds of jubilance rising to fill every nook of the lofty perch.",
            "taste": "The essence of mirth seems almost tangible in the air, a subtle flavor that teases the senses with hints of the opulence below.",
        },
        "details": {
            "balustrade": "The balustrade, with its delicate traceries, casts an ever-changing pattern of shadows upon the balcony floor - an eternal dance of stone and light.",
            "canopy": "The latticed canopy, curling with the grace of ivy and the potency of old vines, shelters from the elements while framing a patchwork view of the open sky.",
        },
    },
    (3, 3): {
        "key": "|233Castle Valaria - Audience Chamber|n",
        "desc": "Within lofty bounds of the kingdom's seat of power, a throne room stands, grand and voluminous, its very air pregnant with expectancy and grandeur. Enormous arches carved from the heart of the mountains support a ceiling as distant as the heavens, upon which the stories of the realm are painted with a celestial hand. Marble, cool and endless, unfurls beneath the feet, leading subjects and suitors forward to the heart of sovereignty - a throne as much a symbol as a seat, wrought of gold and gemstone, cradled by a soaring canopy that proclaims its significance. Vibrant banners hang from the walls, their colors proud and bold in the stillness. Here, the echo of footfall or whisper is magnified, as if even the stones recognize the gravity of this space, where rulers hold court and destinies are shaped.\n\n    <morning>|#FFFFFFThe burgeoning light of daybreak steals into the throne room, brushing over gold and stone with a tender regard for the solemnity within its grasp.|n</morning><afternoon>|#F4A460At the peak of day, sunlight floods the chamber with an aura of invincibility, as if the very rays bow in deference to the throne that commands the room.|n</afternoon><evening>|#FFD700Evening light filters through stained glass, cascading across the marble floor in subdued opalescence, heralding the transition from day to dusk.|n</evening><night>|#6495EDWhen night descends, the room slumbers in dim, reverential illumination, the eternal flames of wall sconces standing sentry over the chamber's sanctity.|n</night>",
        "senses": {
            "feel": "The vast space induces a reverent awe, its coolness and echoes a cloak that settles over the shoulders of all who enter.",
            "smell": "The faint scent of polished stone mixes with the lingering traces of perfumed oils from the garments of royalty and nobility.",
            "sound": "There's a sonorous quality to the silence that inhabits the room, punctuated sporadically by the clear ring of a herald's announcement or the rustle of silken robes.",
            "taste": "The taste here is almost regal, tinged with the stone's mineral kiss and the fleeting spice of incense used in ceremonies of significance.",
        },
        "details": {
            "throne": "The throne itself, a formidable masterpiece, rises with an elegance that commands respect, its surface a saga of triumph, cast in precious materials that catch the light in homage.",
            "ceiling fresco": "Above, the vast fresco sprawls across the ceiling, a silent witness to the room's grandeur, its mythic figures captured mid-gesture in scenes of divine and mortal entwine.",
        },
        "typeclass": "world.valaria.castle.rooms.ThroneRoom",
    },
    ("*", "*"): {},
    ("*", "*", "*"): {},
}

assign_parents(PROTOTYPES_FLOOR1)

XYMAP_DATA_FLOOR1 = {
    "zcoord": "castle_floor1",
    "map": CASTLE_FLOOR1,
    "legend": LEGEND_FLOOR1,
    "prototypes": PROTOTYPES_FLOOR1,
}

XYMAP_DATA_LIST = [XYMAP_DATA_FLOOR0, XYMAP_DATA_FLOOR1]

# Names = |233
