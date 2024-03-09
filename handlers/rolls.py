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
        if not hasattr(
            self, "initialized"
        ):  # This ensures __init__ is only called once
            self.dice_pattern = re.compile(r"(\d*)d(\d+)")
            self.initialized = True

    def check(
        self,
        roll_str,
        stat=None,
        dc=10,
        advantage=False,
        disadvantage=False,
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

        if advantage:
            roll1 = self.roll(roll_str, stat)
            roll2 = self.roll(roll_str, stat)
            return max(roll1, roll2) >= dc

        if disadvantage:
            roll1 = self.roll(roll_str, stat)
            roll2 = self.roll(roll_str, stat)
            return min(roll1, roll2) >= dc

        return self.roll(roll_str, stat) >= dc

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

        num_dice, sides = matches.groups()
        num_dice = int(num_dice) if num_dice else 1
        sides = int(sides)

        total = 0
        if advantage:
            for _ in range(num_dice):
                roll1 = random.randint(1, sides)
                roll2 = random.randint(1, sides)
                total += max(roll1, roll2)
        elif disadvantage:
            for _ in range(num_dice):
                roll1 = random.randint(1, sides)
                roll2 = random.randint(1, sides)
                total += min(roll1, roll2)
        else:
            for _ in range(num_dice):
                total += random.randint(1, sides)

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
