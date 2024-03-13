import time
from random import random

from evennia.server import signals
from evennia.utils import search, utils

from world.buffs.buffs import Buff, Mod


class BuffHandler:
    ownerref = None
    dbkey = "buffs"
    autopause = False
    _owner = None

    def __init__(self, owner, dbkey=dbkey, autopause=autopause):
        """
        Args:
            owner:  The object this handler is attached to
            dbkey:  (optional) The string key of the db attribute to use for the buff cache
            autopause:  (optional) Whether this handler autopauses playtime buffs on owning object's unpuppet
        """
        self.ownerref = owner.dbref
        self.dbkey = dbkey
        self.autopause = autopause
        if autopause:
            self._validate_state()
            signals.SIGNAL_OBJECT_POST_UNPUPPET.connect(self._pause_playtime)
            signals.SIGNAL_OBJECT_POST_PUPPET.connect(self._unpause_playtime)

    # region properties
    @property
    def owner(self):
        """The object this handler is attached to."""
        if self.ownerref:
            _owner = search.search_object(self.ownerref)
        if _owner:
            return _owner[0]
        else:
            return None

    @property
    def buffcache(self):
        """The object attribute we use for the buff cache. Auto-creates if not present."""
        if not self.owner:
            return {}
        if not self.owner.attributes.has(self.dbkey):
            self.owner.attributes.add(self.dbkey, {})
        return self.owner.attributes.get(self.dbkey)

    @property
    def traits(self):
        """All buffs on this handler that modify a stat."""
        _cache = self.all
        _t = {k: buff for k, buff in _cache.items() if buff.mods}
        return _t

    @property
    def effects(self):
        """All buffs on this handler that trigger off an event."""
        _cache = self.all
        _e = {k: buff for k, buff in _cache.items() if buff.triggers}
        return _e

    @property
    def playtime(self):
        """All buffs on this handler that only count down during active playtime."""
        _cache = self.all
        _pt = {k: buff for k, buff in _cache.items() if buff.playtime}
        return _pt

    @property
    def paused(self):
        """All buffs on this handler that are paused."""
        _cache = self.all
        _p = {k: buff for k, buff in _cache.items() if buff.paused}
        return _p

    @property
    def expired(self):
        """All buffs on this handler that have expired (no duration or no stacks)."""
        _cache = self.all
        _e = {
            k: buff
            for k, buff in _cache.items()
            if not buff.paused
            if buff.duration > -1
            if buff.duration < time.time() - buff.start
        }
        _nostacks = {k: buff for k, buff in _cache.items() if buff.stacks <= 0}
        _e.update(_nostacks)
        return _e

    @property
    def visible(self):
        """All buffs on this handler that are visible."""
        _cache = self.all
        _v = {k: buff for k, buff in _cache.items() if buff.visible}
        return _v

    @property
    def all(self):
        """Returns dictionary of instanced buffs equivalent to ALL buffs on this handler,
        regardless of state, type, or anything else."""
        _a = self.get_all()
        return _a

    # endregion

    # region methods
    def add(
        self,
        buff: Buff,
        key: str = None,
        stacks=0,
        duration=None,
        source=None,
        to_cache=None,
        context=None,
        *args,
        **kwargs,
    ):
        """Add a buff to this object, respecting all stacking/refresh/reapplication rules. Takes
        a number of optional parameters to allow for customization.

        Args:
            buff:       The buff class type you wish to add
            key:        (optional) The key you wish to use for this buff; overrides defaults
            stacks:     (optional) The number of stacks you want to add, if the buff is stacking
            duration:   (optional) The amount of time, in seconds, you want the buff to last; overrides defaults
            source:     (optional) The source of this buff. (default: None)
            to_cache:   (optional) A dictionary to store in the buff's cache; does not overwrite default cache keys
            context:    (optional) A dictionary you wish to pass to the at_apply method as kwargs
        """
        if not isinstance(buff, type):
            raise ValueError
        if not context:
            context = {}
        b = {}
        _context = dict(context)

        # Initial cache updating, starting with the class cache attribute and/or to_cache
        if buff.cache:
            b = dict(buff.cache)
        if to_cache:
            b.update(dict(to_cache))

        # Guarantees we stack either at least 1 stack or whatever the class stacks attribute is
        if stacks < 1:
            stacks = min(1, buff.stacks)

        # Create the buff dict that holds a reference and all runtime information.
        b.update(
            {
                "ref": buff,
                "start": time.time(),
                "duration": buff.duration,
                "tickrate": buff.tickrate,
                "prevtick": time.time(),
                "paused": False,
                "stacks": stacks,
                "source": source,
            }
        )

        # Generate the buffkey from the object's dbref and the default buff key.
        # This is the actual key the buff uses on the dictionary
        buffkey = key
        if not buffkey:
            if source:
                mix = str(source.dbref).replace("#", "")
            elif not (buff.unique or buff.refresh) or not source:
                mix = "_ufrf" + str(int((random() * 999999) * 100000))

            buffkey = buff.key if buff.unique is True else buff.key + mix

        # Rules for applying over an existing buff
        if buffkey in self.buffcache.keys():
            existing = dict(self.buffcache[buffkey])
            # Stacking
            if buff.maxstacks > 1:
                b["stacks"] = min(existing["stacks"] + stacks, buff.maxstacks)
            elif buff.maxstacks < 1:
                b["stacks"] = existing["stacks"] + stacks
            # refresh rule for uniques
            if not buff.refresh:
                b["duration"] = existing["duration"]
            # Carrying over old arbitrary cache values
            cur_cache = {k: v for k, v in existing.items() if k not in b.keys()}
            b.update(cur_cache)
        # Setting overloaded duration
        if duration:
            b["duration"] = duration

        # Apply the buff!
        self.buffcache[buffkey] = b

        # Create the buff instance and run the on-application hook method
        instance: Buff = buff(self, buffkey, b)
        instance.at_apply(**_context)
        if instance.ticking:
            tick_buff(self, buffkey, _context)

        # Clean up the buff at the end of its duration through a delayed cleanup call
        if b["duration"] > -1:
            utils.delay(b["duration"], self.cleanup, persistent=True)

    # region removers
    def remove(
        self, key, stacks=0, loud=True, dispel=False, expire=False, context=None
    ):
        """Remove a buff or effect with matching key from this object. Normally calls at_remove,
        calls at_expire if the buff expired naturally, and optionally calls at_dispel. Can also
        remove stacks instead of the entire buff (still calls at_remove). Typically called via a helper method
        on the buff instance, or other methods on the handler.

        Args:
            key:        The buff key
            loud:       (optional) Calls at_remove when True. (default: True)
            dispel:     (optional) Calls at_dispel when True. (default: False)
            expire:     (optional) Calls at_expire when True. (default: False)
            context:    (optional) A dictionary you wish to pass to the at_remove/at_dispel/at_expire method as kwargs
        """
        if not context:
            context = {}
        if key not in self.buffcache:
            return

        buff: Buff = self.buffcache[key]
        instance: Buff = buff["ref"](self, key, buff)

        if loud:
            if dispel:
                instance.at_dispel(**context)
            elif expire:
                instance.at_expire(**context)
            instance.at_remove(**context)

        del instance
        if not stacks:
            del self.buffcache[key]
        elif stacks:
            self.buffcache[key]["stacks"] -= stacks
            if self.buffcache[key]["stacks"] <= 0:
                del self.buffcache[key]

    def remove_by_type(
        self,
        bufftype: Buff,
        loud=True,
        dispel=False,
        expire=False,
        context=None,
    ):
        """Removes all buffs of a specified type from this object. Functionally similar to remove, but takes a type instead.

        Args:
            bufftype:   The buff class to remove
            loud:       (optional) Calls at_remove when True. (default: True)
            dispel:     (optional) Calls at_dispel when True. (default: False)
            expire:     (optional) Calls at_expire when True. (default: False)
            context:    (optional) A dictionary you wish to pass to the at_remove/at_dispel/at_expire method as kwargs
        """
        _remove = self.get_by_type(bufftype)
        if not _remove:
            return
        self._remove_via_dict(_remove, loud, dispel, expire, context)

    def remove_by_stat(
        self,
        stat,
        loud=True,
        dispel=False,
        expire=False,
        context=None,
    ):
        """Removes all buffs modifying the specified stat from this object.

        Args:
            stat:       The stat string to search for
            loud:       (optional) Calls at_remove when True. (default: True)
            dispel:     (optional) Calls at_dispel when True. (default: False)
            expire:     (optional) Calls at_expire when True. (default: False)
            context:    (optional) A dictionary you wish to pass to the at_remove/at_dispel/at_expire method as kwargs
        """
        _remove = self.get_by_stat(stat)
        if not _remove:
            return
        self._remove_via_dict(_remove, loud, dispel, expire, context)

    def remove_by_trigger(
        self,
        trigger,
        loud=True,
        dispel=False,
        expire=False,
        context=None,
    ):
        """Removes all buffs with the specified trigger from this object.

        Args:
            trigger:    The stat string to search for
            loud:       (optional) Calls at_remove when True. (default: True)
            dispel:     (optional) Calls at_dispel when True. (default: False)
            expire:     (optional) Calls at_expire when True. (default: False)
            context:    (optional) A dictionary you wish to pass to the at_remove/at_dispel/at_expire method as kwargs
        """
        _remove = self.get_by_trigger(trigger)
        if not _remove:
            return
        self._remove_via_dict(_remove, loud, dispel, expire, context)

    def remove_by_source(
        self,
        source,
        loud=True,
        dispel=False,
        expire=False,
        context=None,
    ):
        """Removes all buffs from the specified source from this object.

        Args:
            source:     The source to search for
            loud:       (optional) Calls at_remove when True. (default: True)
            dispel:     (optional) Calls at_dispel when True. (default: False)
            expire:     (optional) Calls at_expire when True. (default: False)
            context:    (optional) A dictionary you wish to pass to the at_remove/at_dispel/at_expire method as kwargs
        """
        _remove = self.get_by_source(source)
        if not _remove:
            return
        self._remove_via_dict(_remove, loud, dispel, expire, context)

    def remove_by_cachevalue(
        self,
        key,
        value=None,
        loud=True,
        dispel=False,
        expire=False,
        context=None,
    ):
        """Removes all buffs with the cachevalue from this object. Functionally similar to remove, but checks the buff's cache values instead.

        Args:
            key:         The key of the cache value to check
            value:      (optional) The value to match to. If None, merely checks to see if the value exists
            loud:       (optional) Calls at_remove when True. (default: True)
            dispel:     (optional) Calls at_dispel when True. (default: False)
            expire:     (optional) Calls at_expire when True. (default: False)
            context:    (optional) A dictionary you wish to pass to the at_remove/at_dispel/at_expire method as kwargs
        """
        _remove = self.get_by_cachevalue(key, value)
        if not _remove:
            return
        self._remove_via_dict(_remove, loud, dispel, expire, context)

    def clear(self, loud=True, dispel=False, expire=False, context=None):
        """Removes all buffs on this handler"""
        cache = self.all
        self._remove_via_dict(cache, loud, dispel, expire, context)

    # endregion
    # region getters
    def get(self, key: str):
        """If the specified key is on this handler, return the instanced buff. Otherwise return None.
        You should delete this when you're done with it, so that garbage collection doesn't have to.

        Args:
            key:    The key for the buff you wish to get"""
        buff = self.buffcache.get(key)
        if buff:
            return buff["ref"](self, key, buff)
        else:
            return None

    def get_all(self):
        """Returns a dictionary of instanced buffs (all of them) on this handler in the format {buffkey: instance}"""
        _cache = dict(self.buffcache)
        if not _cache:
            return {}
        return {k: buff["ref"](self, k, buff) for k, buff in _cache.items()}

    def get_by_type(self, buff: Buff, to_filter=None):
        """Finds all buffs matching the given type.

        Args:
            buff:       The buff class to search for
            to_filter:  (optional) A dictionary you wish to slice. If not provided, uses the whole buffcache.

        Returns a dictionary of instanced buffs of the specified type in the format {buffkey: instance}.
        """
        _cache = self.get_all() if not to_filter else to_filter
        return {k: _buff for k, _buff in _cache.items() if isinstance(_buff, buff)}

    def get_by_stat(self, stat: str, to_filter=None):
        """Finds all buffs which contain a Mod object that modifies the specified stat.

        Args:
            stat:       The string identifier to find relevant mods
            to_filter:  (optional) A dictionary you wish to slice. If not provided, uses the whole buffcache.

        Returns a dictionary of instanced buffs which modify the specified stat in the format {buffkey: instance}.
        """
        _cache = self.traits if not to_filter else to_filter
        buffs = {
            k: buff for k, buff in _cache.items() for m in buff.mods if m.stat == stat
        }
        return buffs

    def get_by_trigger(self, trigger: str, to_filter=None):
        """Finds all buffs with the matching string in their triggers.

        Args:
            trigger:    The string identifier to find relevant buffs
            to_filter:  (optional) A dictionary you wish to slice. If not provided, uses the whole buffcache.

        Returns a dictionary of instanced buffs which fire off the designated trigger, in the format {buffkey: instance}.
        """
        _cache = self.effects if not to_filter else to_filter
        buffs = {k: buff for k, buff in _cache.items() if trigger in buff.triggers}
        return buffs

    def get_by_source(self, source, to_filter=None):
        """Find all buffs with the matching source.

        Args:
            source: The source you want to filter buffs by
            to_filter:  (optional) A dictionary you wish to slice. If not provided, uses the whole buffcache.

        Returns a dictionary of instanced buffs which came from the provided source, in the format {buffkey: instance}.
        """
        _cache = self.all if not to_filter else to_filter
        buffs = {k: buff for k, buff in _cache.items() if buff.source == source}
        return buffs

    def get_by_cachevalue(self, key, value=None, to_filter=None):
        """Find all buffs with a matching {key: value} pair in its cache. Allows you to search buffs by arbitrary cache values

        Args:
            key:    The key of the cache value to check
            value:  (optional) The value to match to. If None, merely checks to see if the value exists
            to_filter:  (optional) A dictionary you wish to slice. If not provided, uses the whole buffcache.

        Returns a dictionary of instanced buffs with cache values matching the specified value, in the format {buffkey: instance}.
        """
        _cache = self.all if not to_filter else to_filter
        if not value:
            buffs = {k: buff for k, buff in _cache.items() if buff.cache.get(key)}
        elif value:
            buffs = {
                k: buff for k, buff in _cache.items() if buff.cache.get(key) == value
            }
        return buffs

    # endregion

    def has(self, buff=None) -> bool:
        """Checks if the specified buff type or key exists on the handler.

        Args:
            buff:   The buff to search for. This can be a string (the key) or a class reference (the buff type)

        Returns a bool. If no buff and no key is specified, returns False."""
        if not buff:
            return False
        if not (isinstance(buff, type) or isinstance(buff, str)):
            raise TypeError

        if isinstance(buff, str):
            for k in self.buffcache.keys():
                if k == buff:
                    return True
        if isinstance(buff, type):
            for b in self.buffcache.values():
                if b.get("ref") == buff:
                    return True
        return False

    def check(
        self,
        value: float,
        stat: str,
        loud=True,
        context=None,
        trigger=False,
        strongest=False,
    ):
        """Finds all buffs and perks related to a stat and applies their effects.

        Args:
            value:  The value you intend to modify
            stat:   The string that designates which stat buffs you want
            loud:   (optional) Call the buff's at_post_check method after checking (default: True)
            context: (optional) A dictionary you wish to pass to the at_pre_check/at_post_check and conditional methods as kwargs
            trigger: (optional) Trigger buffs with the `stat` string as well. (default: False)
            strongest:  (optional) Applies only the strongest mods of the corresponding stat value (default: False)

        Returns the value modified by relevant buffs."""
        # Buff cleanup to make sure all buffs are valid before processing
        self.cleanup()

        # Find all buffs and traits related to the specified stat.
        if not context:
            context = {}
        applied = self.get_by_stat(stat)
        if not applied:
            return value

        # Run pre-check hooks on related buffs
        for buff in applied.values():
            buff.at_pre_check(**context)

        # Sift out buffs that won't be applying their mods (paused, conditional)
        applied = {
            k: buff
            for k, buff in applied.items()
            if buff.conditional(**context)
            if not buff.paused
        }

        # The mod totals
        calc = self._calculate_mods(stat, applied)

        # The calculated final value
        final = self._apply_mods(value, calc, strongest=strongest)

        # Run the "after check" functions on all relevant buffs
        for buff in applied.values():
            buff: Buff
            if loud:
                buff.at_post_check(**context)
            del buff

        # If you want to, also trigger buffs with the same stat string
        if trigger:
            self.trigger(stat, context)

        return final

    def trigger(self, trigger: str, context: dict = None):
        """Calls the at_trigger method on all buffs with the matching trigger.

        Args:
            trigger:    The string identifier to find relevant buffs. Passed to the at_trigger method.
            context:    (optional) A dictionary you wish to pass to the at_trigger method as kwargs
        """
        self.cleanup()
        _effects = self.get_by_trigger(trigger)
        if not _effects:
            return
        if not context:
            context = {}

        _to_trigger = {
            k: buff
            for k, buff in _effects.items()
            if buff.conditional(**context)
            if not buff.paused
            if trigger in buff.triggers
        }

        # Trigger all buffs whose trigger matches the trigger string
        for buff in _to_trigger.values():
            buff: Buff
            buff.at_trigger(trigger, **context)

    def pause(self, key: str, context=None):
        """Pauses the buff. This excludes it from being checked for mods, triggered, or cleaned up. Used to make buffs 'playtime' instead of 'realtime'.

        Args:
            key:    The key for the buff you wish to pause
            context:    (optional) A dictionary you wish to pass to the at_pause method as kwargs
        """
        if key in self.buffcache.keys():
            # Mark the buff as paused
            buff = dict(self.buffcache.get(key))
            if buff["paused"]:
                return
            if not context:
                context = {}
            buff["paused"] = True

            # Math assignments
            current = time.time()  # Current Time
            start = buff["start"]  # Start
            duration = buff["duration"]  # Duration
            prevtick = buff["prevtick"]  # Previous tick timestamp
            tickrate = buff["tickrate"]  # Buff's tick rate
            end = start + duration  # End

            # Setting "tickleft"
            if buff["ref"].ticking:
                buff["tickleft"] = max(1, tickrate - (current - prevtick))

            # Setting the new duration (if applicable)
            if duration > -1:
                newduration = end - current  # New duration
                if newduration > 0:
                    buff["duration"] = newduration
                else:
                    self.remove(key)

            # Apply new cache info, call pause hook
            self.buffcache[key] = buff
            instance: Buff = buff["ref"](self, key, buff)
            instance.at_pause(**context)

    def unpause(self, key: str, context=None):
        """Unpauses a buff. This makes it visible to the various buff systems again.

        Args:
            key:    The key for the buff you wish to pause
            context:    (optional) A dictionary you wish to pass to the at_unpause method as kwargs
        """
        if key in self.buffcache.keys():
            # Mark the buff as unpaused
            buff = dict(self.buffcache.get(key))
            if not buff["paused"]:
                return
            if not context:
                context = {}
            buff["paused"] = False

            # Math assignments
            tickrate = buff["ref"].tickrate
            if buff["ref"].ticking:
                tickleft = buff["tickleft"]
            current = time.time()  # Current Time

            # Start our new timer, adjust prevtick
            buff["start"] = current
            if buff["ref"].ticking:
                buff["prevtick"] = current - (tickrate - tickleft)

            # Apply new cache info, call hook
            self.buffcache[key] = buff
            instance: Buff = buff["ref"](self, key, buff)
            instance.at_unpause(**context)

            # Set up typical delays (cleanup/ticking)
            if instance.duration > -1:
                utils.delay(buff["duration"], cleanup_buffs, self, persistent=True)
            if instance.ticking:
                utils.delay(
                    tickrate,
                    tick_buff,
                    handler=self,
                    buffkey=key,
                    initial=False,
                    persistent=True,
                )

    def view(self, to_filter=None) -> dict:
        """Returns a buff flavor text as a dictionary of tuples in the format {key: (name, flavor)}. Common use for this is a buff readout of some kind.

        Args:
            to_filter:  (optional) The dictionary of buffs to iterate over. If none is provided, returns all buffs (default: None)
        """
        if not isinstance(to_filter, dict):
            raise TypeError
        self.cleanup()
        _cache = self.visible if not to_filter else to_filter
        _flavor = {k: (buff.name, buff.flavor) for k, buff in _cache.items()}
        return _flavor

    def view_modifiers(self, stat: str, context=None):
        """Checks all modifiers of the specified stat without actually applying them. Hits the conditional hook for relevant buffs.

        Args:
            stat:   The mod identifier string to search for
            context:    (optional) A dictionary you wish to pass to the conditional hooks as kwargs

        Returns a nested dictionary. The first layer's keys represent the type of modifier ('add' and 'mult'),
        and the second layer's keys represent the type of value ('total' and 'strongest').
        """
        # Buff cleanup to make sure all buffs are valid before processing
        self.cleanup()

        # Find all buffs and traits related to the specified stat.
        if not context:
            context = {}
        applied = self.get_by_stat(stat)
        if not applied:
            return None

        # Sift out buffs that won't be applying their mods (paused, conditional)
        applied = {
            k: buff
            for k, buff in applied.items()
            if buff.conditional(**context)
            if not buff.paused
        }

        # Calculate and return our values dictionary
        calc = self._calculate_mods(stat, applied)
        return calc

    def cleanup(self):
        """Removes expired buffs, ensures pause state is respected."""
        self._validate_state()
        cleanup_buffs(self)

    # region private methods
    def _validate_state(self):
        """Validates the state of paused/unpaused playtime buffs."""
        if not self.autopause:
            return
        if self.owner.has_account:
            self._unpause_playtime()
        elif not self.owner.has_account:
            self._pause_playtime()

    def _pause_playtime(self, sender=owner, **kwargs):
        """Pauses all playtime buffs when attached object is unpuppeted."""
        if sender != self.owner:
            return
        buffs = self.playtime
        if not buffs:
            return
        for buff in buffs.values():
            buff.pause()

    def _unpause_playtime(self, sender=owner, **kwargs):
        """Unpauses all playtime buffs when attached object is puppeted."""
        if sender != self.owner:
            return
        buffs = self.playtime
        if not buffs:
            return
        for buff in buffs.values():
            buff.unpause()
        pass

    def _calculate_mods(self, stat: str, buffs: dict):
        """Calculates the total value of applicable mods.

        Args:
            stat:   The string identifier to search mods for
            buffs:  The dictionary of buffs to calculate mods from

        Returns a nested dictionary. The first layer's keys represent the type of modifier ('add' and 'mult'),
        and the second layer's keys represent the type of value ('total' and 'strongest').
        """

        # The base return dictionary. If you update how modifiers are calculated, make sure to update this too, or you will get key errors!
        calculated = {
            "add": {"total": 0, "strongest": 0},
            "mult": {"total": 0, "strongest": 0},
            "div": {"total": 0, "strongest": 0},
        }
        if not buffs:
            return calculated

        for buff in buffs.values():
            for mod in buff.mods:
                buff: Buff
                mod: Mod
                if mod.stat == stat:
                    _modval = mod.value + ((buff.stacks) * mod.perstack)
                    calculated[mod.modifier]["total"] += _modval
                    if _modval > calculated[mod.modifier]["strongest"]:
                        calculated[mod.modifier]["strongest"] = _modval
        return calculated

    def _apply_mods(self, value, calc: dict, strongest=False):
        """Applies modifiers to a value.

        Args:
            value:  The value to modify
            calc:   The dictionary of calculated modifier values (see _calculate_mods)
            strongest:  (optional) Applies only the strongest mods of the corresponding stat value (default: False)

        Returns value modified by the relevant mods."""
        final = value
        if strongest:
            final = (
                (value + calc["add"]["strongest"])
                / max(1, 1.0 + calc["div"]["strongest"])
                * max(0, 1.0 + calc["mult"]["strongest"])
            )
        else:
            final = (
                (value + calc["add"]["total"])
                / max(1, 1.0 + calc["div"]["total"])
                * max(0, 1.0 + calc["mult"]["total"])
            )
        return final

    def _remove_via_dict(
        self, buffs: dict, loud=True, dispel=False, expire=False, context=None
    ):
        """Removes buffs within the provided dictionary from this handler. Used for remove methods besides the basic remove."""
        if not context:
            context = {}
        if not buffs:
            return
        for k, instance in buffs.items():
            instance: Buff
            if loud:
                if dispel:
                    instance.at_dispel(**context)
                elif expire:
                    instance.at_expire(**context)
                instance.at_remove(**context)
            del instance
            del self.buffcache[k]

    # endregion
    # endregion


