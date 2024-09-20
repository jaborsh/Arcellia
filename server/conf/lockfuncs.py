"""

Lockfuncs

Lock functions are functions available when defining lock strings,
which in turn limits access to various game systems.

All functions defined globally in this module are assumed to be
available for use in lockstrings to determine access. See the
Evennia documentation for more info on locks.

A lock function is always called with two arguments, accessing_obj and
accessed_obj, followed by any number of arguments. All possible
arguments should be handled with *args, **kwargs. The lock function
should handle all eventual tracebacks by logging the error and
returning False.

Lock functions in this module extend (and will overload same-named)
lock functions from evennia.locks.lockfuncs.

"""

# this is more efficient than multiple if ... elif statments
CF_MAPPING = {
    "eq": lambda val1, val2: val1 == val2
    or str(val1) == str(val2)
    or float(val1) == float(val2),
    "gt": lambda val1, val2: float(val1) > float(val2),
    "lt": lambda val1, val2: float(val1) < float(val2),
    "ge": lambda val1, val2: float(val1) >= float(val2),
    "le": lambda val1, val2: float(val1) <= float(val2),
    "ne": lambda val1, val2: float(val1) != float(val2),
    "default": lambda val1, val2: False,
}


def stat(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Usage:
      stat(statname)
      stat(statname, value)
      stat(statname, value, compare=type)

    where compare's type is one of (eq,gt,lt,ge,le,ne) and signifies
    how the value should be compared with one on accessing_obj (so
    compare=gt means the accessing_obj must have a value greater than
    the one given).

    Searches attributes *and* properties stored on the accessing_obj.
    if accessing_obj has a property "obj", then this is used as
    accessing_obj (this makes this usable for Commands too)

    The first form works like a flag - if the attribute/property
    exists on the object, the value is checked for True/False. The
    second form also requires that the value of the attribute/property
    matches. Note that all retrieved values will be converted to
    strings before doing the comparison.
    """
    # deal with arguments
    if not args:
        return False
    stat = args[0].strip()
    value = None
    if len(args) > 1:
        value = args[1].strip()
    compare = "eq"
    if kwargs:
        compare = kwargs.get("compare", "eq")

    def valcompare(val1, val2, typ="eq"):
        "compare based on type"
        try:
            return CF_MAPPING.get(typ, CF_MAPPING["default"])(val1, val2)
        except Exception:
            # this might happen if we try to compare two things that
            # cannot be compared
            return False

    if hasattr(accessing_obj, "obj"):
        # NOTE: this is relevant for Commands. It may clash with scripts
        # (they have Attributes and .obj) , but are scripts really
        # used so that one ever wants to check the property on the
        # Script rather than on its owner?
        accessing_obj = accessing_obj.obj

    # first, look for normal properties on the object trying to gain access
    if accessing_obj.stats.has(stat):
        if value:
            return valcompare(
                str(accessing_obj.stats.get(stat).current), value, compare
            )
        # will return Fail on False value etc
        return bool(accessing_obj.stats.has(stat))

    return False


def stat_gt(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Usage:
       stat_gt(statname, value)

    Only true if accessing_obj's stat > the value given.
    """
    return stat(accessing_obj, accessed_obj, *args, **{"compare": "gt"})


def stat_ge(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Usage:
       stat_ge(statname, value)

    Only true if accessing_obj's stat >= the value given.
    """
    return stat(accessing_obj, accessed_obj, *args, **{"compare": "ge"})


def stat_lt(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Usage:
       stat_lt(statname, value)

    Only true if accessing_obj's stat < the value given.
    """
    return stat(accessing_obj, accessed_obj, *args, **{"compare": "lt"})


def stat_le(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Usage:
       stat_le(statname, value)

    Only true if accessing_obj's stat <= the value given.
    """
    return stat(accessing_obj, accessed_obj, *args, **{"compare": "le"})


def stat_ne(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Usage:
       stat_ne(statname, value)

    Only true if accessing_obj's stat != the value given.
    """
    return stat(accessing_obj, accessed_obj, *args, **{"compare": "ne"})
