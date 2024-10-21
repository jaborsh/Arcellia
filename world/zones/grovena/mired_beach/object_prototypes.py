from evennia.utils.utils import dedent

MIRED_SHORE_HYMNS = {
    "prototype_key": "mired_shore_hymns",
    "key": "book",
    "aliases": ["tide", "hymns"],
    "typeclass": "typeclasses.books.Book",
    "display_name": "|CThe Darkened Tide: Hymns to the Deep Lady|n",
    "locks": "get:pperm(Admin)",
    "prototype_tags": [("mired_shores", "zone")],
    "desc": "Bound in weathered, salt-stained leather, the tome's spine is cracked and swollen from years spent in damp, briny air. Faint barnacle scars cling to its cover, whispering of voyages through treacherous waters. The pages within are brittle and yellowed, their ink a deep, inky black that swirls like the undertow, seeming almost to move as though alive. Etched along the edges are runes of forgotten tongues, their meanings drowned long ago beneath the waves. A faint, ghostly shimmer of seafoam lingers in the air around it, giving the impression that the book has never quite dried.",
    "senses": {
        "feel": "The leather cover feels slick and damp, as though freshly touched by the sea's mist.",
        "smell": "A pungent scent of salt and decay clings to the pages, reminiscent of a forgotten shoreline at low tide.",
        "sound": "When held, a faint echo of distant waves crashing against jagged rocks hums through the air.",
        "taste": "The air around the tome carries a bitter tang, like the aftertaste of swallowed seawater.",
    },
    "story": dedent(
        """
        |CUpon the cold and cursed tide, we sail to the depths below,|n
        
        |CWhere the Lady waits with a thousand eyes in the darkened undertow.|n
        
        |CHer voice is the storm, her breath the gale, her eyes the endless sea,|n
        
        |CAnd when she calls, we give our souls to drown eternally.|n
        
        |CSing, lads, sing of the Lady's wrath, and let the winds go free,|n
        
        |CFor no man lives who sets his course against her willful sea.|n
        """
    ),
}
