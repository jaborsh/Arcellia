from commands.command import Command
from handlers.quests import QuestProgress
from menus.interaction_menu import InteractionMenu
from typeclasses.mobs import Mob
from world.zones.nautilus.quest import NautilusObjective

from evennia import CmdSet
from evennia.utils import delay


class Enchantress(Mob):
    def greeting(self):
        def _say():
            self.execute_cmd("say You! Get me out of this damn cell!")

        delay(1, _say)


class CmdEnchantressInteract(Command):
    """
    Syntax: interact
            interact <target>

    This command allows the player to interact with the specified target.
    """

    key = "interact"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            if not (interaction := caller.location.db.interaction):
                return caller.msg("Interact with what?")
        else:
            target = caller.search(args)
            if not target:
                return

            if not (interaction := target.db.interaction):
                return caller.msg(
                    f"{target.get_display_name(caller)} is not interactive."
                )

        if (
            caller.quests.get_objective_status(
                "Nautilus", NautilusObjective.FREE_ENCHANTRESS
            )
            == QuestProgress.FAILED
        ):
            return caller.msg("The enchantress has been disintegrated.")

        if (
            interaction == "world.nautilus.interactions.enchantress"
            and caller.quests.get_objective_status(
                "Nautilus", NautilusObjective.FREE_ENCHANTRESS
            )
            == QuestProgress.COMPLETED
        ):
            InteractionMenu(
                caller,
                interaction,
                startnode="node_enchantress_intro",
                auto_look=True,
                auto_help=True,
                persistent=True,
            )
        else:
            InteractionMenu(
                caller,
                interaction,
                startnode="node_start",
                auto_look=True,
                auto_help=True,
                persistent=True,
            )


class EnchantressCmdSet(CmdSet):
    mergetype = "replace"
    priority = 11

    def at_cmdset_creation(self):
        self.add(CmdEnchantressInteract())
