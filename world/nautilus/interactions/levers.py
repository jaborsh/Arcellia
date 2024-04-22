from commands.command import Command
from handlers.quests import QuestProgress

from evennia import CmdSet
from world.nautilus.quest import NautilusObjective


class CmdPullLever(Command):
    key = "pull"
    help_category = "Nautilus"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if (
            not caller.quests.get_objective_status(
                "Nautilus", NautilusObjective.FREE_ENCHANTRESS
            )
            == QuestProgress.IN_PROGRESS
        ):
            return caller.msg("The lever does not budge.")

        if not args:
            return caller.msg("Which lever do you want to pull?")

        if "left" in args:
            self.pull_left_lever()
        elif "right" in args:
            self.pull_right_lever()
        else:
            return caller.msg("You can only pull the left or right lever.")

    def pull_left_lever(self):
        caller = self.caller
        caller.quests.set_objective(
            "Nautilus",
            NautilusObjective.FREE_ENCHANTRESS,
            "status",
            QuestProgress.COMPLETED,
        )
        caller.msg(
            "You pull the left lever and hear a loud clunk. Suddenly, the enchantress' cell door swings open!"
        )

    def pull_right_lever(self):
        caller = self.caller
        caller.quests.set_objective(
            "Nautilus",
            NautilusObjective.FREE_ENCHANTRESS,
            "status",
            QuestProgress.FAILED,
        )
        caller.msg(
            "You pull the right lever and hear a loud clunk. Psionic energy radiates from the enchantress' cell and she disintegrates into thin air."
        )


class LeverCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdPullLever())
