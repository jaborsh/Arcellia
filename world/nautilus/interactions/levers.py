from commands.command import Command
from evennia import CmdSet

from world.nautilus.quest import NautilusQuest


class CmdPullLever(Command):
    key = "pull"
    help_category = "Nautilus"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not (caller.quests.get("Nautilus")):
            caller.quests.add(NautilusQuest)

        if caller.quests.get_detail("Nautilus", "pulled_lever"):
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
        caller.quests.add_details("Nautilus", {"pulled_lever": "left"})
        caller.msg(
            "You pull the left lever and hear a loud clunk. Suddenly, the enchantress' cell door swings open!"
        )

    def pull_right_lever(self):
        caller = self.caller
        caller.quests.add_details("Nautilus", {"pulled_lever": "right"})
        caller.quests._save()
        caller.msg(
            "You pull the right lever and hear a loud clunk. Psionic energy radiates from the enchantress' cell and a sense of dread washes over you."
        )


class LeverCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdPullLever())
