from . import prototypes

NAUTILUS_INNER_HOLD = {
    "prototype_key": "xyz_room",
    "typeclass": "typeclasses.nautilus.rooms.NautilusInnerHold",
}

TUTORIAL_MAP = r"""
 + 0 1 2 3 4

 4       #
         |
 3   #---+-#
     |   | |
 2 #-#-# #-#
     |     |
 1 #-#-#   #
     |
 0   #

 + 0 1 2 3 4
"""

PROTOTYPES = {
    (1, 1): {
        "prototype_parent": "xyz_room",
        "key": "|CThe Nautilus - Berthing|n",
        "desc": "In the dim gloom of the ship's berthing, a solitary soul stirs amongst the vestiges of slumbering shadows. It's a chamber somber and forlorn, where mortality hangs heavy in the stagnant air. Bunks line the narrow space, their iron frames wrapped in the icy embrace of the deep, each a silent cradle for a life departed. Death's chill lingers, a long, unbreaking vigil held by those who slumber without end. Linen once white drapes the forms that did not wake, pale and still beneath forever's sleep. Above, timbers groan, a lament for souls lost to the deep's unfathomed heart, where no light dares to linger or hope to pierce the oppressive darkness.",
        "senses": {
            "feel": "A frigid draft meanders through the space, carrying the unwelcome embrace of the grave.",
            "smell": "The brine of the ocean mingles with the melancholy perfume of untreated wood and forlorn dreams.",
            "sound": "The muted groans of the ship's hull, a morose lullaby to the departed, fills the eerie silence.",
            "taste": "The air bears the faint brine of tears unwept, a taste of salt upon the tongue.",
        },
        "details": {
            "bunks": "A singular bunk stands apart, of furnishing sparse and unadorned; it is here the sole waking soul finds themselves, untethered from death's silent banquet."
        },
    },
    (0, 1): {
        "prototype_parent": "xyz_room",
        "key": "|CThe Nautilus - Berthing|n",
        "desc": "The berthing's western alcove holds a desk, its sturdy oak a witness to the room's forlorn ambiance. Years beneath the sea have darkened its grain. Atop it rests an assemblage of |#ffd700|nletters, their edges curled from the embrace of the damp sea air, each character inscribed with careful precision now tinged with the golden patina of age. The desk, surrounded by the immutable repose of the room's deceased occupants, feels like an archive of unfinished stories, holding fast to the last thoughts of those doomed to sleep beneath the waves.",
        "senses": {
            "feel": "The cool, still air bears the weight of the ocean's depth, offering a tranquil yet unnerving caress.",
            "smell": "The scent of aged wood and ink faintly permeates the space, redolent of history and secrets kept.",
            "sound": "The subtle shift of paper as the gentle currents of water stir the letters is the only respite from the silence.",
            "taste": "A taste reminiscent of old books and saltwater lingers on the tongue, a testament to the sea's enduring embrace.",
        },
        "details": {
            "letters": "The letters lie in a neat array, their golden script catching what little light there is, spelling out half-forgotten memories and final words meant for those far from the ocean's depths.",
        },
    },
    (1, 0): {
        "prototype_parent": "xyz_room",
        "key": "|CThe Nautilus - Berthing|n",
        "desc": "Within the southern alcove of the berthing, a small recess houses personal effects untouched by time's mercy. An ensemble of trinkets - a tarnished |#c0c0c0locket|n, a |#b87333compass|n whose needle swings with indecision, and a scattering of |#ffd700coins|n from realms afar - rests atop a simple wooden chest. The chest, its varnish dulled and worn, bears carvings of the creatures of the deep: serpents and leviathans winding in eternal chase around its lock. Here, the presence of those who once called this chamber their own lingers like a watermark, stories untold and voyages abruptly ceased.",
        "tags": "test",
        "senses": {
            "feel": "The stillness of the alcove melds with the coolness of the submerged environment, a silent sanctuary away from the ceaseless tides beyond.",
            "smell": "Aromatic hints of wood polish faintly rise above the omnipresent odor of brine and decay.",
            "sound": "The muted sound of water droplets, which periodically fall from the chamber's ceiling, keeps a slow, rhythmic cadence with the silence.",
            "taste": "The taste of metal and salt hangs in the air, vestiges of the coins and navigational tools left to languor.",
        },
        "details": {
            "locket": "The locket, its once lustrous surface now dulled to a somber silver, lies open, revealing a miniature painted portrait protected by a thin sheet of cloudy glass. Weathered by both time and tide, the likeness within gazes out with colors that struggle against the encroachment of decay, their vibrancy a faint whisper of past affections.",
            "compass": "The compass, encased in a copper shell turned verdigris at the edges, sits heavy and immobile. Its face still gleams faintly when caught by stray shafts of light, the cardinal points etched deeply into the medal as a lasting declaration of direction in a world on the waves.",
            "coins": "Surrounding the other artifacts, coins spill across the chest, their diversity a small treasure trove of tales from afar but ultimately foreign and useless to you. Each disc, whether gilt or silvery or possessing the burnished warmth of copper, carries upon it the countenance of a soverign or the sigil of a distant land, the raised details catching the dim light as if holding one last time to the days above the deep.",
        },
        "items": [(prototypes.NAUTILUS_WOODEN_CHEST, 1)],
    },
    (2, 1): {
        "prototype_parent": "xyz_room",
        "key": "|CThe Nautilus - Berthing|n",
        "desc": "In the eastern alcove, the stark truth of the berthing reveals itself with unflinching finality. The |xcorpses|n of seafarers slump against the corroded bulkhead, their forms draped in the remnants of uniforms that once signified their roles. Flesh and fabric have yielded, leaving behind a grim tableau of bone and shadow, the final act of a play from which all actors have departed. The once vibrant hues of their garb are now muted, a pallor of greys and charcoal forming sigils and rank are now barely discernible amid the disarray. Despite the decay, there exists a sense of order, the crew's last station at their posts preserved in motionless silence.",
        "senses": {
            "feel": "A poignant chill suffuses the air, a reminder of the natural order unheeded by the hands of time and tide.",
            "smell": "The scent of iron and mold converge, an olfactory echo of lives once warm now surrendered to the sea.",
            "sound": "Silence reigns, save for the sound of subtle settling, the slow reclamation of the space by the ocean's silence.",
            "taste": "The taste of staleness and decay lingers unpleasantly, a stark contrast to the once salty, invigorating air of the open sea.",
        },
        "details": {
            "corpses": "Attire merges with wearer, the decay uniform in its progress; amidst the remains, insignias and medals cling to fabric, persevering symbols of duty and honor in the unyielding dark."
        },
        "items": [(prototypes.NAUTILUS_SAILOR_CORPSE, 1)],
    },
    (1, 2): {
        "prototype_parent": "xyz_room",
        "key": "|CThe Nautilus - Map Room|n",
        "desc": "This sanctum of cartography and navigation is replete with the relics of maritime exploration. Vast parchment |#f5deb3scrolls|n cascade across a grand central table. They are meticulously inked with the ebony trails of bygone voyages, the coastlines and routes weaving an intricate dance of ambitious gold and cautious azure. The |#d2b48cwalls|n around stand as custodians, cloaked themselves in a patchwork of celestial charts and nautical maps, the animate tans and hused blues of their geography punctuated by the crimson points of historic significance and burnished golden latitudes. Amidst the meticulous order of this seafarer's haven sits a figure upon a chair. Their head, bereft of its natural crown, reveals the grotesque starkness of raw, vulnerable thought laid bare.",
        "senses": {
            "feel": "The juxtaposition of serenity in the map-strewn room against the visceral sight invokes a disquiet that hangs palpably in the air.",
            "smell": "Earthy tones of parchment and leather are undercut by the iron tang of exposed mortality.",
            "sound": "A profound hush envelops the room, only occasionally breached by the labored, ragged breaths of the figure and the faint rustle of maps.",
            "taste": "The air has a bitter tinge, combining the must of dust-laden paper and the acrid sting of blood.",
        },
        "details": {
            "scrolls": "These sprawling parchments, once vibrant, now adopt a mellowed hue, their surface a battleground where ink and time contend to shape history's trace.",
            "walls": "The walls, blanketed with the catographer's craft, display a palimpsest of exploration; each map, frayed at the edges, layers upon its predecessor in a narrative of discovery.",
        },
        "items": [(prototypes.NAUTILUS_BROKEN_BODY, 1)],
    },
    (0, 2): {
        "prototype_parent": "xyz_room",
        "key": "|CThe Nautilus - Map Room|n",
        "desc": "The western flank of the area dissolves into an alcove where shelves brimming with rolled charts and dusty tomes stand in haphazard ranks. The wood of the bookcases wears a patina of age and salt, the once intricate carvings of ships and mythical sea beasts barely discernible under a film of fine silt. Amongst the heavy, leather-bound tomes, one |Cvolume|n commands particular attention, its cover an imposing dark slate blue. The air here is dense with the musk of leather-bound journals and the brittle aroma of paper long spared the sun's caress. Cobwebs lace the corners, draped like tattered ensigns.",
        "senses": {
            "feel": "Respect for the diverse tapestry of life is almost tangible, swelling within the room with each page turned.",
            "smell": "A hint of ink and parchment layers over the salty backdrop, an olfactory glimpse into the scholarly pursuit that birthed the volume.",
            "sound": "The air is gifted with the gentle rustle of paper, a whispering liaison between reader and the realm of lore inscribed across the pages.",
            "taste": "There's a subtle flavor to the air, as if one can taste the myriad climates and terrains spoken of within the tome, each page a new environment.",
        },
        "details": {
            "volume": "The tome's spine creaks with the weight of its contents, the gilt lettering proclaiming it as a chronicle of epic proportions - a compendium of a millennia - spanning tales of humanoid kinship and strife. Elves, dwarves, humans, and countless others fill its pages with their triumphs and tribulations, the densely penned text at times giving way to intricate illustrations that leap from the pages as if alive with their own ancient essence.",
            "tome": "The tome's spine creaks with the weight of its contents, the gilt lettering proclaiming it as a chronicle of epic proportions - a compendium of a millennia - spanning tales of humanoid kinship and strife. Elves, dwarves, humans, and countless others fill its pages with their triumphs and tribulations, the densely penned text at times giving way to intricate illustrations that leap from the pages as if alive with their own ancient essence.",
        },
    },
    (2, 2): {
        "prototype_parent": "xyz_room",
        "key": "|CThe Nautilus - Map Room|n",
        "desc": "The map room extends towards an observatory area, engineered for the study of stars and the celestial paths that guide a vessel's course. The domed ceiling which once welcomed light from the heavens, now broods under a veil of darkness, an opaque shroud denying any glimpse of the sky. |cAstrolabes|n and other devices of aged brass lay abandoned. Their intricate gears lock in a silent, cryptic dialogue. One large, circular |wwindow|n stares out into the abyss, its glass cracked in a spiderweb of silvered lines that reflect the feeble luminscence of the deep. The very air whistles quietly through the fissures, thick with an unsettled tension.",
        "senses": {
            "feel": "An ominous presence pervades, charging the air with an electric tingle that raises the nape's fine hairs with its unvoiced threat.",
            "smell": "The metallic tang of damaged equipment mingles with the staleness of a space long sealed from the outside world, an aroma both chilling and foreboding.",
            "sound": "The silence in the east is a pregnant pause, occasionally broken by the strain of overwrought hinges or the ghostly hum of a bygone machine's idle whir.",
            "taste": "Tasting the air reveals a mineral sharpness, as if it too were sliced by the same mysterious force that fractured the glass and stilled the room's once purposeful activity.",
        },
        "details": {
            "astrolabes": "Scattered across the observatory, the astrolabes are relics of brass and precision, their form providing homage to the goblin artificers who once crafted devices of such cunning complexity. Each dial and plate intricately engraved, not merely with the signs of the zodiac but also with minuscule depictions of goblin life, hint at a culture rich with tradition and knowledge. To lay one's gaze upon them is to be filled with sudden, fleeting visions of goblins in their daily toil and ancient history, their ingenuity and craft flashing past with ephemeral encounters with a world both alien and intimate.",
            "window": "Dominating the observatory, the window is a melancholic mosaic, its once pristine transparency marred by fissures that catch the light in haunting displays. Where the glass remains intact, it reflects the gloom of the room, an ever-watchful eye that has beheld the unfolding of the ship's fate. Through this fractured pane, the incomprehensible depth of the ocean gazes back, exacerbating the sense of isolation from the world above and the celestial guidance now lost.",
        },
        "items": [(prototypes.NAUTILUS_GOBLIN_CORPSE, 1)],
    },
    (1, 3): {
        "prototype_parent": "xyz_room",
        "key": "|CThe Nautilus - Main Deck|n",
        "desc": "Beyond a jagged breach, the walls give way to the main deck, a sprawling expanse beneath the oppressive weight of the ocean's gaze. The planks groan under the pressure of unseen currents, the sound of a steady chorus of the ship's unrest. Masts stripped of their sails stand as barren pillars, watching over a deck strewn with the detritus of calamity - ropes lie in tangled heaps like serpents turned to stone, and broken barrels mingle with the remnants of the ship's once busy life.|/|/    <morning>|#ffd700The nascent glow of morning filters softly through the waters, hinting at a new day out of the reach in the somber deep.|n</morning><afternoon>|#ffa500An elusive warmth suggests afternoon's peak, the sun's rays striving vainly to penetrate the entombing depths.|n</afternoon><evening>|#dc143cThe vestiges of evening play across the watery expanse, casting wane, fading hues upon the derelict scene.|n</evening><night>|xIn the shroud of night, all remnants of day succumb to the undisturbed shadow that dances with the rhythm of the tides.|n</night>",
        "senses": {
            "feel": "An uneasy energy pervades the deck, a perversion of sea breezes now laden with the silent testimony of disaster.",
            "smell": "The bracing scent of brine is here too, suffused with the acrid bite of seaweed decay and the musk of waterlogged wood.",
            "sound": "The creak of the timeworn deck combines with the muffled, repetitive knocking of loose fittings against the ship's side, a forlorn rhythm in this underwater requiem.",
            "taste": "The taste of dampness and ruin clings to the tongue, hinting at the desolation that has enveloped this place of once well-trodden paths and shouted commands.",
        },
        "details": {
            "planks": "The planks, remnants of a stout construction, sprawl across the deck echoing the strength of the mighty oaks from which they were hewn, now bleached and stripped of life.",
            "masts": "Majestic masts, once proud conduits of wind and speed, stand bereft of canvas and purpose, their stark forms a skeletal remembrance of the Nautilus' voyaging spirit.",
            "deck": "The deck speaks of times better and busier, the worn pathways between fixtures and fittings telling tales of countless sailors' tread and the frenzy of life at sea.",
            "ropes": "Coiled and kinked, the ropes lay in disarray, a chaotic aftermath frozen in time, their fibers frayed by toil and the relentless wear of the elements.",
            "barrels": "The scattered barrels, once full of sustenance and spirits for the journey, now lay broken, their contents long since claimed by the deep, leaving only husks behind.",
        },
    },
    (4, 3): {
        "prototype_parent": "xyz_room",
        "key": "|CThe Nautilus - Hallway|n",
        "desc": "The dimly lit hallway stretches out, its once pristine walls now marred by the unsettling remnants of dark rituals. The air hangs heavy with an oppressive stillness, broken only by the occasional creak of the ship's timbers, as if the vessel itself were mourning the atrocities that have taken place within its confines. The floorboards, stained with the telltale signs of spilled blood, groan underfoot. Shadows dance along the walls, cast by the flickering light of a few remaining oil lamps, their feeble glow serving only to deepen the sense of foreboding that permeates the space. The peeling wallpaper, once a rich burgundy, now appears as a sickly, mottled hue, its intricate patterns distorted. At the far end of the hallway, a heavy wooden door stands slightly ajar, its iron hinges rusted and twisted.|/|/    <morning>|#808080The pale, sickly light of dawn filters through the grimy portholes, casting an eerie, gray pallor over the hallway, as if even the sun itself were reluctant to shed its light upon this forsaken place.|n</morning><afternoon>|#A9A9A9The afternoon sun, obscured by thick clouds, casts a gloomy, ashen light through the portholes, further emphasizing the lifeless atmosphere that pervades the hallway.|n</afternoon><evening>|#696969As evening falls, the dying light filtering through the portholes takes on a sinister, leaden hue, transforming the hallway into a realm of gathering shadows and deepening despair.|n</evening><night>|xIn the dead of night, the hallway is engulfed in an impenetrable, inky darkness, broken only by the feeble, flickering light of the oil lamps, their wavering flames casting grotesque, dancing shadows upon the walls.|n</night>",
        "senses": {
            "feel": "The air feels thick and oppressive.",
            "smell": "A faint, cloying scent of decay and incense lingers in the air.",
            "sound": "The silence is broken by the occasional creak and groan of the ship's timbers, like the mournful whispers of the souls trapped within.",
            "taste": "The taste of fear and despair lingers on the tongue.",
        },
        "details": {
            "lamps": "The oil lamps, their brass fittings tarnished and dented, emit a feeble, flickering light, casting distorted shadows that seem to writhe and dance upon the walls, as if possessed by the malevolent spirits that haunt this place.",
            "door": "The heavy wooden door at the end of the hallway stands slightly ajar, its once sturdy frame now warped and twisted, as if even the inanimate wood had recoiled in horror at the atrocities it had witnessed.",
        },
    },
    (4, 2): {
        "prototype_parent": NAUTILUS_INNER_HOLD,
        "typeclass": "typeclasses.nautilus.rooms.NautilusInnerHold",
        "key": "|CThe Nautilus - Inner Hold|n",
        "desc": "Shrouded in insidious darkness, the hold below betrays its purpose with an unyielding grimness. Corrosion grips the iron lattice of cell doors, the once unwavering barriers succumbing to a relentless siege by salt and moisture. Narrow confines serve as punitive chambers - stark, unfurnished save for the barest necessities of a cot bolted firmly to the wall, a hard wooden bench, and a chamber pot. The air hangs thick with a stagnant heaviness as if suffused with the muted laments of souls once held within these oppressive walls. Long-dead lanterns spaced methodically along the corridor offer no relief from the pervasive umbrage, their glassy eyes mirroring the void where hope's light has long since dwindled.",
        "senses": {
            "feel": "The chilling air within the hold clings to the skin, a damp shroud that seems to seep into the marrow.",
            "smell": "An odor of mildew and the ghost of brine-soaked wood combines with a pungent, iron tang of rust.",
            "sound": "Silence throbs in the ears, punctuated only by the occasional drip of water that seems to mark the passage of eternity.",
            "taste": "A metallic residue hangs in the air, coating the tongue with the stark, unforgiving taste of confinement and neglect.",
        },
        "details": {
            "bars": "The ironwork, once imposing now succumbs to the rust that clings and eats away at its strong constitution, a creeping decay that threatens the solidity of confinement.",
            "cot": "Each cot, fixed against the hold's walls, serves as a testament to minimal comfort, the fabric of their mattresses frayed, embodying the weariness of a rest that never truly came.",
            "bench": "The bench bears the worn grooves of countless hours spent in uneasy repose, standing in stark contrast to the stone-cold floor beneath.",
            "pot": "Austere and overlooked, the chamber pot remains an object that time has not deigned to touch, underscoring the abject solitude once found here.",
            "lanterns": "The lanterns, their light extinguished, are sheathed in the accumulated grime of a tragedy silent and unseen, the faint outlines of their form barely discernible in the cloaking darkness.",
        },
        "items": [(prototypes.NAUTILUS_WOODEN_CHEST, 1)],
    },
    (4, 1): {
        "prototype_parent": "xyz_room",
        "key": "|CThe Nautilus - Morphosis Room|n",
        "desc": "Enclosed by walls etched with a menacing lexicon of runes, the chamber harbors an air of imminent darkness. A viscous, scarlet gleam emanates from the cryptic symbols, casting the room in a ghastly tableau as if illuminated by the very essence of malice. Fresh gore adheres to the surface of the floor, its viscosity narrating a grim chronicle of ritual and sacrifice. At the heart lies a shadowed altar, crafted from somber stone, besieged by a horde of unsanitary instruments and blood-stained blades. The atmosphere vibrates with eldritch energy, a palpable presence that imbues the sinister sigils with a pulsating life, as though on the verge of birthing some abhorrent sentience.",
        "senses": {
            "feel": "A sweltering heat envelops the chamber, the warmth of spilt life force and abhorrent ceremonies suffusing every corner.",
            "smell": "An ironclad odor clings to the air, permeated by the stench of smoldering incense and the undeclared scents of dark conjurations.",
            "sound": "An eerie resonance pervades the stillness, the whisper of otherworldly entities caressing the edges of reality, drawn forth by the chamber's bloodied inscriptions.",
            "taste": "The foul essence of blood and brimstone lingers on the tongue, an unsettling reminder of the chamber's vile purpose.",
        },
        "details": {
            "altar": "Centrally placed, the altar is a slab of darkness, its surface a canvas of arcane imagery weeping with the freshness of sanguine offerings."
        },
        "items": [(prototypes.NAUTILUS_WOODEN_CHEST, 1)],
    },
    (3, 2): {
        "prototype_parent": "xyz_room",
        "key": "|CThe Nautilus - Entrance to the Helm|n",
        "desc": "An ornate door stands as the silent guardian to the vessel's command center, a threshold that separates the chaos of the sea from the calculated order required to navigate it. Resilient oak panels, bound by bands of deep bronze, are adorned with carvings that depict roiling waves and mythic creatures of the deep. Above, the transom is inlaid with stained glass of cobalt and khaki, depicting a compass rose that filters the ambient light into a map of colors on the floor. Heavy iron hinges strain silently, patinated by salt and spray.",
        "senses": {
            "feel": "An aura of anticipation brushes against those who approach, the air charged with the import of countless decisions made just beyond.",
            "smell": "The scent of aged wood and a tinge of metal polish rise from the door, mingling with the omnipresent brine of the ocean.",
            "sound": "Each movement near the entryway seems to carry an echo, as if the very air anticipates the creak of the hinges and the subsequent orders that will steer the ship's course.",
            "taste": "There is a crispness here, as if one can taste the threshold between the tumult of outside elements and the stability that command necessitates.",
        },
    },
    (3, 4): {
        "prototype_parent": "xyz_room",
        "key": "|CThe Nautilus - Helm|n",
        "desc": "Arrayed with instruments of navigation and control, this chamber exudes an air of mastery over the unyielding sea. A large wheel, polished by years of seafaring hands, commands the space, its spokes reaching out like the rays of a maritime sun. Panels of brass fittings and gauges cluster in stations where maps lay sprawled, their meticulous details eager to be charted. Taut rope and varnished wooden planks lie beneath wide windows which arch across the forward wall, offering an unobstructed vista of the ocean's vast canvas, where the play of light and shadow dares the hopeful and the wary to peer into the abyss.|/|/    <morning>|#ffd700Sunrise ushers a golden radiance that bathes the room in hope, casting long shadows behind the helm's many contours and glinting off brass instruments with a dawning new day.|n</morning><afternoon>|#ffa500The high afternoon sun pours in, its brilliance sharp and clear, rendering the room a theater of light; every tool and surface reflects its strong, unwavering course across the sky.|n</afternoon><evening>|#dc143cAs dusk falls, the room is cloaked in amber hues of twilight, the gauges and maps thrown into soft relief while the wheel stands silhouetted against the shifting of night.|n</evening><night>|xUnder the cloak of night, the chamber assumes a subdued, mysterious aspect, the moon's silvered light tracing paths across the dashboard, a keeper of vigil in the unending obsidian expanse.|n</night>",
        "senses": {
            "feel": "The room confers a sense of hushed power, where the thrill of conquest over nature's wildest domain palpably shivers through the air.",
            "smell": "A melange of polished wood, the oil of machinery, and a hint of saltwater creates a unique bouquet that is both invigorating and comforting.",
            "sound": "Muted ticks and the gentle clinks of the navigator's tools provide a rhythmic accompaniment to the distant thrum of the sea against the hull.",
            "taste": "The air carries with it the flavor of adventure, a hint of excitement and trepidation that combines with the essence of an ocean breeze.",
        },
        "details": {
            "wheel": "The ship's wheel, an emblem of control, stands resolute. Its smooth, polished wood bears the indents of countless grasps, and the brass hub at its center gleams with the care befitting the helm's heart.",
            "instruments": "Brass instruments, each one a marvel of maritime engineering, dot the space. Gauges measure depth and speed, their needles poised to jump at the ship's command, while astrolabes and compasses stand ready to navigate through the stars and the seas alike.",
            "maps": "Sprawled across the tables, the maps portray a world of possibility. Inked coastlines and sketched terrain wait silently for the navigator's mark, the paper edges worn soft from the touch of pondering fingers.",
            "rope": "Coils of rope, sinewy and strong, hang from their pegs. Each thread is woven tight, a testament to the strength and reliability demanded by the unpredictable waters that the ship charts.",
            "wood": "The varnished beams and panels of the room exude a warmth only aged timber can. The grain patterns tell a tale of winds and waters weathered, the sheen a result of careful maintenance in the face of saline assaults.",
            "windows": "The arched windows encompass the room's forward wall, crafted to withstand the ocean's wrath. They offer a portal to the vast theater of the sea, framing the ever-changing view that is part sailor's dream, part navigator's challenge.",
        },
    },
}

XYMAP_DATA_TUTORIAL = {
    "zcoord": "nautilus",
    "map": TUTORIAL_MAP,
    "prototypes": PROTOTYPES,
}

XYMAP_DATA_LIST = [XYMAP_DATA_TUTORIAL]
