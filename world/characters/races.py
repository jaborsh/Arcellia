from class_registry import ClassRegistry

RaceRegistry = ClassRegistry("race")

RACE_INFO_DICT = {
    "human": "|YHumans|n:\n\nThey are creatures of passion and paradox, canvases of immeasurable depth painted with the vibrant hues of their experiences. In their eyes, one finds the glimmer of stars they have yet to chart, and in the steady rhythm of their hearts, the beat of the ancient drums that have long echoed through the corridors of time. Bound to the wheel of progress, humans traverse the breadth of their realm with insatiable curiosity. They are builders and dreamers, forging empires from the raw materials of nature, etching their histories into the stones of the world. With hands capable of both creation and destruction, they mold their destinies, leaving the legacies of their triumphs and tragedies. Amongst them walk the valiant and the villainous, a spectrum of souls whose choices thread the fine line between heroism and infamy. Love is their greatest strength, and it is love that can be their undoing - such are the stark contrasts that define them. Every smile and tear, a note in the human spirit.",  # noqa: E501
    "elf": "|YElves|n:\n\nTall and regal, draped in the elegance of their rich culture, elves move with a grace that belies their formidable strength. Their features, sharp and delicately crafted, mirror the beauty of their surroundings, where each leaf and bud thrives under their tender care. Eyes that sparkle with the wisdom of ages seem to pierce through the veils of time, beholding the mysteries that lie hidden to the more fleeting gazes of other beings. Bound by ancient traditions and an unwavering respect for the balance of nature, these denizens cultivate a deep-seated magic that breathes in harmony with the world. The natural arcane is their companions, a silent dialogue that has stretched unbroken since the dawn of time. In their hands, spells weave seamlessly, and the pulse of the land resonates through their songs and storied craftwork which reflects both the beauty of the natural world and the depth of their reverence for it.",  # noqa: E501
    "dwarf": "|YDwarves|n:\n\nDeep in the bosom of Arcellia's mountains and hills, the dwarves carve their legacy into the very bones of the earth. These stout and stalwart folk are the unyielding stone of the fantasy realm, enduring as the crags they call home. With sinew and steel, they sculpt their existence from the rock, delving into the heart of the world to unearth its secrets and riches. Beneath a firmament of stone, in halls wrought by their own hands, the dwarves' society thrives. Their cities are marvels of engineering and craftsmanship, illuminated by the radiant glow of forge and gemstone. Their connection to the earth is palpable, a deep resonance with the ore and stone that forms the foundation of their culture. In every etched rune and every chiseled hallway, the narrative of their people echoes - a saga of determination and toil.",  # noqa: E501
    "gnome": "|YGnomes|n:\n\nTucked away in the nooks and crannies of Arcellia, where the hidden corners of the world converge in a mosaic of shadow and light, the gnomes thrive with keen curiosity and inventive wit. These diminutive denizens are the embodiment of the earth's quieter whispers - the rustle of fallen leaves, the secrets of the stones, and the murmurs of burrowing roots. Gnomes are a people of intricate detail and profound connection to the subtler aspects of the natural world. Standing no taller than a young sapling, they navigate their surroundings with an inherent agility and grace. Their eyes are pools of profound observation, gleaming with the spark of discovery and the steady gaze of those who understand the value of patience and precision. In the heart of their burrowed communities, gnomes foster a culture rich with tradition yet ever-evolving, a society that cherishes the old ways whilst seeking new understandings. Their homes are often hidden within hillocks or beneath the roots of ancient trees, doorways that lead to warrens of warmth and the glow of hearth fires.",  # noqa: E501
    "nymph": "|YNymphs|n:\n\nNymphs grace the woodlands and waters with a presence that is as gentle as it is pervasive, their very beings intertwined with the life force of the natural world they inhabit. They dance in the dappled sunlight that filters through the leaves and in the reflective surfaces of serene lakes and babbling brooks. In their movements, there is a poetry that speaks of the synchrony of all living things, a symphony conducted by the rustle of leaves and the lapping of waves. Elusive and enchanting, the nymphs exhibit a beauty that transcends the physical form. They are the sons and daughters of the elements, each bearing the features and essence of the domain they embody.",  # noqa: E501
    "orc": "|YOrcs|n:\n\nOrcs carry upon their broad shoulders and sinewy frames an air of indomitable strength, their features as hard as the craggy landscapes from which they hail. Skin hewn in hues that echo the varied earth - greens, grays, and tans; their visages are adorned with the scars of battles past and the ancestral tattoos that tell the story of their lineage. Eyes like smoldering coals burn with the intensity of their warrior souls, ever vigilant and ever unyielding. Their societies are built upon the unforgiving bedrock of survival, where might and merit shape the forge of hierarchy. In the orcish tribes, a chieftain's rule is won through prowess in combat and the ability to lead with both ferocity and wisdom. They are understanding of nature's cruel impartiality and embrace a life where honor is earned and strength revered.",  # noqa: E501
    "pyreling": "|YPyrelings|n:\n\nIn their aspect, pyrelings are a curious sight: small in stature but filled with an intensity that belies their size. Their skin is a canvas of hellish tones, echoing the colors of a sunset ablaze or the glow of coals in a smith's forge. They embody the dance of flames, their movements imbued with an energetic vibrancy that leaves a trail of warmth in the air. They reside in realms touched by the earth's inner burn, within volcanic ranges or scorched plains where geysers release their steam in skyward columns. The pyrelings are at one with these places of primordial power, their homes nestled close to the nurturing flame, amidst rivers of molten rock and mountains breathing ash.",  # noqa: E501
}

