from evennia.utils.utils import dedent

from handlers.quests import QuestProgress
from typeclasses.books import Book
from world.quests.emberlyn.emberlyn_start_quest import ArrivalObjective


class ShantyBook(Book):
    def at_read(self, reader):
        super().at_read(reader)
        reader.quests.set_objective(
            "Arrival",
            ArrivalObjective.READ_BOOK,
            "status",
            QuestProgress.COMPLETED,
        )


EMBERLYN_SHORE_HYMNS = {
    "prototype_key": "emberlyn_shore_hymns",
    "key": "book",
    "aliases": ["tide", "hymns"],
    "typeclass": "world.zones.emberlyn.emberlyn_beach.object_prototypes.ShantyBook",
    "display_name": "|CThe Darkened Tide: Hymns to the Deep Lady|n",
    "locks": "get:pperm(Admin)",
    "prototype_tags": [("emberlyn_shores", "zone")],
    "desc": "Bound in weathered, salt-stained leather, the tome's spine is cracked and swollen from years spent in damp, briny air. Faint barnacle scars cling to its cover, whispering of voyages through treacherous waters. The pages within are brittle and yellowed, their ink a deep, inky black that swirls like the undertow, seeming almost to move as though alive. Etched along the edges are runes of forgotten tongues, their meanings drowned long ago beneath the waves. A faint, ghostly shimmer of seafoam lingers in the air around it, giving the impression that the book has never quite dried.",
    "senses": {
        "feel": "The leather cover feels slick and damp, as though freshly touched by the sea's mist.",
        "smell": "A pungent scent of salt and decay clings to the pages, reminiscent of a forgotten shoreline at low tide.",
        "sound": "When held, a faint echo of distant waves crashing against jagged rocks hums through the air.",
        "taste": "The air around the tome carries a bitter tang, like the aftertaste of swallowed seawater.",
    },
    "stories": [
        dedent(
            """
            |xUpon the cold and cursed tide, we sail to the depths below,|n

            |xWhere the Lady waits with a thousand eyes in the darkened undertow.|n
            
            |xHer voice is the storm, her breath the gale, her eyes the endless sea,|n
            
            |xAnd when she calls, we give our souls to drown eternally.|n
            
            |xSing, lads, sing of the Lady's wrath, and let the winds go free,|n
            
            |xFor no man lives who sets his course against her willful sea.|n
            """
        ),
        dedent(
            """
            |CBelow the deck and below the sea, the Lady's voice calls out,|n
            
            |CHer song is the mournful cry of the depths, where sailors drift about.|n

            |CShe takes their bones and takes their souls, where light shall never be,|n

            |CAnd those who serve her wicked will shall know no light nor lee.|n

            |CSing, lads, sing of the endless night, where her dominion lies,|n

            |CFor no sun nor star can guide you through the dark beneath her skies.|n
            """
        ),
        dedent(
            """
            |mBeware the winds that scream her name, the Tempest's daughter's cry,|n
            
            |mFor when her rage unfurls its sails, beneath her wrath you'll lie.|n
            
            |mHer eyes are like the storm-tossed waves, her hair the blackened foam,|n
            
            |mAnd in her grasp, the ocean's might, her kingdom's endless home.|n
            
            |mSing, lads, sing of her cruel delight, the Lady fierce and free,|n
            
            |mFor none can tame the vicious gale that howls across the sea.|n
            """
        ),
        dedent(
            """
            |CFar below where the daylight fades, she waits with arms outspread,|n
            
            |CHer cold embrace the sailor's fate, their final, sunless bed.|n
            
            |CNo prayers can stay her hunger, no ship can flee her gaze,|n
            
            |CFor all who sail her haunted tides are lost in her dark maze.|n
            
            |CSing, lads, sing of the shadowed deep, where none shall ever flee,|n
            
            |CFor in her grasp, all souls are claimed to rest beneath the sea.|n
            """
        ),
        dedent(
            """
            |xThe tide comes in with the Lady's hand, to claim her rightful prize,|n
            
            |xShe drags the ships beneath the foam, no matter how men rise.|n
            
            |xHer waves are claws that tear and rend, her hunger knows no shore,|n
            
            |xAnd those who fight her fury's grasp will sink to rise no more.|n
            
            |xSing, lads, sing of the tide reaver, whose grip no man can break,|n
            
            |xFor once she claims you as her own, you're lost beneath the wake.|n
            """
        ),
    ],
}
