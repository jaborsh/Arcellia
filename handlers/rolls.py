import random
import re


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]


class RollHandler(metaclass=SingletonMeta):

    def __init__(self):
        """Initialize a RollHandler object."""
        if not hasattr(self, "initialized"):
            self.dice_pattern = re.compile(r"(\d*)d(\d+)")
            self.initialized = True

    def check(self, roll_str, stat=None, dc=10, advantage=False, disadvantage=False):
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

    def roll(self, roll_str, stat=None, advantage=False, disadvantage=False):
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

        rolls = [random.randint(1, sides) for _ in range(num_dice)]
        total = sum(rolls)

        if advantage:
            adv_rolls = [random.randint(1, sides) for _ in range(num_dice)]
            total = max(total, sum(adv_rolls))
        elif disadvantage:
            dis_rolls = [random.randint(1, sides) for _ in range(num_dice)]
            total = min(total, sum(dis_rolls))

        modifier = self.get_modifier(stat) if stat else 0
        return total + modifier

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
