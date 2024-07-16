from handlers import buffs


# humans
class HumanVersatility(buffs.BaseBuff):
    """
    A buff that represents the human versatility trait.

    Humans are versatile creatures, allowing them to carry more weight.

    Attributes:
        key (str): The unique identifier for the buff.
        name (str): The name of the buff.
        flavor (str): A description of the buff.

    Methods:
        at_apply(): Applies the buff to the owner.
        at_remove(): Removes the buff from the owner.
    """

    key = "human_versatility"
    name = "Human Versatility"
    flavor = "Humans are versatile creatures. You can carry more weight."

    def at_apply(self):
        """
        Applies the buff to the owner.

        Increases the maximum weight the owner can carry by 25%.
        """
        self.owner.stats.weight.max = self.owner.stats.weight.max * 1.25

    def at_remove(self):
        """
        Removes the buff from the owner.

        Decreases the maximum weight the owner can carry by 25%.
        """
        self.owner.stats.weight.max = self.owner.stats.weight.max / 1.25


# elves, drow, and dwarves
class Darkvision(buffs.BaseBuff):
    """
    A class representing the Darkvision buff.

    Darkvision allows the character to see in the dark.

    Attributes:
        key (str): The key identifier for the superior darkvision feature.
        name (str): The name of the superior darkvision feature.
        flavor (str): A description of the enhanced darkvision ability.
    """

    key = "darkvision"
    name = "Darkvision"
    flavor = "You can see in the dark."


# drow
class SuperiorDarkvision(Darkvision):
    """
    A subclass of Darkvision that represents superior darkvision.

    Attributes:
        key (str): The key identifier for the superior darkvision feature.
        name (str): The name of the superior darkvision feature.
        flavor (str): A description of the enhanced darkvision ability.
    """

    key = "superior_darkvision"
    name = "Superior Darkvision"
    flavor = "Your darkvision is enhanced, allowing you to see even in complete darkness."


# halfling
class HalflingLuck(buffs.BaseBuff):
    """
    A buff that represents the halfling luck trait.

    Halflings are lucky creatures, allowing them to reroll failed saving throws.

    Attributes:
        key (str): The unique identifier for the buff.
        name (str): The name of the buff.
        flavor (str): A description of the buff.

    Methods:
        at_apply(): Applies the buff to the owner.
        at_remove(): Removes the buff from the owner.
    """

    key = "halfling_luck"
    name = "Halfling Luck"
    flavor = (
        "Halflings are lucky creatures. You can reroll failed saving throws."
    )
