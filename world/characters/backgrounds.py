from class_registry import ClassRegistry

background_registry = ClassRegistry("name")

BACKGROUND_INFO_DICT = {
    "acolyte": "|YAcolyte|n:\n\nHere, in the cloistered recesses of a sanctified monastery, a young acolyte finds solace, the air imbued with currents of piety and the scent of incense. Devoted from a tender age, with incandescent hope kindling a fire within, the acolyte learns the lore of the celestial beings and the cryptic cadence of sacred chants. Anointed into service, chosen by fate or divine whim, the acolyte's spirit entwines with the arcane and the prophetic. Vows uttered in reverent tones bind this pupil to a life of devout study, shaping the essence of being, refining body and soul for the pious battle against the encroaching shades of malevolence.",
    "charlatan": "|YCharlatan|n:\n\nWhere haggling voices and the clinking of coin weave the threads of commerce, a figure adept in the art of guile and craft moves with the grace of a whisper. Through the throngs cluttering the marketplace, the charlatan maneuvers, eyes brimming with deceptive mirth, lips curled in a conspirator's smirk. Trained in the virtuosic craft of deceit, this artificer of illusions revels in the masquerade, spinning tales as intricate as the fine silks peddled by merchants from far-off lands.",
    "criminal": "|YCriminal|n:\n\nIn the underbelly of a city cloaked in the deceptive comfort of shadows, where law exists merely as a spider's web waiting to be torn asunder by those cunning enough, a criminal's tale unravels. With hands that have danced the nimble waltz of thievery and a gaze ever watchful, the criminal emerges, a ghost among the chaos of depravity. Crafted in the crucible of the unwritten, where might reigns and honor is but a withered relic, this denizen of darkness thrives upon the thrill of the illicit.",
    "entertainer": "|YEntertainer|n:\n\nBeneath the glow of limelights and the approving gaze of the moon, an amphitheater resounds with the timbre of a life most vivid. Here, the entertainer spins tales not with words alone, but with the very sinews of being, giving breath to the dreams of others. The stage - a world unto itself - beckons, and the entertainer obliges, a puppeteer of delight woven into the grand narrative of escapade and spectacle. Echoes of applause and the rush of elation serve as a siren's call, as the entertainer pledges to a life of itinerancy, embracing applause as a beloved companion.",
    "folk hero": "|YFolk Hero|n:\n\nThis champion's saga began with a pledge whispered amidst the wheat fields, where the land itself bore witness - a promise to uphold the sanctity of the simple, the integrity of the honest, and the valor of the righteous. A steel-forged resolve in a leather-clad grip, the folk hero's tale is one of humble origins scaling insurmountable odds, a melody that stirs the blood and emboldens even the weariest of spirits.",
    "hermit": "|YHermit|n:\n\nSeparated from the common throng by choice or by fate's stern hand, the hermit's covenant is struck with the essence of isolation, a solemn oath to slice through the veils of ignorance with wisdom's keen blade. The hermit understands that knowledge is the truest companion, a kindred spirit that neither betrays nor fades as the mortal coil may.",
    "merchant": "|YMerchant|n:\n\nArrayed not in steel but in the sheen of silk and the luster of well-touched gold, the merchant commands a different sort of empire - one built upon the ebb and flow of supply and demand, of rare spices and rarer artifacts, each a story in its own right. Their ledger - a chronicle of ambition inscribed with the careful hand that knows the true power of wealth wielded with acumen.",
    "noble": "|YNoble|n:\n\nClad in the mantle of their forebears, the refinement of their bearing as much a birthright as the blood that runs noble and cold in their veins, this scion of prestige navigates a world of elaborate dances and dangerous liaisons. Each gesture is a calculated move; every word, a carefully placed piece upon the chessboard of aristocratic stratagems. As the clarion call of destiny reverberates through the marbled ancestry, the noble is drawn to the realization that their role is but a prelude to a larger saga: a tale yet unwritten, of valorous deeds and whispered secrets amidst the annals of power. With the weight of their name as a bannerman's call, the noble ventures forth, armored by privilege and armed with the cunning to forge their own path.",
    "outlander": "|YOutlander|n:\n\nGarbed in leathers weathered by the kiss of countless suns and caress of tireless winds, the outlander knows the earth's secrets as kin. Their stride is unburdened, fluid with the instinctual knowledge of one who has partaken of untrodden paths and drunk from hidden springs. With every step that distances them from the comfort of the familiar, the outlander carries the untold stories of remote vistas and the fortunes that lie yonder. The call of the wild, a resonant drum that beats in tandem with their heart, guides the outlander on - a nomad caught between worlds, seeking the crossroads where fate and freedom intersect in the vast sermon of the untamed earth.",
    "sage": "|YSage|n:\n\nWithin the silent reverence of a library that transcends time, where the air itself is thick with the musk of parchment and the essence of knowledge sealed within infinite tomes, a sage finds their calling. Amidst towering shelves that hold the weight of wisdom and the whispers of the past, they meander - a seeker and guardian of the arcane and the known. The volumes that surmount the oaken desks, their pages fraught with the musings of sages and scholars long departed, are companions as dear as any flesh-bound peer. Bound by an innate drive to unravel the universe's heart, the sage's journey is one of perpetual discovery, illuminated by the luminescence of intellect.",
    "sailor": "|YSailor|n:\n\nUpon the tempestuous canvas of the ocean, where horizon meets heaven in an endless embrace, a sailor finds harmony in the heave and thrum of the untamed deep. Cradled in the bosom of a vessel that creaks its sea shanties to the rhythm of the waves, this sojourner of brine and brume heeds the siren call of the vast watery expanse. The sailor's tale unfolds with each cresting wave and sung with every taut line. Destiny is no longer dictation from the land, but a chart to be plotted amongst stars and sea. With each journey that carves its legacy into the annals of maritime lore, the sailor ventures forth, guiding their ship to lands distant and dreams wild as the ocean herself is boundless.",
    "soldier": "|YSoldier|n:\n\nEach scar is a verse in the soldier's lore, every callused hand speaking to battles endured and victories seized in the breathless moments when life and duty intersect with the acute edge of a blade. Versed in the grim cadence of combat, they learn the weighty language of discipline and the unyielding lexicon of endurance, pledges made not in word, but in deed - the tacit conclave between shieldmates as they stand shoulder-to-shoulder against the tide of adversaries.",
    "urchin": "|YUrchin|n:\n\nCrafted by the unforgiving hands of scarcity and a life lived within the narrow avenues beyond society's gaze, this sprite of the streets wields cunning as a blade, as necessary as the very air drawn into young lungs. With the tenacity of the forsaken and the wiles of the wise, the urchin steps forth from the whispering dark, ready to ply the trade of survival in a world vast and unpredictable, carrying nothing but the currency of their wits and the mettle forged in the furnaces of want and will.",
}


class CharacterBackground:
    pass


@background_registry.register
class Adventurer(CharacterBackground):
    name = "adventurer"


@background_registry.register
class Acolyte(CharacterBackground):
    name = "acolyte"


@background_registry.register
class Charlatan(CharacterBackground):
    name = "charlatan"


@background_registry.register
class Criminal(CharacterBackground):
    name = "criminal"


@background_registry.register
class Entertainer(CharacterBackground):
    name = "entertainer"


@background_registry.register
class FolkHero(CharacterBackground):
    name = "folk hero"


@background_registry.register
class GuildArtisan(CharacterBackground):
    name = "guild artisan"


@background_registry.register
class Hermit(CharacterBackground):
    name = "hermit"


@background_registry.register
class Merchant(CharacterBackground):
    name = "merchant"


@background_registry.register
class Noble(CharacterBackground):
    name = "noble"


@background_registry.register
class Outlander(CharacterBackground):
    name = "outlander"


@background_registry.register
class Sage(CharacterBackground):
    name = "sage"


@background_registry.register
class Sailor(CharacterBackground):
    name = "sailor"


@background_registry.register
class Soldier(CharacterBackground):
    name = "soldier"


@background_registry.register
class Urchin(CharacterBackground):
    name = "urchin"
