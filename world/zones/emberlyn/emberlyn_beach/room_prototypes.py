# from evennia.utils import dedent
from world.zones.emberlyn.emberlyn_beach import object_prototypes

EMBERLYN_BEACH_ROOMS = {
    (0, 0): {
        "key": "|#C7B299Emberlyn Shore|n",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "desc": "The ground beneath your feet transitions from packed, pale sand into a treacherous mire, where slick mud eagerly clings with every step. Dark, stagnant waters stretch out like an inkblot across the landscape, merging with patches of spindly reeds and moss-covered stones. Here and there, the bones of long-forgotten vessels and bleached driftwood lie half-buried in the muck, remnants of a time when this shore was less forsaken. Above, the sky hangs low and gray, casting a pall over the dismal scene, while the breeze carries with it the damp, heavy scent of decay.",
        "senses": {
            "feel": "The air is thick with humidity, and your skin prickles with the moisture that clings to it.",
            "smell": "A potent mix of rotting vegetation and briny water fills the air.",
            "sound": "The soft sucking of mud underfoot is interrupted only by the distant croak of frogs and the occasional splash of unseen creatures.",
            "taste": "A faint bitterness lingers on your tongue, as though the air itself were saturated with the essence of the brackish water.",
        },
        "details": {
            "mud": "The mud is thick, nearly swallowing your boots with each step. It is dark, almost black, and streaked with veins of pale sand.",
            "driftwood": "Twisted, sun-bleached logs lie scattered, half-buried in the muck, their shapes distorted by time and decay.",
            "bones": "The skeletal remains of boats long forgotten jut out from the mire, their frames splintered and warped, speaking of past storms or ill-fated voyages.",
        },
    },
    (0, 1): {
        "key": "|#C7B299Emberlyn Shore|n",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "desc": "Before you stretches a wide, desolate expanse of pale, ashen ground, its surface marred by cracks and jagged, uneven patches of hardened earth. The soil here is chalky and dry, crumbling beneath your feet as you step forward. Scattered throughout the expanse are patches of darkened, charred earth, as though some ancient fire had ravaged the land long ago. Faint trails of soot meander between the lighter stretches, marking the passage of long-gone winds. To the south, the land gives way to the darker, treacherous shores, while to the north, the land rises slightly, the pale dust blending into distant, rocky hills.",
        "senses": {
            "feel": "The ground feels brittle and fragile beneath your feet, as if it might give way at any moment.",
            "smell": "The air is dry, carrying a faint, acrid scent of burnt earth and old fires.",
            "sound": "A deep, eerie silence pervades the area, broken only by the occasional whisper of wind stirring the fine, ashen dust.",
            "taste": "The dryness of the air makes your throat parched, with the faintest hint of something bitter and metallic lingering on your tongue.",
        },
        "details": {
            "ash": "The pale ground is covered in a fine layer of ash, so light it stirs with the slightest breeze, leaving thin trails in its wake.",
            "charred earth": "Scattered patches of dark, charred ground dot the landscape, their edges hardened and blackened as though scorched by some long-forgotten fire.",
            "soot trails": "Thin trails of soot snake across the ground, barely discernible amidst the pale surroundings, marking the ghostly remnants of winds that once swept through here.",
        },
    },
    (0, 2): {
        "key": "|#C7B299Emberlyn Shore|n",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "desc": "A wide plain of broken earth stretches out before you, the once-solid ground now fractured into jagged slabs and patches of pale, dusty sand. Scattered rocks of varying sizes lie embedded in the soil, their rough surfaces worn smooth by the elements. The light earth here is bleached and speckled with the remnants of past floods, clinging to patches of stone that offer no refuge. Along the edges of the plain, larger boulders loom like silent sentinels, casting long shadows. To the south, the ashen ground recedes.",
        "senses": {
            "feel": "The wind cuts across the plain, stirring the dust and leaving your skin dry and parched.",
            "smell": "There's a faint smell of sunbaked rock and dry soil, laced with the scent of old mineral deposits.",
            "sound": "The dry rasp of the wind across the fractured ground is punctuated by the occasional clatter of loose stones.",
            "taste": "The air is dusty and dry, with a hint of salt on the breeze, as though the land remembers ancient seas.",
        },
        "details": {
            "fractured earth": "The ground is split into irregular slabs and crevices, each crack a testament to the shifting of the land beneath.",
            "scattered rocks": "The rocks here vary in size, some no larger than pebbles, while others stand like forgotten monuments. They are smooth and pale, weathered by time.",
            "boulders": "The larger boulders that ring the plain are dark and imposing, their rough surfaces cracked and pitted, as though once caught in the grip of a great force.",
        },
    },
    (1, 2): {
        "key": "|#C7B299Emberlyn Shore|n",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "desc": "A towering bluff of fractured stone dominates the eastern landscape, its jagged face worn smooth in places by wind and time. The pale sand of the surrounding plain thins as it meets the bluff, giving way to clusters of boulders and hardy vegetation clinging to the cracks. The stone itself, mottled with shades of brown and ochre, rises steeply from the earth, while the shadows cast by the bluff deepen the greenish hue of the stagnant waters that pool nearby. At the base of the bluff, remnants of old stone formations seem half-consumed by the landscape, while a faint path of worn earth traces the contours of the terrain.",
        "senses": {
            "feel": "The air is cooler near the bluff, carrying the dampness from the waters nearby.",
            "smell": "A faint scent of wet stone and earthy moss drifts from the bluff.",
            "sound": "The occasional drip of water from the bluff echoes softly, mixing with the rustle of dry grass.",
            "taste": "The air tastes faintly mineral, like stone after a fresh rain.",
        },
        "details": {
            "bluff face": "The bluff is split and weathered, its surface streaked with bands of brown and ochre, giving the stone a marbled appearance.",
            "boulders": "Scattered boulders, large and irregular, sit at the base of the bluff. They are covered in moss and lichen, their rough surfaces contrasting with the smooth patches of the bluff.",
            "stagnant waters": "Dark, still waters pool near the base of the bluff, their surfaces almost opaque with algae and sediment, giving them a greenish tint.",
        },
    },
    (1, 3): {
        "key": "|#4A766EEmberlyn Shore - Splintered Pier|n",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "desc": "A rickety, weather-beaten pier stretches out across the murky waters, its wood warped and bleached by years of exposure to the elements. The planks, unevenly spaced and broken in places, creak under the slightest pressure. Moss and algae cling to the timbers, making the surface slick with moisture. Beneath the pier, the green waters swirl lazily, dark and opaque, concealing whatever lies below. Rusted remnants of once-sturdy beams poke through the water's surface, while fragments of old ropes and decayed nets dangle from the edge, swaying gently in the breeze. The air around the pier feels damp and thick, saturated with the scent of brine and decay.",
        "senses": {
            "feel": "The pier sways slightly with each step, the wood beneath your feet cold and damp.",
            "smell": "A sharp, briny smell rises from the water, mixed with the pungent odor of rotting wood.",
            "sound": "The soft lapping of water against the pier is interrupted by the occasional groan of the wood shifting in the wind.",
            "taste": "The air carries a salty tang, with a hint of damp, rotting wood lingering on the back of your tongue.",
        },
        "details": {
            "pier planks": "The planks of the pier are rough and splintered, many of them worn down by the relentless erosion of water and time. Some are cracked, revealing the dark, damp understructure beneath.",
            "ropes and nets": "Old, frayed ropes dangle over the sides of the pier, remnants of a time when this structure saw regular use. The nets that remain are brittle and crumbling, tangled beyond use.",
            "water": "The water beneath the pier is dark and stagnant, its surface covered in patches of algae that ripple slightly with the breeze, concealing any movement below.",
        },
        "objects": [object_prototypes.EMBERLYN_SHORE_HYMNS],
    },
    (0, 3): {
        "key": "|#C7B299Emberlyn Shore|n",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "desc": "A shallow depression in the landscape opens up here, its pale, powdery sand giving the area a muted, almost ghostly appearance. Scattered stones and tufts of stubborn grass dot the edges of the hollow, breaking up the otherwise barren expanse. At its center lies a large, stagnant puddle, its surface a cloudy blue, reflecting little more than the overcast sky above. The sand near the water's edge is damp and compact, gradually giving way to the softer, drier sands further out. Jagged roots from nearby trees stretch into the hollow, their tendrils winding through the soil as though reaching for the elusive moisture.",
        "senses": {
            "feel": "The sand shifts underfoot, alternately soft and damp near the water, then dry and powdery farther away.",
            "smell": "A faintly earthy scent mixes with the sterile smell of stagnant water.",
            "sound": "The hollow is eerily silent, save for the occasional distant drip of water from the roots into the puddle.",
            "taste": "The air is tasteless, devoid of any strong character, save for the slight hint of dampness.",
        },
        "details": {
            "puddle": "The puddle at the center is a murky blue, its still surface unbroken and opaque, offering no glimpse of its depth.",
            "roots": "Long, jagged tree roots snake into the hollow, their gnarled surfaces weathered and gray. They claw at the ground, twisting into the soil as if searching for sustenance.",
            "sand": "The sand here is a dull, off-white, fine and powdery in some areas, while compacted and darker near the water's edge.",
        },
    },
    (0, 4): {
        "key": "|#C7B299Emberlyn Shore|n",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "desc": "The ground here dips into a shallow basin, its surface scoured smooth by the relentless passage of wind and time. Pale sand collects in the hollow, broken only by patches of coarse gravel and a few larger stones strewn haphazardly across the ground. The edges of the basin are lined with dark, jagged rocks, creating a stark contrast with the pale interior. Though the area is largely barren, a faint green tinge along the far edge hints at the resilience of life, with sparse grasses clinging to the inhospitable soil. To the east, the land slopes upward, leading away from this wind-swept hollow.",
        "senses": {
            "feel": "The sand is cool to the touch, though the wind across the basin feels harsh and biting.",
            "smell": "A faint mineral scent rises from the rocky ground, blending with the dryness of the sand.",
            "sound": "The wind howls softly across the basin, stirring up faint whispers of sand in its wake.",
            "taste": "The air is dry and gritty, carrying a subtle hint of salt and dust.",
        },
        "details": {
            "rocks": "Jagged and dark, the rocks lining the basin's edge are sharp and unyielding, standing in stark contrast to the pale, smooth sand.",
            "gravel": "Small patches of gravel break up the expanse of sand, their dark color marking them as outliers in the otherwise light terrain.",
            "grass": "Sparse and hardy, the grasses that cling to the edge of the basin are pale green, their blades thin and wiry, bent low by the persistent wind.",
        },
    },
    (0, 5): {
        "key": "|#C7B299Emberlyn Shore|n",
        "typeclass": "world.xyzgrid.xyzroom.XYZRoom",
        "desc": "This narrow pass winds between steep, uneven walls of weathered stone, the path beneath your feet a mixture of pale sand and scattered rocks. Along the edges of the trail, mergrass grows in sparse clusters, its long, silvery strands swaying softly in the breeze. The soft glint of dark, violet-hued belladonna berries can be seen nestled among the rocks, their leaves thick and waxy, thriving in the shaded crevices where the light barely reaches. Overhead, a stone arch marks the pass's northern exit, its ancient surface smoothed by years of erosion. The atmosphere here is one of quiet desolation, the landscape seemingly untouched by time.",
        "senses": {
            "feel": "The air is still and cool, with a faint breeze stirring the mergrass at your feet.",
            "smell": "A faint, sweet fragrance rises from the belladonna, mingling with the earthiness of the stone and sand.",
            "sound": "The sound of wind through the narrow pass is low and constant, broken only by the soft rustle of mergrass.",
            "taste": "A subtle bitterness lingers in the air, carried on the breeze along with the faint sweetness of the belladonna.",
        },
        "details": {
            "mergrass": "The mergrass grows in tall, silvery tufts, its delicate blades swaying like strands of fine silk, giving the area an ethereal quality.",
            "belladonna": "Clusters of belladonna thrive in the shaded crevices, their dark, glossy leaves cradling violet-black berries that gleam ominously in the dim light.",
            "stone arch": "The stone arch spans the pass, its surface smooth and ancient, worn down by time yet still standing as a silent sentinel marking the way forward.",
        },
    },
}
