import math
import time
from typing import Any, Dict, List, Optional, Union

from .handler import Handler


class CooldownHandler(Handler):
    """
    Handler for cooldowns. This can be attached to any object that supports
    DB attributes (like a Character or Account).

    A cooldown is a timer that is usually used to limit how often some action
    can be performed or some effect can trigger. When a cooldown is first
    added, it counts down from the amount of time provided back to zero, at
    which point it is considered ready again.

    Cooldowns are named with an arbitrary string, and that string is used to
    check on the progression of the cooldown. Each cooldown is tracked
    separately and independently from other cooldowns on that same object. A
    cooldown is unique per-object.

    Cooldowns are saved persistently, so they survive reboots. This module
    does not register or provide callback functionality for when a cooldown
    becomes ready again. Users of cooldowns are expected to query the state
    of any cooldowns they are interested in.

    Methods:
        - ready(name): Checks whether a given cooldown name is ready.
        - time_left(name): Returns how much time is left on a cooldown.
        - add(name, seconds): Sets a given cooldown to last for a certain
            amount of time. Until then, ready() will return False for that
            cooldown name. set() is an alias.
        - extend(name, seconds): Like add(), but adds more time to the
            given cooldown if it already exists. If it doesn't exist yet,
            calling this is equivalent to calling add().
        - reset(cooldown): Resets a given cooldown, causing ready() to
            return True for that cooldown immediately.
        - clear(): Resets all cooldowns.
    """

    def __init__(
        self,
        obj: Any,
        db_attribute_key: str = "cooldowns",
        db_attribute_category: Optional[str] = None,
        default_data: Optional[Dict] = None,
    ) -> None:
        super().__init__(
            obj, db_attribute_key, db_attribute_category, default_data
        )
        self._last_timestamp: float = time.time()

    @property
    def current_time(self) -> float:
        """Cache and return current timestamp."""
        self._last_timestamp = time.time()
        return self._last_timestamp

    def all(self) -> List[str]:
        """Returns a list of all cooldown keys."""
        return list(self._data.keys())

    def ready(self, *args: str) -> bool:
        """Checks whether all of the provided cooldowns are ready."""
        return self.time_left(*args, use_int=True) <= 0

    def time_left(self, *args: str, use_int: bool = False) -> Union[float, int]:
        """Returns the maximum amount of time left on given cooldowns."""
        now = self.current_time
        # Optimize list comprehension by avoiding multiple lookups
        cooldowns = []
        for name in args:
            if name in self._data:
                cooldowns.append(self._data[name] - now)

        if not cooldowns:
            return 0 if use_int else 0.0

        left = max(max(cooldowns), 0)
        return math.ceil(left) if use_int else left

    def add(self, cooldown: str, seconds: Union[float, int]) -> None:
        """Adds/sets a given cooldown to last for a specific amount of time."""
        self._data[cooldown] = self.current_time + max(seconds or 0, 0)

    set = add

    def extend(self, cooldown: str, seconds: Union[float, int]) -> float:
        """Adds a specific amount of time to an existing cooldown."""
        time_left = self.time_left(cooldown) + (seconds or 0)
        self.set(cooldown, time_left)
        return max(time_left, 0)

    def reset(self, cooldown: str) -> None:
        """Resets a given cooldown."""
        self._data.pop(
            cooldown, None
        )  # More efficient than checking then deleting

    def clear(self) -> None:
        """Resets all cooldowns."""
        self._data.clear()

    def cleanup(self) -> None:
        """Deletes all expired cooldowns."""
        now = self.current_time
        # Change condition to remove timestamps that are in the past
        cleaned = {
            key: value for key, value in self._data.items() if value > now
        }

        if len(cleaned) != len(self._data):
            self._data = cleaned
            self.obj.attributes.add(self._db_attr, cleaned)
