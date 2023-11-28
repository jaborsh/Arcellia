import time

from evennia.typeclasses.attributes import AttributeProperty


class BuffableProperty(AttributeProperty):
    """An example of a way you can extend AttributeProperty to create properties that automatically check buffs for you."""

    def at_get(self, value, obj):
        _value = obj.buffs.check(value, self._key)
        return _value


class Buff:
    key = "buff"  # The buff's unique key. Will be used as the buff's key in the handler
    name = "Buff"  # The buff's name. Used for user messaging
    flavor = "Buff String"  # The buff's flavor text. Used for user messaging
    visible = True  # If the buff is considered "visible" to the "view" method

    triggers = []  # The effect's trigger strings, used for functions.

    handler = None
    start = 0

    duration = -1  # Default buff duration; -1 for permanent, 0 for "instant", >0 normal
    playtime = False  # Does this buff autopause when owning object is unpuppeted?

    refresh = True  # Does the buff refresh its timer on application?
    unique = True  # Does the buff overwrite existing buffs with the same key on the same target?
    maxstacks = 1  # The maximum number of stacks the buff can have. If >1, this buff will stack.
    stacks = 1  # Used as the default when applying this buff if no or negative stacks were specified (min: 1)
    tickrate = (
        0  # How frequent does this buff tick, in seconds (cannot be lower than 1)
    )

    mods = []  # List of mod objects. See Mod class below for more detail
    cache = {}

    @property
    def ticknum(self):
        """Returns how many ticks this buff has gone through as an integer."""
        x = (time.time() - self.start) / max(1, self.tickrate)
        return int(x)

    @property
    def owner(self):
        """Return this buff's owner (the object its handler is attached to)"""
        if not self.handler:
            return None
        return self.handler.owner

    @property
    def timeleft(self):
        """Returns how much time this buff has left. If -1, it is permanent."""
        _tl = 0
        if not self.start:
            _tl = self.duration
        else:
            _tl = max(-1, self.duration - (time.time() - self.start))
        return _tl

    @property
    def ticking(self) -> bool:
        """Returns if this buff ticks or not (tickrate => 1)"""
        return self.tickrate >= 1

    @property
    def stacking(self) -> bool:
        """Returns if this buff stacks or not (maxstacks > 1)"""
        return self.maxstacks > 1

    def __init__(self, handler, buffkey, cache) -> None:
        """
        Args:
            handler:    The handler this buff is attached to
            buffkey:    The key this buff uses on the cache
            cache:      The cache dictionary (what you get if you use `handler.buffcache.get(key)`)
        """
        required = {"handler": handler, "buffkey": buffkey, "cache": cache}
        self.__dict__.update(cache)
        self.__dict__.update(required)
        # Init hook
        self.at_init()

    def __setattr__(self, attr, value):
        if attr in self.cache:
            if attr == "tickrate":
                value = max(0, value)
            self.handler.buffcache[self.buffkey][attr] = value
        super().__setattr__(attr, value)

    def conditional(self, *args, **kwargs):
        """Hook function for conditional evaluation.

        This must return True for a buff to apply modifiers, trigger effects, or tick.
        """
        return True

    # region helper methods
    def remove(self, loud=True, expire=False, context=None):
        """Helper method which removes this buff from its handler. Use dispel if you are dispelling it instead.

        Args:
            loud:   (optional) Whether to call at_remove or not (default: True)
            expire: (optional) Whether to call at_expire or not (default: False)
            delay:  (optional) How long you want to delay the remove call for
            context:    (optional) A dictionary you wish to pass to the at_remove/at_expire method as kwargs
        """
        if not context:
            context = {}
        self.handler.remove(self.buffkey, loud=loud, expire=expire, context=context)

    def dispel(self, loud=True, delay=0, context=None):
        """Helper method which dispels this buff (removes and calls at_dispel).

        Args:
            loud:   (optional) Whether to call at_remove or not (default: True)
            delay:  (optional) How long you want to delay the remove call for
            context:    (optional) A dictionary you wish to pass to the at_remove/at_dispel method as kwargs
        """
        if not context:
            context = {}
        self.handler.remove(
            self.buffkey, loud=loud, dispel=True, delay=delay, context=context
        )

    def pause(self, context=None):
        """Helper method which pauses this buff on its handler.

        Args:
            context:    (optional) A dictionary you wish to pass to the at_pause method as kwargs
        """
        if not context:
            context = {}
        self.handler.pause(self.buffkey, context)

    def unpause(self, context=None):
        """Helper method which unpauses this buff on its handler.

        Args:
            context:    (optional) A dictionary you wish to pass to the at_unpause method as kwargs
        """
        if not context:
            context = {}
        self.handler.unpause(self.buffkey, context)

    def reset(self):
        """Resets the buff start time as though it were just applied; functionally identical to a refresh"""
        self.start = time.time()
        self.handler.buffcache[self.buffkey]["start"] = time.time()

    def update_cache(self, to_cache: dict):
        """Updates this buff's cache using the given values, both internally (this instance) and on the handler.

        Args:
            to_cache:   The dictionary of values you want to add to the cache"""
        if not isinstance(to_cache, dict):
            raise TypeError
        _cache = dict(self.handler.buffcache[self.buffkey])
        _cache.update(to_cache)
        self.cache = _cache
        self.handler.buffcache[self.buffkey] = _cache

    # endregion

    # region hook methods
    def at_init(self, *args, **kwargs):
        """Hook function called when this buff object is initialized."""
        pass

    def at_apply(self, *args, **kwargs):
        """Hook function to run when this buff is applied to an object."""
        pass

    def at_remove(self, *args, **kwargs):
        """Hook function to run when this buff is removed from an object."""
        pass

    def at_dispel(self, *args, **kwargs):
        """Hook function to run when this buff is dispelled from an object (removed by someone other than the buff holder)."""
        pass

    def at_expire(self, *args, **kwargs):
        """Hook function to run when this buff expires from an object."""
        pass

    def at_pre_check(self, *args, **kwargs):
        """Hook function to run before this buff's modifiers are checked."""
        pass

    def at_post_check(self, *args, **kwargs):
        """Hook function to run after this buff's mods are checked."""
        pass

    def at_trigger(self, trigger: str, *args, **kwargs):
        """Hook for the code you want to run whenever the effect is triggered.
        Passes the trigger string to the function, so you can have multiple
        triggers on one buff."""
        pass

    def at_tick(self, initial: bool, *args, **kwargs):
        """Hook for actions that occur per-tick, a designer-set sub-duration.
        `initial` tells you if it's the first tick that happens (when a buff is applied).
        """
        pass

    def at_pause(self, *args, **kwargs):
        """Hook for when this buff is paused"""
        pass

    def at_unpause(self, *args, **kwargs):
        """Hook for when this buff is unpaused."""
        pass

    # endregion


