"""
Typeclass command module.
"""

from evennia.commands.default import building


class CmdTypeclass(building.CmdTypeclass):
    """
    Syntax: typeclass[/switch] <object> [= typeclass.path]
            typeclass/prototype <object> = prototype_key

            typeclasses or typeclass/list/show [typeclass.path]
            swap - this is a shorthand for using /force/reset flags.
            update - this is a shorthand for using the /force/reload flag.

    Switch:
        show, examine - display the current typeclass of object (default) or,
                        if given a typeclass path, show the docstring of that
                        typeclass.
        update - *only* re-run at_object_creation on this object
                 meaning locks or other properties set later may remain.
        reset - clean out *all* the attributes and properties on the object,
                basically making this a new clean object. This will also
                reset cmdsets!
        force - change to the typeclass also if the object already has a
                typeclass of the same name.
        list - show available typeclasses. Only typeclasses in modules actually
               imported or used from somewhere in the code will show up here
               (those typeclasses are still available if you know the path)
        prototype - clean and overwrite the object with the specified
                    prototype key - effectively making a whole new object.

    Example:
        type button = examples.red_button.RedButton
        type/prototype button=a red button

    If the typeclass_path is not given, the current object's typeclass is
    assumed.

    View or set an object's typeclass. If setting, the creation hooks of the
    new typeclass will be run on the object. If you have clashing properties on
    the old class, use /reset. By default you are protected from changing to a
    typeclass of the same name as the one you already have - use /force to
    override this protection.

    The given typeclass must be identified by its location using python
    dot-notation pointing to the correct module and class. If no typeclass is
    given (or a wrong typeclass is given). Errors in the path or new typeclass
    will lead to the old typeclass being kept. The location of the typeclass
    module is searched from the default typeclass directory, as defined in the
    server settings.
    """

    key = "typeclass"
    aliases = ["type", "parent", "swap", "update", "typeclasses"]
