from evennia.utils import dedent

from world.zones.riverdale.object_prototypes import RIVERDALE_BOOK_WARRIOR

RIVERDALE_ROOMS = {
    (2, 0): {
        "prototype_parent": "xyz_room",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "key": "|#A9A9A9Riverdale - Ravine|n",
        "desc": dedent(
            """
            The ravine lies desolate beneath a heavy blanket of pallid snow, its craggy outcrops and jagged stones standing stark against the icy terrain. A thin, worn path meanders through the center, its dirt slick with frost, leading through the fractured earth like a faint scar. Sparse patches of hardy shrubs cling desperately to life among the rocks, their dull greens muted by the unrelenting cold. On either side, the rocks rise in irregular formations, towering and looming as though time itself has forgotten them. In this forsaken place, the silence is profound, broken only by the occasional sigh of the wind weaving through the barren landscape.
            """
        ),
        "senses": {
            "feel": "The cold bites into your skin, sharp and unforgiving, as if the very air were turned to brittle ice.",
            "smell": "The air carries a faint scent of damp earth, mixed with the crisp, metallic tinge of snow.",
            "sound": "The whisper of the wind is a ghostly echo, faintly stirring the silence as it rushes through the ravine.",
            "taste": "A dry, mineral bitterness lingers on your tongue, as though the dust of the ancient rocks has taken to the air.",
        },
        "details": {
            "rocks": "The jagged rocks rise in uneven clusters, their surfaces rough and cracked from ages of wear. Faint lines of frost cling to their crevices, shimmering faintly under what little light pierces the clouds.",
            "path": "The narrow path is uneven, worn by centuries of footfall, its surface hardened by frost. It twists and turns through the ravine like an old wound etched into the earth.",
            "shrubs": "These stunted shrubs are hardy survivors, their roots grasping at the rocky soil beneath the snow. Their dull green leaves are frostbitten, curling at the edges but stubbornly refusing to die.",
        },
    },
    (2, 1): {
        "prototype_parent": "xyz_room",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "key": "|#A9A9A9Riverdale - Ravine|n",
        "desc": "The ravine widens here, the frozen earth splitting into several narrow paths that wind between large boulders and patches of hardy scrub. The snow lies thinner on the ground, where it has been trampled by the feet of many travelers, leaving behind a patchwork of dirt and slush. The towering stones stand like silent sentinels, their weathered faces etched with the marks of time, casting long shadows across the pass. Sparse pines and shrubs dot the landscape, their branches drooping under the weight of frost, while to the north, the land rises once more into a ridge of rocky hills, promising yet more treacherous ground ahead.",
        "senses": {
            "feel": "The ground beneath your feet shifts unevenly, with patches of ice and slush making each step a cautious one.",
            "smell": "A faint but fresh scent of pine mixes with the cold air, mingling with the earthiness of damp stone.",
            "sound": "The wind gusts through the pass with a sharp whistle, rattling the stiffened branches of the sparse trees.",
            "taste": "The air is cold and sharp, tasting faintly of pine and dust.",
        },
        "details": {
            "boulders": "These massive stones are scattered across the pass, their surfaces chipped and worn. Flecks of ice cling to their sides, while patches of lichen creep along their bases.",
            "paths": "The forks in the road are narrow and uneven, each path winding around boulders and disappearing into the distance, their surfaces muddy where snow has melted underfoot.",
            "pines": "The few pine trees that have managed to grow here are stunted and frost-covered, their needles brittle under the weight of winter, yet they stand resilient against the biting wind.",
        },
    },
    (3, 1): {
        "prototype_parent": "xyz_room",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "key": "|#556B2FRiverdale - Forest Path|n",
        "desc": "The narrow path threads its way through a cluster of frost-laden pines, their dark branches reaching out like skeletal hands against the pale sky. The ground is uneven here, where gnarled roots break through the snow and stone, making each step precarious. Above, jagged cliffs rise on either side, hemming the forest in and trapping the cold air. Despite the thickening of the trees, the wind still howls through the gaps, carrying with it a biting chill. The forest floor is littered with broken branches and patches of icy moss, while the distant peaks loom ominously in the background, shrouded in mist.",
        "senses": {
            "feel": "The cold here feels sharper, amplified by the narrow confines of the trees and cliffs, as if the air itself were heavy and oppressive.",
            "smell": "The crisp scent of pine fills the air, mingling with the faint, earthy smell of damp wood and moss.",
            "sound": "The wind roars through the trees, rattling their branches as it snakes through the narrow pass.",
            "taste": "A faint taste of resin lingers in the cold air, mixed with the bitterness of pine needles.",
        },
        "details": {
            "trees": "The pine trees are thick with frost, their needles brittle and encrusted with ice. Some branches have broken off under the weight of the cold, lying scattered across the forest floor.",
            "cliffs": "The cliffs on either side of the path rise high and jagged, their dark stone marred with cracks and fissures. Here and there, patches of snow cling to the ledges, glistening faintly in the dim light.",
            "roots": "The roots of the trees twist through the ground, some bursting up from the earth in great, gnarled knots. They are slick with frost and treacherous to walk upon.",
        },
    },
    # TODO: Add something Warrior related here.
    (4, 1): {
        "prototype_parent": "xyz_room",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "key": "|#8B4513Riverdale - Cliffside Encampment|n",
        "desc": "Nestled against the base of a towering cliff, this small encampment offers a rare moment of respite amidst the unforgiving wilderness. A rough-hewn wooden platform supports a worn bedroll, laid out beside a few barrels and crates, the only signs of habitation in this isolated place. Above, icicles hang precariously from the cliff's edge, shimmering faintly in the campfire's glow. A crude spit juts from the fire, where something charred slowly roasts. The camp is sheltered from the wind, though the surrounding pines and jagged rocks loom nearby, ever a reminder of the untamed land just beyond the fire's warmth.",
        "senses": {
            "feel": "The warmth of the fire radiates through the air, a welcome change from the biting cold outside.",
            "smell": "The smoky scent of wood and roasting meat mingles with the sharpness of the cold air.",
            "sound": "The crackle of the fire and the occasional rustle of nearby trees create a rare sense of calm in the otherwise silent wilderness.",
            "taste": "The air is tinged with the savory aroma of roasting meat, its flavor faint on your tongue as the smoke drifts lazily around you.",
        },
        "details": {
            "bedroll": "The bedroll is a patchwork of rough animal hides, worn thin in places, but it offers enough warmth for a night's rest in the cold.",
            "crates": "The wooden crates are sturdy but show signs of age, their edges splintered from travel. One is slightly ajar, revealing basic supplies like dried meats and cloth.",
            "fire": "The fire crackles warmly, casting flickering shadows against the rock wall. A simple iron spit is suspended above it, where a small haunch of meat slowly roasts over the flame.",
        },
        "contents": [RIVERDALE_BOOK_WARRIOR],
    },
    (1, 1): {
        "prototype_parent": "xyz_room",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "key": "|#556B2FRiverdale - Verdant Hollow|n",
        "desc": "The landscape softens slightly here as the path curves into a hollow, where the barren rock gives way to patches of green. Small shrubs and tufts of grass push through the thin layer of snow, their vivid colors standing in contrast to the grey stones that litter the ground. The earth is uneven and soft underfoot, made damp by the trickling streams that weave through the area, fed by the melting snow from the higher cliffs. In the center of the hollow, a moss-covered boulder rises, its surface glistening faintly with dew. Despite the sparse vegetation, there's a wild, untamed beauty to the place, as if nature itself is reclaiming the land from the grip of winter.",
        "senses": {
            "feel": "The ground feels softer here, giving slightly underfoot as the earth is damp from melted snow.",
            "smell": "A fresh, earthy scent fills the air, mingling with the faint aroma of moss and damp stone.",
            "sound": "The faint trickle of water can be heard, as small streams wind their way through the hollow.",
            "taste": "The air is moist, carrying the subtle taste of wet earth and moss.",
        },
        "details": {
            "shrubs": "The shrubs here are more vibrant, their leaves a deep green, standing in stark contrast to the grey rocks and sparse snow surrounding them.",
            "boulder": "The moss-covered boulder is large and rounded, its surface soft to the touch and slick with moisture. The moss glows faintly with a vibrant green, thriving in this sheltered space.",
            "streams": "Small streams meander through the hollow, their clear waters trickling over smooth stones and collecting in shallow pools. The sound of their flow adds a peaceful murmur to the quiet surroundings.",
        },
    },
    # TODO: Add a bandit here.
    (0, 1): {
        "prototype_parent": "xyz_room",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "key": "|#8B7765Riverdale - Forest Hideaway|n",
        "desc": "Tucked among the towering pines, this small encampment offers the barest essentials for survival. A crude tent, made of stretched hides and supported by worn wooden poles, stands as the sole refuge from the wilderness. Inside, a patchwork bedroll lies on the ground, accompanied by a simple wooden table holding a lantern, a well-worn book, and a tarnished tin cup. The air is thick with the scent of pine, and the forest floor beneath the tent is covered in dry grass and scattered leaves, offering little comfort but a necessary reprieve from the cold, hard earth outside.",
        "senses": {
            "feel": "The air is cool but still, offering a brief respite from the harsher winds of the wilderness beyond the tent.",
            "smell": "The thick scent of pine dominates, mingling with the musty odor of the animal hide tent.",
            "sound": "The soft rustling of trees and distant calls of birds blend with the occasional creak of wood from the makeshift shelter.",
            "taste": "The taste of damp earth lingers faintly in the air, with a slight tang of rust from the tin cup.",
        },
        "details": {
            "tent": "The tent is made from patched animal hides, stitched together and stretched tightly over crooked wooden poles. It offers minimal shelter but shields from the wind.",
            "table": "The small wooden table is crudely fashioned, its surface rough and splintered. A lantern, half-full of oil, and a tin cup rest on it, along with a worn, leather-bound book.",
            "bedroll": "The bedroll is a simple affair, made from stitched-together animal hides. Its surface is rough and thin, offering little comfort against the forest floor beneath.",
        },
    },
    (1, 3): {
        "prototype_parent": "xyz_room",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "key": "|#A9A9A9Riverdale - Rocky Pass|n",
        "desc": "The path narrows as it winds between towering stone formations, their jagged surfaces rising like ancient sentinels on either side. The ground beneath is uneven, strewn with loose rocks and pebbles, forcing careful footing. Sparse patches of wiry grass and stubborn shrubs cling to the cracks in the stone, thriving despite the harsh conditions. The pass is quiet, save for the occasional clatter of a loose rock tumbling down the cliffs. The air feels thinner here, with the high stone walls blocking out much of the light, casting long, creeping shadows over the rocky trail.",
        "senses": {
            "feel": "The ground beneath your feet is rough and uneven, with loose stones shifting underfoot at every step.",
            "smell": "The air is dry and carries the faint scent of dust and stone, with just a hint of fresh grass carried on the breeze.",
            "sound": "The faint sound of rocks tumbling down the cliffs echoes eerily in the stillness of the pass.",
            "taste": "A dry, gritty taste clings to the back of your throat, a mixture of dust and cold air.",
        },
        "details": {
            "stones": "The stones scattered across the pass vary in size, from small pebbles to larger chunks of rock, their surfaces rough and jagged.",
            "shrubs": "The small shrubs that grow here are tough and resilient, with spindly branches and deep green leaves that seem to defy the rocky terrain.",
            "cliffs": "The cliffs rise sharply on either side of the pass, their craggy surfaces marked by deep cracks and worn edges, as if shaped by countless years of wind and erosion.",
        },
    },
    # TODO: Figure out what to do here.
    (0, 3): {
        "prototype_parent": "xyz_room",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "key": "|#708090Riverdale - Ancient Stone Circle|n",
        "desc": "Perched atop a rocky outcrop, three weathered stone pillars stand in solemn silence, their surfaces etched with faded runes that speak of an ancient, forgotten time. The ground beneath is cracked and uneven, with gnarled tree roots winding around the base of the stones as if nature itself seeks to reclaim this sacred site. Beyond the circle, the forest stretches out in all directions, the distant glimmer of a lake just visible through the trees. The air here is thick with an uncanny stillness, as if the very land remembers the rituals once performed in the shadow of these monoliths.",
        "senses": {
            "feel": "The stone beneath your feet is cool and smooth, while a faint tingle of energy lingers in the air, as if something unseen watches from the ancient stones.",
            "smell": "A faint scent of moss and damp stone mingles with the fresh, earthy aroma of the forest beyond.",
            "sound": "The wind whispers softly through the pillars, a low and haunting sound that seems to carry the echoes of long-forgotten words.",
            "taste": "The air tastes clean and sharp, with a faint hint of minerals from the weathered stone.",
        },
        "details": {
            "pillars": "The three stone pillars are each marked with faded, timeworn runes, their surfaces rough with age. Though weathered, the stones seem imbued with an ancient power, and a faint hum can be felt when standing near them.",
            "roots": "Gnarled roots snake around the base of the stones, their tendrils thick and twisted, as if they are slowly reclaiming the ancient site for the forest.",
            "view": "From this elevated vantage point, the forest stretches out in a sea of green, with a distant lake shimmering in the sunlight beyond the trees.",
        },
    },
    (2, 3): {
        "prototype_parent": "xyz_room",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "key": "|#4682B4Riverdale - Riverbend|n",
        "desc": "The path hugs the edge of a deep gorge where the river rushes by, its blue waters churning over rocks and tumbling into a cascading waterfall. The sound of the water is a constant, soothing roar, echoing off the cliffs that line the gorge. The ground here is slick with spray, and the rocky path is treacherous underfoot, with loose stones threatening to tumble into the frothing water below. Sparse vegetation clings to the sides of the gorge - small shrubs and patches of grass that have found a foothold in the craggy terrain. The air is cool and fresh, filled with the scent of river spray and the distant sound of birds calling from the forest beyond.",
        "senses": {
            "feel": "The air is cool and damp, with mist from the waterfall clinging to your skin and making the rocks slick beneath your feet.",
            "smell": "The fresh scent of the river fills your lungs, tinged with the earthy aroma of wet stone and moss.",
            "sound": "The roaring sound of the waterfall dominates, with the occasional chirp of birds piercing through the steady rush of water.",
            "taste": "The cool air carries the clean, crisp taste of fresh water, mixed with the faint mineral tang of stone.",
        },
        "details": {
            "waterfall": "The waterfall cascades down the rocks in a frothy rush, its waters sparkling in the light as it crashes into the pool below.",
            "path": "The path is narrow and uneven, with loose rocks scattered across its surface. It runs perilously close to the edge of the gorge, where the river roars just below.",
            "vegetation": "Small shrubs and patches of grass grow stubbornly along the edge of the gorge, their roots buried deep in the cracks between the rocks.",
        },
    },
    # TODO: Add bandit warning to go away.
    (2, 2): {
        "prototype_parent": "xyz_room",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "key": "|#B22222Riverdale - Ember Mine Entrance|n",
        "desc": "The entrance to Ember Mine looms ahead, carved roughly into the rock face and framed by thick wooden beams that seem barely capable of holding back the weight of the stone above. Scattered crates and barrels, weathered and worn, litter the ground near the entrance, alongside broken tools and heaps of debris. A makeshift wooden gate stands ajar, its hinges creaking faintly in the breeze. Beyond the threshold, the dark mouth of the mine beckons. The air here is thick with dust, and the occasional sound of distant clattering echoes from deep within the mine.",
        "senses": {
            "feel": "The air is dry and heavy, carrying the grit of dust with every breeze, as if the land itself clings to the remnants of hard labor.",
            "smell": "A faint metallic tang mingles with the scent of old wood and damp earth, a testament to the mine's long-forgotten past.",
            "sound": "The creak of wooden beams and the occasional clatter of loose stones create an uneasy silence, broken only by the distant drip of water echoing from deep within the mine.",
            "taste": "The taste of dust is thick in the air, dry and gritty, with the faintest hint of iron.",
        },
        "details": {
            "entrance": "The mine's entrance is framed by rough-hewn wooden beams, their surfaces splintered and weathered by time and the elements. A small gate, made of crude planks, stands partially open, inviting any who dare to venture inside.",
            "crates": "The crates near the entrance are old and falling apart, filled with discarded tools and remnants of past mining efforts. The wood is splintered and worn, covered in a thin layer of dust.",
            "shadows": "The darkness within the mine is thick and impenetrable from the outside, offering no clue as to what dangers—or treasures—lie within its depths.",
        },
    },
}
