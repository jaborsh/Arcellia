from evennia.utils import (
    evtable,
)

from commands.command import Command


class CmdScore(Command):
    """
    Displays your character's score sheet, providing a detailed overview of your
    current attributes, health, mana, stamina, and other vital statistics.

    Usage:
        score

    Upon invoking this command, you will be presented with a neatly formatted
    table that includes your character's name, gender, race, level, and various
    attributes. Additionally, you will see your current health, mana, stamina,
    experience, wealth, and carried weight, giving you a comprehensive snapshot
    of your character's condition.
    """

    key = "score"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        table = evtable.EvTable(border="table")
        table.add_header("Score")
        table.add_row("Name:")
        table.add_row("Gender:")
        table.add_row("Race:")
        table.add_row("Level:")
        table.add_row("")
        table.add_row("")
        table.add_row("")
        table.add_row("Health:")
        table.add_row("Mana:")
        table.add_row("Stamina:")
        table.add_column(
            caller.name,
            caller.gender.value.value,
            caller.race.value.key,
            f"{caller.level.current}",
            "",
            "",
            "",
            f"{int(caller.health.value)}/{int(caller.health.max)}",
            f"{int(caller.mana.value)}/{int(caller.mana.max)}",
            f"{int(caller.stamina.value)}/{int(caller.stamina.max)}",
        )
        table.add_column(
            "Strength:",
            "Dexterity:",
            "Constitution:",
            "Intelligence:",
            "Wisdom:",
            "Charisma:",
            "",
            "Experience:",
            "Wealth:",
            "Weight:",
        )
        table.add_column(
            f"{int(caller.strength.value)}",
            f"{int(caller.dexterity.value)}",
            f"{int(caller.constitution.value)}",
            f"{int(caller.intelligence.value)}",
            f"{int(caller.wisdom.value)}",
            f"{int(caller.charisma.value)}",
            "",
            f"{caller.experience.value}",
            f"{caller.wealth.value}",
            f"{int(caller.weight.value)}/{int(caller.weight.max)}",
        )
        caller.msg(table)
