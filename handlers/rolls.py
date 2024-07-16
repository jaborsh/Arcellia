import random
import re

from world.features import racial as racial_feats


class SingletonMeta(type):
    """
    Metaclass for creating singleton classes.

    This metaclass ensures that only one instance of a class is created and
    returned on subsequent calls to the class constructor.

    Usage:
    class MySingletonClass(metaclass=SingletonMeta):
        # class definition
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]


class RollHandler(metaclass=SingletonMeta):
    """
    A class that handles rolling dice and checking roll results against difficulty classes.
    """

    def __init__(self):
        """Initialize a RollHandler object."""
        if not hasattr(self, "initialized"):
            self.dice_pattern = re.compile(r"(\d*)d(\d+)")
            self.initialized = True

    def check(
        self, roll_str, stat=None, dc=10, advantage=False, disadvantage=False
    ):
        """
        Checks if the result of a roll meets or exceeds a given difficulty class (dc).

        Args:
            roll_str (str): The string representing the roll to be performed.
            stat (str, optional): The stat to use for the roll. Defaults to None.
            dc (int, optional): The difficulty class to compare the roll result against. Defaults to 10.
            advantage (bool, optional): Whether to roll with advantage. Defaults to False.
            disadvantage (bool, optional): Whether to roll with disadvantage. Defaults to False.

        Returns:
            bool: True if the roll result is greater than or equal to the dc, False otherwise.
        """
        if advantage and disadvantage:
            raise ValueError("Cannot have both advantage and disadvantage.")

        rolls = [
            self.roll(roll_str, stat)
            for _ in range(2 if advantage or disadvantage else 1)
        ]
        return (
            any(roll >= dc for roll in rolls)
            if advantage
            else all(roll >= dc for roll in rolls)
        )

    def roll(
        self,
        roll_str,
        stat=None,
        advantage=False,
        disadvantage=False,
        roller=None,
    ):
        """
        Rolls a specified number of dice with a specified number of sides and returns the total sum.

        Args:
            roll_str (str): The string representing the roll, in the format "NdS" where N is the number of dice and S is the number of sides.
            stat (int, optional): The modifier to be added to the total sum. Defaults to None.
            advantage (bool, optional): Whether to roll with advantage. Defaults to False.
            disadvantage (bool, optional): Whether to roll with disadvantage. Defaults to False.

        Returns:
            int: The total sum of the dice rolls plus the modifier.

        Raises:
            ValueError: If the roll string is invalid.
        """
        matches = self.dice_pattern.match(roll_str)
        if not matches:
            raise ValueError(f"Invalid roll string: {roll_str}.")

        num_dice, sides = map(int, matches.groups())
        num_dice = num_dice or 1

        if roller and roller.feats.has(racial_feats.HalflingLuck):
            rolls = [random.randint(2, sides) for _ in range(num_dice)]
        else:
            rolls = [random.randint(1, sides) for _ in range(num_dice)]

        total = sum(rolls)
        total += self.get_modifier(stat) if isinstance(stat, int) else 0

        if advantage or disadvantage:
            adv_roll = self.roll(roll_str, stat, roller)
            total = max(total, adv_roll) if advantage else min(total, adv_roll)

        return total

    def get_modifier(self, stat):
        """
        Calculates the modifier for a given stat.

        Args:
            stat (int): The value of the stat.

        Returns:
            int: The modifier value.

        """
        if stat < 1:
            return -5
        elif stat > 30:
            return 10
        else:
            return (stat - 10) // 2