def cleanup_buffs(handler: BuffHandler):
    """Cleans up all expired buffs from a handler."""
    _remove = handler.expired
    for v in _remove.values():
        v.remove(expire=True)


def tick_buff(handler: BuffHandler, buffkey: str, context=None, initial=True):
    """Ticks a buff. If a buff's tickrate is 1 or larger, this is called when the buff is applied, and then once per tick cycle.

    Args:
        handler:    The handler managing the ticking buff
        buffkey:    The key of the ticking buff
        context:    (optional) A dictionary you wish to pass to the at_tick method as kwargs
        initial:    (optional) Whether this tick_buff call is the first one. Starts True, changes to False for future ticks
    """
    # Cache a reference and find the buff on the object
    if buffkey not in handler.buffcache.keys():
        return
    if not context:
        context = {}

    # Instantiate the buff and tickrate
    buff: Buff = handler.get(buffkey)
    tr = max(1, buff.tickrate)

    # This stops the old ticking process if you refresh/stack the buff
    if (tr > time.time() - buff.prevtick and initial is not True) or buff.paused:
        return

    # Only fire the at_tick methods if the conditional is truthy
    if buff.conditional():
        # Always tick this buff on initial
        if initial:
            buff.at_tick(initial, **context)

        # Tick this buff one last time, then remove
        if buff.duration > -1 and buff.duration <= time.time() - buff.start:
            if tr < time.time() - buff.prevtick:
                buff.at_tick(initial, **context)
            buff.remove(expire=True)
            return

        # Tick this buff on-time
        if tr <= time.time() - buff.prevtick:
            buff.at_tick(initial, **context)

    handler.buffcache[buffkey]["prevtick"] = time.time()
    tr = max(1, buff.tickrate)

    # Recur this function at the tickrate interval, if it didn't stop/fail
    utils.delay(
        tr,
        tick_buff,
        handler=handler,
        buffkey=buffkey,
        context=context,
        initial=False,
        persistent=True,
    )
