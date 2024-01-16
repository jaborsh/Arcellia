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
        "key": "|CThe Nautilus - Berthing",
        "desc": "In the bowels of a seafaring vessel, the air hangs heavy with the scent of brine and unwelcome decay, casting an ominous pall over the confined quarters. Each bunk, shrouded in shadows, cradles a motionless form, a grisly exhibit of death's quiet conquest. All save one - a solitary refuge from the macabre collection - that had served as your unwitting cocoon amidst the calamity that befell this cursed vessel. Thick webs drape like mournful curtains from the wooden beams above, and the creaking protest of the ship's timbers sings a dirge that resonates through the space. A mournful tableau is set, where desolation holds court with the remnants of the deceased crew, their stories silenced by some unspoken horror.",
        "senses": {
            "feel": "The air, clammy and still, clings to the skin with the chill of the grave.",
            "smell": "The pungent aroma of saltwater mingles with the disquieting sweetness of decay.",
            "sound": "The groaning of the ship's hull plays a haunting melody, punctuated by the distant crash of waves.",
            "taste": "The stale taste of salt and neglect lingers in the mouth, a remembrance of the sea's omnipresence.",
        },
        "details": {
            "bunk": "The vacant bunk, a narrow cot of rough-hewn timber, boasts a thin, tattered mattress that whispers of more restful nights now lost to time."
        },
    },
    (0, 1): {
        "key": "|CThe Nautilus - Berthing",
        "desc": "You encounter a series of trunks and personal effects strewn haphazardly across the creaking wooden floor. The belongings, once the treasure of lives now extinguished, lie in a morbid disarray, as if abandoned in haste or in the throes of a struggle. Half-hidden under a forlorn piece of sailcloth, a scatter of yellowed letters and leather-bound journals beckons, their secrets sealed within, untouched by the chaos that claimed their owners. Cleaved into the timber walls, deep gouges speak mutely of desperation, perhaps the last futile attempts of those who yearned to escape their fated demise. Above, the faint glimmer of a lantern swings gently, casting capricious shadows that dance and flit across the confined space, as though mocking the stillness of the departed.",
        "senses": {
            "feel": "The ground shifts underfoot, a grim reminder of the unsteady world outside the decrepit wooden sanctuary.",
            "smell": "Whispers of mildew and leather rise from the abandoned trunks, telling tales of long voyages and old memories.",
            "sound": "The moan of the sea melds with the soft rustle of paper, a somber harmony to the room's stillness.",
            "taste": "Dust motes mingle with the briny air, tasting of times past and stories left adrift.",
        },
        "details": {
            "letters": "Upon the yellowed pages, the ink curls and weaves in the elegant script of hands now stilled, their final words awaiting an audience with the living.",
            "journals": "Upon the yellowed pages, the ink curls and weaves in the elegant script of hands now stilled, their final words awaiting an audience with the living.",
        },
    },
    (1, 0): {
        "key": "|CThe Nautilus - Berthing",
        "desc": "The area opens up into a somber chamber of slumber. Shadows cling like mourners to the edges where the timbers meet. A row of weathered bunks, each enshrouded by the gloom, forms a narrow gauntlet through which a timid soul must past. Upon an adjacent bunk lays a corpse, its countenance locked in an eternal repose of mystery and silence. The very air seems to thicken with the presence of death, as if it cradles the souls of the departed. Beside this funereal berth, a study chest rests.",
        "senses": {
            "feel": "A chill caresses the skin, born of the damp sea air and the unease that ebbs and flows with the ship's rocking.",
            "smell": "The pungent scent of salted wood mingles with a faint, unsettling sweetness of decay.",
            "sound": "The ship's timbers groan mournfully, a chorus underscored by the soft lapping of the waves against the hull.",
            "taste": "The damp air carries the taste of briny depths and the slightest trace of metallic tang, reminiscent of blood long spilled.",
        },
        "details": {
            "corpse": "Draped in a faded naval garb, the corpse lies with an outstretched arm, as though reaching for an unattainable salvation in its final moments.",
            "chest": "Crafted from oak, bound in iron, the chest possesses an aged patina; its curved lid hints at countless voyages endured, each scar and mar a silent testament to its history.",
        },
    },
    (2, 1): {
        "key": "|CThe Nautilus - Berthing",
        "desc": "Through a narrow passage, the eastern segment of the berthing area unfurls, gripped by the same morose atmosphere as its sullen counterparts. Here, a study table stands firm against the ship's ceaseless sway, steadfast as an anchor amidst the tumultuous sea. Upon its worn surface lie a lone tome, its pages yellowed with age, and a singular gem as black as the abyssal depths. The tome, left open, tells of days when the ship, billowed by stalwart winds, coursed through the waves with the zeal of a creature possessed. It speaks of the vessel's prowess in cleaving through the ocean's embrace, its hull slicing the froth with eager ferocity, a sharp contrast to the deathly stillness that now pervades.",
        "senses": {
            "feel": "A draft slinks in from a distant part of the ship, imbuing the air with a restless energy.",
            "smell": "An undertone of musty parchment from the book rises above the omnipresent odor of brine.",
            "sound": "Paper rustles as the book's pages stir, a quiet reminder of the world beyond the stillness.",
            "taste": "The air is laced with the staleness of neglect, yet beneath it lies an undercurrent of bygone adventures tasted in the salt of distant shores.",
        },
        "details": {
            "book": "Its leather-bound cover, embossed with maritime symbols, guards the knowledge within — stories of the ship, its crew, and the once-vivid life they shared.",
            "gem": "Opaque and inscrutable, the gem absorbs the dim light, holding within it an impenetrable darkness that seems to weigh heavy upon the soul.",
        },
    },
    (1, 2): {
        "key": "|CThe Nautilus - Map Room",
        "desc": "Beyond the berthing lies a once hallowed chamber now tainted with the unyielding grip of foreboding. At its heart, an aged chair cradles its penultimate occupant, a solitary figure grappling with the cruel precipice between life and death. With scalp mercilessly shorn, the exposed convolutions of a thinking organ lay bare. Gossamer strands of life still cling to the being, each breath a shallow echo in the oppressive silence. Charts and cartographic scrolls unfurled, this chamber turned charnel house once bore witness to fervent strategizing and dreams of distant lands.",
        "senses": {
            "feel": "A suffocating tension permeates the map room, laden with the apprehension of a truth too grim for daylight's reach.",
            "smell": "A coppery stench of fresh wounds and cerebral matter invades the nostrils with unsettling intimacy.",
            "sound": "A labored breath from the chair's occupant cuts through the stillness, each gasp a tragic cadence.",
            "taste": "The air tastes of iron and fear, an acrid flavor that tinges the tongue with the presence of imminent death.",
        },
    },
    (0, 2): {
        "key": "|CThe Nautilus - Map Room",
        "desc": "In the map room's eastern quarter, a labyrinth of celestial charts and oceanic plots adorns the walls. Centered beneath them, a tome lay open, bound in marbled leather with exquisite embossing. The volume seems to be set apart from its surroundings, an island amid a sea of cartographic endeavors. Within its opened page, depictions of humans with their fleeting fervor, elves with their timeless grace, dwarves with their unyielding forge-spirit, and more are captured in vivid detail. Each chapter weaves a cultural patchwork, a rich and diverse mosaic of lineage and custom. The histories within are penned with a meticulous touch, portraying victories and follies in equal measure.",
        "senses": {
            "feel": "Respect for the diverse tapestry of life is almost tangible, swelling within the room with each page turned.",
            "smell": "A hint of ink and parchment layers over the salty backdrop, an olfactory glimpse into the scholarly pursuit that birthed the volume.",
            "sound": "The air is gifted with the gentle rustle of paper, a whispering liaison between reader and the realm of lore inscribed across the pages.",
            "taste": "There's a subtle flavor to the air, as if one can taste the myriad climates and terrains spoken of within the tome, each page a new environment.",
        },
        "details": {
            "tome": "This volume, with each page scribed and illustrated with meticulous care, stands as a venerable envoy from a consortium of historians, dedicated to chronicling and celebrating the endeavors and wisdom of the land's multifarious inhabitants."
        },
    },
    (2, 2): {
        "key": "|CThe Nautilus - Map Room",
        "desc": "The map room's eastern expanse harbours a clutter of navigational instruments and parchments, yet amidst this trove of voyage and venture, a solitary tome commands attention. Resplendent with rich leather and clasps forged of aged bronze, the book nestled among the maritime relics with an enigmatic air, as if it harbors secrets far beyond the charting of stars and seas.",
        "senses": {
            "feel": "The air carries a dense weight of knowledge and history, silently observed by the arcane presence of the tome.",
            "smell": "A scent of dusty vellum and time-worn leather wafts from the book, redolent of ancient libraries and aged wisdom.",
            "sound": "A silence envelops the western quarter, punctuated only by the gentle creak of the tome's binding as it reveals its contents.",
            "taste": "Somehow, the air is tinged with the faintest hint of earth and toil, akin to the humble roots of the creatures detailed within the tome's bosom.",
        },
        "details": {
            "tome": "Bound by the hands of an erudite scholar, the book exudes a reverence for its subject, its scholars embarking on an odyssey of words to capture the essence of goblin-kind, in all their complexity and vibrancy."
        },
    },
    (1, 3): {
        "key": "|CThe Nautilus - Main Deck",
        "desc": "Upon emerging from the bowels of the ship, one is greeted by the vast expanse of the deck, a theatre of seafaring tales both jubilant and tragic. The ship herself, a grand old mariner, bears the scars and tales of a thousand leagues. Her masts, like the venerable arms of a stalwart sentinel, stretch toward the sky, the rigging singing with every push of the wind. Cannon ports, long silent, yawn like the mouths of some ancient leviathan, longing for the days when they spoke with thunder. At the helm, the wheel stands untouched, its timeworn surface wearing the prints of countless hands that guided this drifting citadel across the mercurial ocean. Barrels and crates huddle in the nooks, remnants of provisions and plunder, while the binnacle, with its compass, awaits a glance that can no longer navigate by its surety.|/|/    <morning>|#ffffffThe golden fingers of dawn trickle the edges of the horizon, spilling a soft, nascent glow upon the planks, where dew sparkles like a myriad of scattered diamonds,</morning><afternoon>|#f5deb3The sun reigns supreme, bequeathing a blaze of glory that gilds the sails and burnishes the wood with the hue of midday toil,</afternoon><evening>|#dda0ddTwilight caresses the deck, the sky a canvas of deep purples and soft pinks, the world holding its breath as day cedes to night,</evening><night>|xStars illuminate the heavens, the moon casting its ivory glow upon the vessel,</night> and the vast sea stretches into eternity.|n",
        "senses": {
            "feel": "The kiss of the sea breeze mingles with the warmth or chill of the surrounding air, embracing the skin with the timeless call of adventure.",
            "smell": "The scent of salt and tar pervades, a heady perfume of open waters and the essence of travel.",
            "sound": "Seagulls cry their harrowing songs as the ship creaks and groans, a symphony of maritime life and longing for the voyages of yesteryear.",
            "taste": "The air is laced with the brackish taste of sea spray, a reminder of the ocean's vast dominion and its enduring mysteries.",
        },
        "details": {
            "wheel": "Crafted from sturdy oak, the wheel's spokes bear the smooth patina of innumerable voyages, each turn a chapter in the ship's storied passage through the tempestuous embrace of the sea.",
            "cannons": "Each port gapes open, black and hollow, a fierce remembrance of battles fought, the iron scent of cannonballs long since silent within their darkened maws.",
            "ports": "Each port gapes open, black and hollow, a fierce remembrance of battles fought, the iron scent of cannonballs long since silent within their darkened maws.",
            "barrels": "Stacked haphazardly, these wooden vessels of sustenance and trade are banded with iron, their contents a mystery save for the occasional rat that scuttles from within, seeking refuge from the sea's infinite gaze.",
            "crates": "Stacked haphazardly, these wooden vessels of sustenance and trade are banded with iron, their contents a mystery save for the occasional rat that scuttles from within, seeking refuge from the sea's infinite gaze.",
            "binnacle": "The binnacle stands polished by the hands of time, its brass fixtures reflecting the dimming light, the compass within steadfast even as the ship around it succumbs to silence and despair.",
        },
    },
    (4, 3): {
        "key": "|CThe Nautilus - Prison Cells",
        "desc": "Descending into the belly of the ship, one finds the prison - an austere chamber that breathes an ancient sorrow. The air clings with the pungent odor of rust and confinement, and the groaning of wood above serves as a reminder of the freedom just out of reach. Cells, three iron monoliths, stand ominously. Within one iron grasp, a woman's spirit rebels against her shackles. Her limbs beat a desperate rhythm against her metal confines, each thud a sonnet of indignation and fierce will. On a nearby table lies a manuscript, its pages spread open as if gasping for breath, revealing a study of a brain and foretelling a century of darkness. Alongside the manuscript, an onyx gemstone throbs with an inexplicable energy, its polished surface absorbing rather than reflecting the dim glow that penetrates this forlorn space.",
        "senses": {
            "feel": "Dampness envelops the skin, a chill reminder of the encompassing sea and the isolation it imposes upon the ship's innards.",
            "smell": "The must of stagnation and the acrid sting of anxiety pervade, hanging heavily around the prisoners and their keep.",
            "sound": "Whispers of water dripping and the relentless thud of the trapped woman's struggle compose a somber dirge for confined souls.",
            "taste": "The air bestows a metallic milieu upon the tongue, seasoned with the bitterness of captivity and the tang of looming menace.",
        },
        "details": {
            "cells": "Sturdy and solemn, the cells have been forged with purpose, their unforgiving surfaces cold and relentless to the touch of their unwilling inhabitants.",
            "manuscript": "The manuscript, a tome of ominous knowledge, its leather cover worn by the touch of seekers and madmen, lies next to the jet-black gemstone, both custodians of darkened lore.",
        },
    },
    (4, 2): {},
    (4, 1): {},
    (3, 2): {},
    (3, 4): {},
}