SUBRACE_INFO_DICT = {
    "elf": {
        "high": "|YHigh Elves|n:\n\nThe High Elves stand with a luminous distinction, their nobility carved from the highest peaks and the purest streams. Lithe and statuesque, their bearing speaks of an ancestry mingled with the very essence of majesty. Their eyes, often clear pools of sapphire and emerald, gleam with a brilliance that spills forth the secrets of a higher understanding, a splendor birthed in the loftiest alcoves of wisdom. High Elves navigate their existence with a solemnity reserved for those who have drunk deeply from the chalice of arcane knowledge. Their spires pierce the heavens, gleaming citadels of crystalline elegance that reflect the grandiosity of their visions. A lineage steeped in the pursuit of excellence, the High Elves dedicate their ageless lives to perfecting their art with the patience of the stars.",  # noqa: E501
        "night": "|YNight Elves|n:\n\nVeiled in the penumbral depths, where light dares not linger, dwell the largest gatherings of Night Elves, shrouded in the intrigue as thick as the shadows they adore. Slender and seductive, their forms are draped in the subterfuge of midnight, a stark contrast to their fairer kin bathed in the daylight's favor. Their features, hauntingly alluring, are etched with a subtle menace, as if they were chiseled from the darker, untamed aspects of the natural world. Their eyes, usually dark as onyx orbs, glint with the cold fire of the under-realm, reflecting an inner flame forged in the crucible of ancient grudges and deep-seated enmity. Sanctuaries of twisted spires and arachnid elegance sprawl beneath the surface, defiant monuments to their enduring spite for the radiance of the high-born. Here they master forbidden magic, seeking to one day estrange their kin.",
        "wood": "|YWood Elves|n:\n\nTheir countenances, kissed by the dappling light of their leafy sanctuaries, bear the serene beauty of the arboreal lands they protect. Eyes the shade of fresh foliage and rich earth behold the world with a quiet knowing. Their sanctuaries, hidden amongst the great oaks and pines, embody the harmonious marriage between nature and those who revere it with a pure, uncomplicated devotion. Wood Elves embrace the ebb and flow of the natural cycle, their temperament as even as the seasons' transitions. They are the balancers, the keepers of the gentle equilibrium that sustains the pulsating heart of the woodland. Untouched by the stratifications of their high-born counterparts, uninterested in the politics of the darker kin, the Wood Elves nurture a world apart.",  # noqa: E501
    },
    "dwarf": {
        "emberheart": "|YEmberheart Dwarves|n:\n\nDeep within the fiery bowels of the earth, where rivers of molten rock etch luminescent veins through the darkness, the Emberheart Dwarves toil. Their sturdy forms are as unyielding as the ancient stone from which they hew their legacy, and their spirits burn as bright as the forge-fires they have mastered. Their hands, calloused and sure, are the instruments of unparalleled artistry, sculpting the very essence of the mountains into shapes both intricate and enduring. Reverence for tradition fuels their daily rites, each hammer strike and chisel chip a ceremony in homage to the earth that cradles them. Their celebrations are raucous, yet honor-bound, rich with the resonant anthems of their people and the clangorous symphony of metal against anvil. They rejoice in their labor, for each masterpiece is not merely a work of craft but a hallowed offering to the elements that have long shaped their destiny.",  # noqa: E501
        "ironvein": "|YIronvein Dwarves|n:\n\nIn the deep, resonating chambers where the arcane pulses through the very bedrock, the Ironvein Dwarves carve their existence. Their robust silhouettes are hewn from the same unbreakable mineral that surrounds them, their resolve as steadfast as the ore-rich veins they mine. The iron in their souls resonates with the raw magic that suffuses their subterranean home, a harmonic convergence of might and mysticism. The Ironvein Dwarves are the confluence of brawn and arcane intellect. Their forges sing not merely with the clangor of metalwork but with the murmurs of spells that weave into the very fabric of their creations. Here, weaponry and armor are not just forged; they are born of elemental rituals, each piece a repository for the latent powers that the Ironvein wield with a casual, practiced deftness. Their society is a crucible for the mystical arts, balanced by the pragmatism of the hammer and tongs. The chants of their ancient rune-smiths fill the air. Though their craftsmanship bears the weighty substance of iron, it also hums with the subtle song of the arcane, a craft that wields spell and steel with equal adroitness.",  # noqa: E501
        "stoneguard": "|YStoneguard Dwarves|n:\n\nAmidst the echoes of a grandeur now lost, the Stoneguard Dwarves stand vigilant, the vestiges of their once-mighty dominion etched into the furrows of their brow. Hardened by loss and tempered by the relentless assault of memory, their sturdy figures are as unmovable as the mountains that bear witness to their unending resolve. They reside close to the bones of the earth, where vestiges of their former halls whisper to them of glory and sovereignty usurped. Cynicism laces their speech like veins of flint within rock, yet it does not dampen the fire of their courage or the edge of their steely determination. Every Stoneguard Dwarf is a living embodiment of their unbroken lineage. Within the embittered hearts of the Stoneguard Dwarves, there flickers an undiminishable flame of reclamation, a boundless drive that will one day see them restore the sanctity of their birthright. It is this inexorable yearning that clenches their fists, fortifies their will, and steels them against the specter of oblivion. Through trials untold and the passage of innumerable moons, they endure - a people of stone and iron, unyielding in their sacred quest to reclaim the revered halls of their ancestors from the clutches of darkness.",  # noqa: E501
    },
    "gnome": {
        "dusk": "|YDusk Gnomes|n:\n\nThe Dusk Gnomes are the poets of the gloaming, their culture a reflection of the intermediary world they cherish: a blend of the seen and the unseen, the known and the mysterious. They revere the subtleties of change, the nuance of transition that their very essence embodies. Their arts and magic weave through the moonlit hours like the soft droplets of dew, each one a glistening mimicry of their mastery over the elements of twilight. Secluded from the full gaze of Arcellia, the Dusk Gnomes cultivate an enigmatic aura, their very lives a ritual dedicated to the moment when daylight fades and the first star whispers its greeting. It is in this serene interlude they find their strength and their inspiration - a people eternally suspended in the beauty of the world's softest sigh, the enchanting ephemeral hour of dusk.",  # noqa: E501
        "hearth": "|YHearth Gnomes|n:\n\nWhere the warmth of the hearth fire crackles and innovation sparks to life, Hearth Gnomes flourish amidst invention and clever design. These artisans of the domestic and the practical are the quintessence of gnomish ingenuity, their lives intertwined with the joyous clatter of gears and the satisfied hum of well-oiled mechanisms. They stand as the embodiment of resourceful craftsmanship, their small statures belying the grandeur of their creative ambition. Their hands, ever busy and dexterous, deftly manipulate the materials of their trade, fashioning inventions as whimsical as they are functional. The twinkle in their lively eyes mirrors the flicker of flames against polished brass and sheer ingenuity. In their cozy subterranean abodes or snug treetop lofts, every nook bristles with the evidence of their inventive spirit: clockwork contraptions and steam-driven wonders that speak of a mind ever churning with the next great inspiration.",  # noqa: E501
        "sylvan": "|YSylvan Gnomes|n:\n\nLithe and lively, Sylvan Gnomes possess an almost ethereal grace that allows them to flit through the underbrush with scarcely a sound, their delicate footfalls leaving but the lightest imprint upon the mossy earth. Their eyes, bright and shimmering like sunlit dew upon a spider's web, hold the lively spark of nature's capriciousness. With an irrepressible zest for life, they embody the untamed whimsy of Arcellia's woodlands. Sylvan Gnomes revel in the intricate wonders of the natural world, their every endeavor infused with the joy of spontaneous creation. They are the artisans of the organic, shaping the flora and crafting from the materials gifted by the woods in a seamless blend of utility and aesthetics. Their stealth and subtlety are matched only by their connection to the myriad creatures that rustle and roam amidst the undergrowth.",  # noqa: E501
    },
    "pyreling": {
        "arcanist": "|YArcanist Pyrelings|n:\n\nWhere the fervor of flame and the enigma of the arcane entwine, the Arcanist Pyrelings conduct their mysteries. These Pyrelings stand at the crossroads of fire and magic, their presence an alchemical reaction that defies simple elements. The hues that adorn their skin are not just the colors of burning horizons but also the gleaming spectra of magic at its most primal and untamed. Their diminutive forms are deceptively slight against the grandeur of their power, their stature in striking contrast to the vastness of the energies they channel. The Arcanist Pyrelings carry the dual legacy of their native flames and the intricate weavings of raw magical forces, their gestures sparking both embers and enigmatic sigils into the charmed air around them. Devotees of a craft both ancient and ever-burning, they shape spellcraft as one might forge steel, tempering and bending it to their indomitable wills. Their artifacts are not mere baubles but complex repositories of transcendent energy, each object a nexus of fire's passion and magic's boundless possibility.",  # noqa: E501
        "emberkin": "|YEmberkin Pyrelings|n:\n\nSmall they may be, yet each Emberkin carries the might of an inferno within. Their spirits are as indomitable as the eternal flames they revere, and their exuberance crackles through their beings with a fiery cadence that can ignite the most stoic of hearts. Quick on their feet, they navigate their incandescent world with an effervescent zest, leaving the air shimmering with the subtle heat of their passage. Their homes mirror the twinkling bed of a starlit fire, nestled within the embrace of volcanic stone or carved into the walls of smoldering ravines. Here, the Emberkin Pyrelings draw life and inspiration from the very pulse of their blistering surroundings, their dwellings aglow with the reflection of their ceaseless, radiant keeper.",  # noqa: E501
        "warbrand": "|YWarbrand Pyrelings|n:\n\nIn the crucible where fire's fury forges the unbreakable, Warbrand Pyrelings rise. Cloaked in the robust raiment of battle and borne from the heart of conflict's flame, they are the embodiment of martial ardor. Their skin brandishes the ruddy glow of embers ready to ignite, a herald of the combative spirit that simmers within their fierce hearts. These skirmish-born Pyrelings walk with an inextinguishable resolve, their every sinew knitted with the ferocity of the blaze that has tested and tempered them. The fire that gave them life serves as their eternal ally, casting their silhouettes in a fearsome dance of light and shadow, aglow with the very essence of conflagration. Their warrens and redoubts are bastions set amidst the earth's seething rage, fortresses melded from the obsidian and basalt of their volcanic barricades. Here the Warbrand sharpen their resolve, their homes not mere residences but armaments against a world that challenges their might and dominion. The Warbrand are not merely warriors; they are the animate fusion of battle's call and the relentless spirit of fire that refuses to be quenched. In their eyes glimmers the tactical cunning born of firelit skirmishes and the profound camaraderie of those tested by the flames. They are steadfast sentinels, valiant and resolute, their kinship forged in the deepest heat - in the crucible where each Pyreling becomes a Warbrand, a living vow to stand with a blade of fire in the face of all that would dare challenge their fiery essence and iron-willed tenacity.",  # noqa: E501
    },
}


