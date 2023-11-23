from evennia.contrib.grid.xyzgrid import xymap_legend


def assign_parents(prototypes):
    for key, prot in prototypes.items():
        if len(key) == 2:
            # we don't want to give exits the room typeclass!
            prot["prototype_parent"] = ROOM_PARENT
        else:
            prot["prototype_parent"] = EXIT_PARENT


ROOM_PARENT = {
    "typeclass": "typeclasses.rooms.XYRoom",
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
        "key": "Castle Valaria - Entrance",
        "desc": "Grandeur incarnate rises: the castle stands majestic, its formidably thick stone walls asserting a silent strength that has withstood the test of many ages. Turrets tower toward the sky, tip-capped with conical roofs of gleaming |#b43757slate|n that catch the light, commanding the landscape with a noble elegance. Crenelations along the battlements sketch a jagged silhouette against the vista, like the spine of a slumbering dragon. Grand are the gates, forged from resolute iron and bound in timeworn oak, adorned with intricate ironwork that tells of crafts long past. Ivy clings to the weathered facade, a tender marriage of nature with the stalwart bulwark, while wildflowers dare to bloom in the crevices where wind-swept seeds have found a home. <morning>|/|/    The castle walls blush with the rosy kiss of the morning sun, as tendrils of mist from the surrounding countryside retreat like bashful spirits before the day's embrace.</morning><afternoon>|/|/    In the fullness of the afternoon sun, the stonework seems alight with an inner fire, standing as a timeless testament to the days when knights and noble steeds would clatter across the drawbridge.</afternoon><evening>|/|/    As dusk nestles in, the evening light paints the stones in a palette of purples and grays, shadows lengthening to stretch out like velvet drapes across the landscape.</evening><night>|/|/    The moon bestows its silver benediction onto the facade, the turrets now sentinels in a world of quietude, under the watchful gaze of a tapestry of stars.</night>",
        # Smell: A fresh, bracing scent of cold stone mingles with the earthy fragrance of the surrounding forests and meadows. Sound: The distant clang of the blacksmith, the rustling of leaves in the gentle breeze, and the occasional call of a bird of prey from the high battlements. Taste: A hint of the morning dew, or perhaps the kiss of an evening frost, imparts a crisp, clean taste to the air, as if drawing from the very essence of the land.
    },
    (2, 1): {
        "key": "Castle Valaria - Grand Hall",
        "desc": "A great hall stretches magisterially from end to end, its lofty ceilings supported by robust columns that reach towards the heavens like the trunks of ancient trees. Vibrant banners drape from the vaulted expanse, each one a tapestry of heraldry that flutters gently, whispering tales of valor and legacy. Sentinel-like statues flank the peripheries, masterfully carved from marble and alabaster, their stoic faces and muscular forms embodying the virtues and triumphs of yesteryear. High above, an ornate balcony, wrought in intricate ironwork, graces the perimeter, offering a commanding view of the grandeur below. Its balustrade is a lacework of elegance, under which the multitude of faces revel in feasts and festivities, enveloped in the soft glow of torchlight. <morning>|/|/    Golden beams of the morning sun filter through the lancet windows, casting a radiant dance of light and shadow that plays across the floor in a mosaic of the day's nascent promise.</morning><afternoon>|/|/    The afternoon light spills across the high windows, bathing the great hall in a warm, amber radiance that illuminates the banners and breathes life into the statues as if they might descend and join the throng.</afternoon><evening>|/|/    The tender gleam of the evening moon filters in, casting a silvered hush over the hall, lending an ethereal quality to the faces of the statues and the fabric of the banners.</evening><night>|/|/    Suspended above, chandeliers gleam like constellations, their flickering candlelight reflecting off polished surfaces, mirroring the distant stars that peek through the night's veil from outside the high windows.</night>"
        # Smell: The rich scent of aging wood mingles with the faint aroma of beeswax from the candles and the occasional waft of lavender from the linens. Sound: The hall echoes with the soft patter of footsteps on stone, the occasional creak of the timbers above, and the distant melody of a lute string plucked in a far-off corridor. Taste: The air carries the subtle flavor of almond and honey from the kitchens, whetting the appetite for a feast that seems ever impending.
    },
    (2, 2): {
        "key": "Castle Valaria - Grand Hall",
        "desc": "A great hall stretches magisterially from end to end, its lofty ceilings supported by robust columns that reach towards the heavens like the trunks of ancient trees. Vibrant banners drape from the vaulted expanse, each one a tapestry of heraldry that flutters gently, whispering tales of valor and legacy. Sentinel-like statues flank the peripheries, masterfully carved from marble and alabaster, their stoic faces and muscular forms embodying the virtues and triumphs of yesteryear. High above, an ornate balcony, wrought in intricate ironwork, graces the perimeter, offering a commanding view of the grandeur below. Its balustrade is a lacework of elegance, under which the multitude of faces revel in feasts and festivities, enveloped in the soft glow of torchlight. <morning>|/|/    Golden beams of the morning sun filter through the lancet windows, casting a radiant dance of light and shadow that plays across the floor in a mosaic of the day's nascent promise.</morning><afternoon>|/|/    The afternoon light spills across the high windows, bathing the great hall in a warm, amber radiance that illuminates the banners and breathes life into the statues as if they might descend and join the throng.</afternoon><evening>|/|/    The tender gleam of the evening moon filters in, casting a silvered hush over the hall, lending an ethereal quality to the faces of the statues and the fabric of the banners.</evening><night>|/|/    Suspended above, chandeliers gleam like constellations, their flickering candlelight reflecting off polished surfaces, mirroring the distant stars that peek through the night's veil from outside the high windows.</night>"
        # Smell: The rich scent of aging wood mingles with the faint aroma of beeswax from the candles and the occasional waft of lavender from the linens. Sound: The hall echoes with the soft patter of footsteps on stone, the occasional creak of the timbers above, and the distant melody of a lute string plucked in a far-off corridor. Taste: The air carries the subtle flavor of almond and honey from the kitchens, whetting the appetite for a feast that seems ever impending.
    },
    (3, 2): {
        "key": "Castle Valaria - Lower Eastern Wing",
        "desc": "This is a place of quietude, a haven marked by an elongated corridor flanked by tall, narrow windows that filter sunlight into a gallery of hues on the stone floor. Fine tapestries, adorned with thread spun from the most vibrant of colors, hang from the walls, depicting forests and enchanted glades abounding with creatures both mythical and mundane. Arched doorways punctuate the long passage, leading to chambers unknown, their oaken doors carved with intricate symbols whispering of knowledge and secrets kept within. The air is imbued with a subtle stillness, as if the very stones hold their breath. <morning>|/|/    The morning light cascades through the windows, casting a golden glow that glistens on the polished floor, lending a serene ambiance to the wing's repose.</morning><afternoon>|/|/    By afternoon, the light is a radiant symphony, igniting the colors of the tapestries into a vivid spectacle that seems to animate the scenes depicted within their weaves.</afternoon><evening>|/|/    As the evening encroaches, the quality of light softens, wrapping the wing in a more contemplative cloak, the shadows lengthening like gentle fingers tracing the contours of the space.</evening><night>|/|/    Night envelops the wing in a calm darkness, pierced only by the occasional flicker of torchlight that creates a slow dance of light on the old stones, each footprint of flame as transient as time itself.</night>"
        # Smell: The scent of beeswax and polished wood is dominant, with a faint whisper of dried lavender from the sachets secreted amongst the tapestries. Sound: The hush is occasionally broken by the distant sound of a page turning, a sigh from an unseen servant, or the soft echo of a solitary set of footsteps pacing with contemplative regularity. Taste: In the stillness, there lies a taste of dust mingling with a ghost of incense long burned away, the flavor of the past lingering on the edge of perception.
    },
    (3, 3): {
        "key": "Castle Valaria - Living Quarters",
        "desc": "Nestled within the sturdy walls of the castle, the staff quarters provide a simpler contrast to the opulence found elsewhere. The rooms are modest yet well-tended, reflecting the sincerity and diligence of those who rest their weary bodies within after a day's labor. Whitewashed walls glow with a diffuse warmth, and sturdy wooden beams crisscross the low ceilings, instilling a sense of rustic safety. Each bed is a cozy haven, dressed in linens spun from homespun cloth, and accompanied by personal trinkets that speak quietly of homes and hearts afar. The communal hearth stands as the heart of the living space, its flames a jovial companion to the murmur of voices sharing tales and laughter well into the respite of the night. <morning>|/|/    The first slivers of dawn's light seep through the modest windows, coaxing the chamber into waking, setting the simple furnishings aglow with the promise of a new day's toil.</morning><afternoon>|/|/    The afternoon sun fills the room with a fullness, a steady light that lies upon the sturdy furniture like a gentle benediction to the labors of those who serve.</afternoon><evening>|/|/    Evening's tender light filters in softly, offering a reprieve from the day's work as the staff gather, their faces touched by the sunset's fading warmth.</evening><night>|/|/    Lanterns and candles offer their flickering lights to the night, casting everything into a soothing tapestry of shadows that invite the weary to rest their bones.</night>",
    },
    (4, 3): {
        "key": "Castle Valaria - Armory",
        "desc": "A vault of martial glory, a chamber resonant with the silent history of countless battles forged and fought. Rows upon rows of weapons are meticulously arrayed against the cold stone walls: swords with hilts wrapped in aged leather, lances that still bear the scars of violent clashing, and shields emblazoned with crests worn from the embrace of war. Each piece gleams with the care bestowed upon them by unseen hands, the steel whispering of polish and preservation. Mannequins dressed in chainmail and plate armor stand sentinel within this sanctum, their hollow gaze promising protection and intimidation. High above, racks of unstrung longbows await the call to arms, and quivers of arrows, their fletchings as yet unruffled, accompany them in silent readiness. <morning>|/|/    The weapons catch the tentative light of morning, reflecting a subtle luster that signals the start of another day's vigil.</morning><afternoon>|/|/    As afternoon dominates the firmament, each metallic surface captures the light and reflects it back, as if in challenge to the sun's own brilliance.</afternoon><evening>|/|/    In the evening, shadows claim dominion over the armory, and the armor seems to stir with the spirits of warriors long past, rustling with the echo of dusk's approach.</evening><night>|/|/    Under the watchful eye of night, torches flicker across the armaments, casting a live tableau of light and dark, a mimicry of the timeless battle between order and chaos.</night>"
        # Smell: The space is heavy with the scent of oiled metal and worn leather, the pungent trademarks of diligent maintenance and storied use. Sound: The hushed room echoes with the near-silent clinks and clanks of weapons shifting, a constant reminder of the ready arsenal at hand. Taste: There is a tang of iron on the tongue, a metallic reminder of the armory's purpose and the bitter tang of conflict it embodies.
    },
    (1, 2): {
        "key": "Castle Valaria - Lower Western Wing",
        "desc": "This is a place of quietude, a haven marked by an elongated corridor flanked by tall, narrow windows that filter sunlight into a gallery of hues on the stone floor. Fine tapestries, adorned with thread spun from the most vibrant of colors, hang from the walls, depicting forests and enchanted glades abounding with creatures both mythical and mundane. Arched doorways punctuate the long passage, leading to chambers unknown, their oaken doors carved with intricate symbols whispering of knowledge and secrets kept within. The air is imbued with a subtle stillness, as if the very stones hold their breath. <morning>|/|/    The morning light cascades through the windows, casting a golden glow that glistens on the polished floor, lending a serene ambiance to the wing's repose.</morning><afternoon>|/|/    By afternoon, the light is a radiant symphony, igniting the colors of the tapestries into a vivid spectacle that seems to animate the scenes depicted within their weaves.</afternoon><evening>|/|/    As the evening encroaches, the quality of light softens, wrapping the wing in a more contemplative cloak, the shadows lengthening like gentle fingers tracing the contours of the space.</evening><night>|/|/    Night envelops the wing in a calm darkness, pierced only by the occasional flicker of torchlight that creates a slow dance of light on the old stones, each footprint of flame as transient as time itself.</night>"
        # Smell: The scent of beeswax and polished wood is dominant, with a faint whisper of dried lavender from the sachets secreted amongst the tapestries. Sound: The hush is occasionally broken by the distant sound of a page turning, a sigh from an unseen servant, or the soft echo of a solitary set of footsteps pacing with contemplative regularity. Taste: In the stillness, there lies a taste of dust mingling with a ghost of incense long burned away, the flavor of the past lingering on the edge of perception.
    },
    (1, 3): {
        "key": "Castle Valaria - Dining Room",
        "desc": "The castle's dining room is a feast for the senses, a grand chamber where echoes of regality and conviviality harmonize. A prodigious table of dark oak dominates the center, its grain telling of years and the countless banquets it has borne. Above it hangs an ornate chandelier, each of its many candles cradled delicately, casting a warm, inviting glow upon the silver and crystal that sparkle upon the table. The walls are adorned with rich tapestries and portraits in gold-gilded frames, watching over the merry diners with eyes from ages past. High-backed chairs stand proudly, upholstered in velvet that drinks deeply of the room's luxury, providing comfort to all who gather here in the spirit of camaraderie and feasting. <morning>|/|/    The dining room awakens softly to the morning, the air filled with the quiet anticipation of breaking fast under the tender glow of first light.</morning><afternoon>|/|/    In the full embrace of the afternoon, sunlight bathes the room, enlivening the colors of the tapestries and lending each goblet and platter a radiant sheen.</afternoon><evening>|/|/    The gilded frames of the portraits catch the evening's fading glow, as if holding onto the day's last whispers, offering subtle company as the night ascends.</evening><night>|/|/    Candle flames sputter and dance in the night, the flickering light creating a merry theater of shadows and radiance upon the walls and faces alike.</night>"
        # Smell: The aroma of roasted meats, freshly baked bread, and the piquant scent of spiced wine intermingle, creating an olfactory symphony that entices one's deepest cravings. Sound: A chorus of clinking silverware, the gentle murmur of conversation, and shared laughter create a lively acoustic tapestry that breathes life into the stony keep. Taste: The ambient air carries with it the lingering taste of the night's feast, a mélange of savory and sweet that indulges the palate like the memory of a joyous celebration.
    },
    (0, 3): {
        "key": "Castle Valaria - Kitchen",
        "desc": "The heart of sustenance within the castle lies in its vast kitchen, a hive of ceaseless industry and culinary alchemy. Towering hearths blaze with gusto, providing both warmth and the crucible for cooking grand feasts. Cauldrons simmer atop the flames, bubbling with stews and broths that shall soon grace the tables of highborn and servant alike. Rows of wooden tables are laden with a cornucopia of fresh produce from the castle's own grounds, and the air is alive with the symphony of knives chopping and the rhythmic thud of dough being kneaded on well-worn boards. Copper pots and pans gleam from their hooks, reflecting the flickering light and faces of bustling cooks. Amidst this orchestrated chaos, the air hangs heavy with the promise of nourishment and the comforting solidity of tradition. <morning>|/|/    The dawn's early light creeps through windows high on the walls, casting a soft glow over the day's preparations - as loaves are set to bake and the first broths begin their gentle simmer.</morning><afternoon>|/|/    The afternoon sun streams in, warming the backs of the kitchen staff as they toil, the glittering beams turning steam from the pots into shining veils over their diligent heads.</afternoon><evening>|/|/    The heavy stone of the kitchen walls takes on an amber hue in the evening, the day's labor now culminating in a crescendo of searing, roasting, and plating.</evening><night>|/|/    Torches and candles take up the night shift, their light casting a steady glow onto surfaces dotted with the remnants of a feast, as the kitchen slowers its pace but never truly sleeps.</night>",
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
        "key": "Castle Valaria - Roundtable Lobby",
        "desc": "A grand lobby stretches outwards, its vaulted ceilings soaring to touch the very breath of the heavens. Polished marble floors, veined with hints of sienna, reflect the splendor above - a fresco depicting a dance of seasons in perpetual celebration. A large, circular table of golden oak stands proudly in the center, its surface a cartographer's dream, etched with the delicate lines of the known world, and around it, plush chairs invite discussions that echo with the gravity of diplomacy.\n\n    Flanking the room, statues carved from the purest alabaster cast an air of nobility; they stand as silent sentinels, their faces chiseled into expressions of serene wisdom that bestow an air of contemplation upon all who pass. Stained glass windows, like shards of captured sky, throw a kaleidoscope of colors onto the statues, painting them with the hues of tranquility and hope. <morning>|/|/    The first tendrils of dawn stretch through the stained glass, bathing the space in a gentle glow that animates the etched landscapes on the table with the promise of a new day.</morning><afternoon>|/|/    By the zenith of the day, the sun plays master artist, flooding the lobby with resplendent light, magnifying the statue's tranquil features to the realm of celestial guardians.</afternoon><evening>|/|/    As twilight whispers its arrival, the transition of hues shifts to an |#ffcb69amber|n, casting warm, elongated shadows that stretch across the floor, harkening to the closing of day.</evening><night>|/|/    The moon, a silent overseer, filters through the stained glass, enshrouding the statues in a softer version of day's grandeur, now whispered secrets in silvered tones.</night>",
    },
    (5, 2): {
        "key": "Castle Valaria - Upper Eastern Wing",
        "desc": "This corridor, lit by ornate sconces, cradles a warm, flickering candlelight that bestows an intimate glow upon the faces of ancestors immortalized in their gilded frames. Exquisite paintings of landscapes, both lush and serene, emerge from the depths of brooding canvases, verdant with the lifeblood of far-off realms. Bronze statues, polished by the passage of countless reverent hands, emerge from alcoves to punctuate the hallway with their bronzed patina and silent grace. The vaulted ceiling arcs high above, a canopied sky within the castle's embrace, adorned with frescoes that depict a ballet of celestial wonders, as if to mirror the heavens themselves. <afternoon>|/|/    As the afternoon sun casts its gaze through the tall, narrow windows, piercing the corridor with shafts of |#f4e242golden|n light, it sets the dust motes dancing in a spectacle of quiet beauty.</afternoon><evening>|/|/    In the hush of evening, shifting shadows play upon the floor, where the stone retains the last, loving touch of the day's warmth.</evening>",
        # "Smell:" The subtle scent of beeswax lingers in harmony with the aging oak and a faint draft of the bracing, fresh air from the nearby gardens. "Sound:" The soft echo of one's own footsteps partners with the distant, muffled calls of heralds and the occasional creak of a gently-swinging door. "Taste:" The perceived taste is one of antique elegance, a whisper of spiced pears served in distant halls, carrying the hint of bygone feast days.
    },
    (6, 2): {
        "key": "Castle Valaria - Eastern Study",
        "desc": "The walls rise up to a vaulted ceiling where the light from the rising sun filters through tall, arched windows, casting a golden hue over the room's rich tapestries.<morning> The early morning light illuminates the dust motes dancing playfully in the air, a harbinger of the day's potential.</morning><afternoon> Streams of sunlight pierce the chamber, traversing the room like silent sentinels, warming the faded pages of many an ancient tome.</afternoon> Stately bookshelves, carved from dark, noble woods, stretch from floor to ceiling, cradling countless leather-bound volumes whose spines hold tales of wisdom long past. A massive oak desk resides at the heart of the study, its surface lovingly polished to a deep sheen, upon which rests an open book, its pages splayed like the wings of a resting bird, and quills poised as if ready to soar across the parchment with ink-stained grace. A grand globe of the known world stands near the window, inviting the curious hand to spin it gently, while nearby, a celestial orrery traces the silent ballet of the heavens with unerring precision.",
        # Smell: The old parchment emits a subtle, musty sweetness, mingled with the lingering scent of lavender wafting from a delicate ceramic vase.
        # Sound: A gentle creaking of the wooden shelves under the weight of tomes accompanies the soft rustle of pages turned by an unseen scholar's hand.
        # Taste: The air carries the faint taste of dust mixed with the enduring tang of black ink.
    },
    (5, 0): {
        "key": "Castle Valaria - Storage Closet",
        "desc": "Tucked away, forgotten. The air is stale, laden with the musky fragrance of mildew and the pungent odor of rust. Dust-laden shelves bow under the weight of miscellaneous items once deemed valuable but now relegated to the shadows: chipped vases missing their once resplendent blooms, a plethora of candles rendered shapeless by time and disuse, and moth-eaten tapestries whose forgotten splendor is suggested only by the ghostly remnants of vibrant threads. Cobwebs festoon corners like tattered banners, while motes of dust hang suspended in the slivers of light that dare to pierce the small, grimy window pane. An assortment of decrepit trunks lies haphazardly strewn, their contents a mystery swathed in layers of time, the locks tarnished and keys long since lost. Amidst the clutter, the past lingers, stubborn and forlorn, while the present scarcely intrudes upon this sanctum of neglect.",
        # Smell: The unmistakable scent of old leather mixes with a dank earthiness that seeps from the cold stone walls.
        # Sound: The faint scurrying of unseen creatures provides a soft counterpoint to the silence that blankets the chamber.
        # Taste: Each breath tastes like forgotten years, a dusty blend of decay and abandonment that clings to the tongue.
    },
    (5, 1): {
        "key": "Castle Valaria - Small Library",
        "desc": "Nestled within the confines of the castle, a small library awaits, a jewel box of knowledge and narrative. It is a cozy alcove where walls are lined with walnut bookcases that reach up towards the timbered ceiling. Here, the shelves are laden with books of all sizes, their well-worn covers imbued with the dignity of age; they lean into one another as old friends might in quiet conversation. Ivory pages, edged with gold, peek out from their ranks, inviting the touch of those who seek their secrets. A grand, oriel window at the library's end creates a nook bathed in natural light, a solitary cushioned bench beneath it offering a perfect haven for the daydreamer or the devoted reader alike.<morning> The morning sun slips through the glass, brushing each tome with a gentle kiss, as if awakening them from their slumber.</morning><afternoon> The afternoon light streams through paneled glass, casting a patchwork of warmth that dances upon the floors and walls as the day progresses.</afternoon> Across the room, a small hearth waits patiently, surrounded by a pair of high-backed chairs upholstered in velvet, their cushions worn from many an hour of repose. A narrow table hovers near, its surface a tableau of reading glasses and leather bookmarks lying in haphazard repose. <night>|/|/    |#6A5ACDSlivers of lavender and twilight blue from a stained glass window filter through the library, dappling the interior with tranquil hues.</night>",
        # Smell: The scent of aged paper combines with the faint aroma of beeswax polish, used lovingly on the woodwork.
        # Sound: The subtle crackle of a fireplace contends with the quiet rustling of pages as readers immerse themselves within other worlds.
        # Taste: There is an almost palpable taste of oiled leather and the tang of ink that seems to linger in the air, like a remnant of whispered stories.
    },
    (1, 2): {
        "key": "Castle Valaria - Upper Western Wing",
        "desc": "This corridor, lit by ornate sconces, cradles a warm, flickering candlelight that bestows an intimate glow upon the faces of ancestors immortalized in their gilded frames. Exquisite paintings of landscapes, both lush and serene, emerge from the depths of brooding canvases, verdant with the lifeblood of far-off realms. Bronze statues, polished by the passage of countless reverent hands, emerge from alcoves to punctuate the hallway with their bronzed patina and silent grace. The vaulted ceiling arcs high above, a canopied sky within the castle's embrace, adorned with frescoes that depict a ballet of celestial wonders, as if to mirror the heavens themselves. <afternoon>|/|/    As the afternoon sun casts its gaze through the tall, narrow windows, piercing the corridor with shafts of |#f4e242golden|n light, it sets the dust motes dancing in a spectacle of quiet beauty.</afternoon><evening>|/|/    In the hush of evening, shifting shadows play upon the floor, where the stone retains the last, loving touch of the day's warmth.</evening>",
        # "Smell:" The subtle scent of beeswax lingers in harmony with the aging oak and a faint draft of the bracing, fresh air from the nearby gardens. "Sound:" The soft echo of one's own footsteps partners with the distant, muffled calls of heralds and the occasional creak of a gently-swinging door. "Taste:" The perceived taste is one of antique elegance, a whisper of spiced pears served in distant halls, carrying the hint of bygone feast days.
    },
    (1, 1): {
        "key": "Castle Valaria - Upper Western Wing",
        "desc": "This corridor, lit by ornate sconces, cradles a warm, flickering candlelight that bestows an intimate glow upon the faces of ancestors immortalized in their gilded frames. Exquisite paintings of landscapes, both lush and serene, emerge from the depths of brooding canvases, verdant with the lifeblood of far-off realms. Bronze statues, polished by the passage of countless reverent hands, emerge from alcoves to punctuate the hallway with their bronzed patina and silent grace. The vaulted ceiling arcs high above, a canopied sky within the castle's embrace, adorned with frescoes that depict a ballet of celestial wonders, as if to mirror the heavens themselves. <afternoon>|/|/    As the afternoon sun casts its gaze through the tall, narrow windows, piercing the corridor with shafts of |#f4e242golden|n light, it sets the dust motes dancing in a spectacle of quiet beauty.</afternoon><evening>|/|/    In the hush of evening, shifting shadows play upon the floor, where the stone retains the last, loving touch of the day's warmth.</evening>",
        # "Smell:" The subtle scent of beeswax lingers in harmony with the aging oak and a faint draft of the bracing, fresh air from the nearby gardens. "Sound:" The soft echo of one's own footsteps partners with the distant, muffled calls of heralds and the occasional creak of a gently-swinging door. "Taste:" The perceived taste is one of antique elegance, a whisper of spiced pears served in distant halls, carrying the hint of bygone feast days.
    },
    (0, 2): {
        "key": "Castle Valaria - Royal Bedchamber",
        "desc": "Among towers that climb towards the heavens and high walls of ancient strength rests the sanctum of velvet dreams: the royal bedchamber. Here, within these hallowed quarters, the air hums with a tranquil stillness, as if the stone itself respects the burdens borne by its slumbering inhabitants. Elegantly arched windows admit a fickle play of light and shadow upon the vast, four-poster bed, its frame ornately carved with a tapestry of woodland scenes, where mythic creatures dance amidst the twisting boughs. Adjacent to the bed, a great hearth cradles an eternal flame, its glow lending both warmth and a soothing lullaby of crackles and sparks. Precious, hand-woven tapestries adorned with shimmering threads of silver and gold cloak the walls, depicting the valiant deeds and serene wisdom of rulers past. Delicate frescoes of cherubs and blossoms grace the ceiling, a dance of grace and whimsy high above. <evening>|/|/    As evening enfolds the castle, lanterns imbued with golden light cast a serene glow upon the chamber, creating an intimate world set apart from the tumult of courtly life.</evening><night>|/|/    A silent moon carves a passage through the nighttime sky, bathing the room in a pale, ethereal luster, enchanting all with the promise of peace until the dawn.</night>"
        # The bed, a masterpiece of craftsmanship, is festooned with sumptuous fabrics: a duvet imbued with the softest down of geese, and pillows plump as cloud banks in a summer sky, encased in linens the color of fresh cream. Heavy damask curtains, deep burgundy in hue, can be drawn to shroud the room in opulent darkness, or parted to reveal the verdant sweep of the royal gardens beyond.
        # "Smell:" A delicate fragrance of lavender and rosewood permeates the air, interwoven with the faint, comforting scent of burning oak from the hearth. "Sound:" The soft rustling of silk drapes, swaying gently with the breath of the night air, mingles with the distant murmur of the castle’s lifeblood, kept at bay by thick stone walls. "Taste:" The air carries the regal essence of aged wine and honeyed fruits, reminiscent of banquets held in honor of kings and queens of yore.
    },
    (2, 1): {
        "key": "Castle Valaria - Balcony",
        "desc": "Suspended between the majestic western and eastern wings of the castle, the balcony is as if suspended in a daydream, which allows for a commanding view of the vast great hall below. Encased by an intricately wrought balustrade of goldenrod hue, it boasts a filigree of ironwork so fine, the delicate pattern seems spun by mythical weaver spiders from tales of yore. Here, one can lean upon the cool metal, while gazing out over the ebb and flow of courtly ceremony below, the balcony a privileged perch from which to observe the intricacies of high society weave through the grand dance of life. The stone underfoot, worn smooth by the presence of countless royal soles, glistens with a patina earned through ages of vigilant observation. <evening>|/|/    As dusk embraces the sky, the balcony becomes a stage for the ballet of twilight, where the heavy velvet of night drapes over the firmament, and the stars emerge as a scattering of |#dcdcdcsilver|n dust across the theater of the heavens.</evening>"
        # "Smell:" The perfume of the great hall rises to meet the fresh scent of flora—a mingling of old stone, polished wood, and a tapestry of banquet delicacies. "Sound:" From below, the symphony of communal life crescendos—a constellation of conversations, laughter, and the soft, rhythmic steps of those who dance to the tune of royalty. "Taste:" There exists an ambience of aerial grace, imbued with the subtle taste of the crisp, outside air that mixes with the sweet essence of garnished dishes from feasts laid out beneath.
    },
    (3, 1): {
        "key": "Castle Valaria - Balcony",
        "desc": "Suspended between the majestic western and eastern wings of the castle, the balcony is as if suspended in a daydream, which allows for a commanding view of the vast great hall below. Encased by an intricately wrought balustrade of goldenrod hue, it boasts a filigree of ironwork so fine, the delicate pattern seems spun by mythical weaver spiders from tales of yore. Here, one can lean upon the cool metal, while gazing out over the ebb and flow of courtly ceremony below, the balcony a privileged perch from which to observe the intricacies of high society weave through the grand dance of life. The stone underfoot, worn smooth by the presence of countless royal soles, glistens with a patina earned through ages of vigilant observation. <evening>|/|/    As dusk embraces the sky, the balcony becomes a stage for the ballet of twilight, where the heavy velvet of night drapes over the firmament, and the stars emerge as a scattering of |#dcdcdcsilver|n dust across the theater of the heavens.</evening>"
        # "Smell:" The perfume of the great hall rises to meet the fresh scent of flora—a mingling of old stone, polished wood, and a tapestry of banquet delicacies. "Sound:" From below, the symphony of communal life crescendos—a constellation of conversations, laughter, and the soft, rhythmic steps of those who dance to the tune of royalty. "Taste:" There exists an ambience of aerial grace, imbued with the subtle taste of the crisp, outside air that mixes with the sweet essence of garnished dishes from feasts laid out beneath.
    },
    (4, 1): {
        "key": "Castle Valaria - Balcony",
        "desc": "Suspended between the majestic western and eastern wings of the castle, the balcony is as if suspended in a daydream, which allows for a commanding view of the vast great hall below. Encased by an intricately wrought balustrade of goldenrod hue, it boasts a filigree of ironwork so fine, the delicate pattern seems spun by mythical weaver spiders from tales of yore. Here, one can lean upon the cool metal, while gazing out over the ebb and flow of courtly ceremony below, the balcony a privileged perch from which to observe the intricacies of high society weave through the grand dance of life. The stone underfoot, worn smooth by the presence of countless royal soles, glistens with a patina earned through ages of vigilant observation. <evening>|/|/    As dusk embraces the sky, the balcony becomes a stage for the ballet of twilight, where the heavy velvet of night drapes over the firmament, and the stars emerge as a scattering of |#dcdcdcsilver|n dust across the theater of the heavens.</evening>"
        # "Smell:" The perfume of the great hall rises to meet the fresh scent of flora—a mingling of old stone, polished wood, and a tapestry of banquet delicacies. "Sound:" From below, the symphony of communal life crescendos—a constellation of conversations, laughter, and the soft, rhythmic steps of those who dance to the tune of royalty. "Taste:" There exists an ambience of aerial grace, imbued with the subtle taste of the crisp, outside air that mixes with the sweet essence of garnished dishes from feasts laid out beneath.
    },
    (3, 3): {
        "key": "Castle Valaria - Audience Chamber",
        "desc": "The castle's throne room is a grand, voluminous chamber where majesty is etched into every detail. Towering pillars of veined marble ascend to a lofty ceiling, upon which artists of old have lavished frescoes of clouds and cherubs that dance in eternal blue skies. The room's vast expanse is filled with a hushed reverence, ambient light filtering through tall, narrow windows, embroidering the air with an almost tangible luminance. At the far end, upon a dais of gleaming alabaster steps, stands the throne itself - a masterwork of craftsmanship, carved from timeworn oak and embellished with |#FFD700|ngilded detailing|n, the seat cushioned in sumptuous velvet. Flanking the throne, statuesque suits of armor keep silent vigil, their polished surfaces catching the light and casting soft reflections upon the checkered marble floor. Heavy velvet drapes, deep crimson in hue, hang alongside the chamber walls, mute observers to the irrevocable edicts proclaimed within this sacrosanct space.",
        # Smell: The scent of beeswax from meticulously maintained floors mingles with the trace fragrance of the ceremonial oils that anoint the dais.
        # Sound: Footsteps echo solemnly across the stone floor, each step a reminder of the countless that have come before in times of celebration and trepidation.
        # Taste: The air bears an austere quality, as if one could taste the residue of power and the tang of ambition that hang heavy in the atmosphere.
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
