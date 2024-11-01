from evennia.utils import (
    inherits_from,
)

from commands.command import Command
from typeclasses.books import Book


class CmdRead(Command):
    """
    Read a book or document.

    Syntax: read <book/document>

    Everyone loves a good book. Read one.
    """

    key = "read"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            return caller.msg("Read what?")

        book = caller.search(args)
        if not book:
            return

        if not inherits_from(book, Book):
            return caller.msg("You can't read that.")

        book.at_read(caller)