class CharacterRace:
    pass


@RaceRegistry.register
class Human(CharacterRace):
    race = "human"


@RaceRegistry.register
class Elf(CharacterRace):
    race = "elf"


@RaceRegistry.register
class HighElf(Elf):
    race = "high elf"


@RaceRegistry.register
class NightElf(Elf):
    race = "night elf"


@RaceRegistry.register
class WoodElf(Elf):
    race = "wood elf"


@RaceRegistry.register
class Dwarf(CharacterRace):
    race = "dwarf"


@RaceRegistry.register
class EmberheartDwarf(Dwarf):
    race = "emberheart dwarf"


@RaceRegistry.register
class StoneguardDwarf(Dwarf):
    race = "stoneguard dwarf"


@RaceRegistry.register
class IronveinDwarf(Dwarf):
    race = "ironvein dwarf"


@RaceRegistry.register
class Gnome(CharacterRace):
    race = "gnome"


@RaceRegistry.register
class DuskGnome(Gnome):
    race = "dusk gnome"


@RaceRegistry.register
class HearthGnome(Gnome):
    race = "hearth gnome"


@RaceRegistry.register
class SylvanGnome(Gnome):
    race = "sylvan gnome"


@RaceRegistry.register
class Nymph(CharacterRace):
    race = "nymph"


@RaceRegistry.register
class Orc(CharacterRace):
    race = "orc"


@RaceRegistry.register
class Pyreling(CharacterRace):
    race = "pyreling"


@RaceRegistry.register
class ArcanistPyreling(Pyreling):
    race = "arcanist pyreling"


@RaceRegistry.register
class EmberkinPyreling(Pyreling):
    race = "emberkin pyreling"


@RaceRegistry.register
class WarbrandPyreling(Pyreling):
    race = "warbrand pyreling"
