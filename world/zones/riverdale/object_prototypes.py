from evennia.utils.utils import dedent

RIVERDALE_BOOK_WARRIOR = {
    "prototype_key": "riverdale_book_warrior",
    "key": "book",
    "aliases": ["warrior"],
    "display_name": "|#4B7F52Book of the Warrior|n",
    "desc": dedent("""
        The cover depicts a dimly lit chamber within a grand, but aging mansion. The room is opulent, with rich, heavy curtains of deep burgundy framing a tall, open window on the right side of the cover, the night sky visible beyond. A half-moon casts a faint silver glow through the window, illuminating a shadowy figure mid-leap, just vanishing out of the frame, with a glint of a large, radiant gem visible in his hand. His face is hidden by a hood, his silhouette agile and sharp against the darkness of the night.
        
        |Y[Hint]|n: You might want to |C'read'|n this book.
    """),
    "locks": "get:pperm(Admin)",
    "prototype_tags": [("riverdale", "zone")],
    "senses": {
        "feel": "The cover of the book feels textured, with an embossed title rising slightly beneath your fingertips. The pages are thick and sturdy, their edges rough and untrimmed, as though made from handmade parchment.",
        "smell": "Opening the book, the scent of aged leather wafts up, mingling with the faint, musty aroma of old paper. There's a trace of ink, still sharp and rich.",
        "sound": "As the pages turn, they make a soft rustling sound. When the book is closed, the faint creak of the binding can be heard, like the groaning of an old, sturdy chest being opened for the first time in years.",
        "taste": "Should you be curious enough to taste it, the book carries the faintest hint of dust on the tongue, mixed with the dryness of old paper.",
    },
    "story": dedent(
        """
        In a distant kingdom, a young heir, burdened with immense wealth but no familial ties or secure standing, was whisked away from his impoverished homeland to a foreign city by his servants. His life of indulgence left him with little concern for anything but the expansion of his fortune. His obsession with gold knew no bounds, and he resorted to hiring mercenaries to terrorize lands he wished to acquire cheaply. His latest plot involved a rare vineyard of great value, and to secure it, he had promised a vast gem to a renowned mercenary leader. One day, after a fitful sleep, he awoke to find a thief in his room, attempting to steal the very gem he had promised. A clumsy struggle ensued, as the heir, more concerned with preserving the value of his treasures than fighting effectively, flailed uselessly with a sword. The thief, shield in hand, evaded the heir's clumsy strikes until, with the guards arriving too late, he leaped from the window and fled into the streets, the stolen gem in his possession, unsure of his next destination but certain he could never return.
        """
    ),
}
