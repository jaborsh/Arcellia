from evennia.utils.funcparser import ACTOR_STANCE_CALLABLES, FuncParser

from commands.command import Command
from typeclasses.characters import Character
from utils.text import wrap

PARSER = FuncParser(ACTOR_STANCE_CALLABLES)


class CmdShout(Command):
    """
    Syntax: shout [message]

    Shout something to tell the whole world.
    """

    key = "shout"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if caller.permissions.check("no_shout"):
            return caller.msg("Your throat is too sore to shout.")

        if not args:
            return caller.msg("Shout what?")

        chars = [char for char in Character.objects.all() if char.is_connected]
        for char in chars:
            pre_text = PARSER.parse(
                '$You() $conj(shout), "', caller=caller, receiver=char
            )
            message = "|r" + wrap(args + '"', pre_text=pre_text)
            char.msg(message)