class Mod:
    """A single stat mod object. One buff or trait can hold multiple mods, for the same or different stats."""

    stat = (
        "null"  # The stat string that is checked to see if this mod should be applied
    )
    value = 0  # Buff's value
    perstack = 0  # How much additional value is added to the buff per stack
    modifier = "add"  # The modifier the buff applies. 'add' or 'mult'

    def __init__(self, stat: str, modifier: str, value, perstack=0.0) -> None:
        """
        Args:
            stat:       The stat the buff affects. Normally matches the
                        object attribute name
            mod:        The modifier the buff applies. "add" for add/sub
                        or "mult" for mult/div
            value:      The value of the modifier
            perstack:   How much is added to the base, per stack (including
                        first).
        """
        self.stat = stat
        self.modifier = modifier
        self.value = value
        self.perstack = perstack


"""
Example Buff Command:

class CmdBuff(Command):
    \"""
    Buff a target.

    Usage:
      buff <target> <buff>

    Applies the specified buff to the target. All buffs are defined in the bufflist dictionary on this command.
    \"""

    key = "buff"
    aliases = ["buff"]
    help_category = "builder"

    bufflist = {"foo": BaseBuff}

    def parse(self):
        self.args = self.args.split()

    def func(self):
        caller = self.caller
        target = None
        now = time.time()

        if self.args:
            target = caller.search(self.args[0])
            caller.ndb.target = target
        elif caller.ndb.target:
            target = caller.ndb.target
        else:
            caller.msg("You need to pick a target to buff.")
            return

        if self.args[1] not in self.bufflist.keys():
            caller.msg("You must pick a valid buff.")
            return

        if target:
            target.buffs.add(self.bufflist[self.args[1]], source=caller)
            pass

"""
