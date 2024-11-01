"""
Spawn command module.
"""

from evennia.commands.default import building


class CmdSpawn(building.CmdSpawn):
    """
    Syntax: spawn[/noloc] <prototype_key>
            spawn[/noloc] <prototype_dict>

            spawn/search [prototype_keykey][;tag[,tag]]
            spawn/list [tag, tag, ...]
            spawn/list modules    - list only module-based prototypes
            spawn/show [<prototype_key>]
            spawn/update <prototype_key>

            spawn/save <prototype_dict>
            spawn/edit [<prototype_key>]
            olc     - equivalent to spawn/edit

    Switches:
        noloc - allow location to be None if not specified explicitly. Otherwise,
                location will default to caller's current location.
        search - search prototype by name or tags.
        list - list available prototypes, optionally limit by tags.
        show, examine - inspect prototype by key. If not given, acts like list.
        raw - show the raw dict of the prototype as a one-line string for manual editing.
        save - save a prototype to the database. It will be listable by /list.
        delete - remove a prototype from database, if allowed to.
        update - find existing objects with the same prototype_key and update
                 them with latest version of given prototype. If given with /save,
                 will auto-update all objects with the old version of the prototype
                 without asking first.
        edit, menu, olc - create/manipulate prototype in a menu interface.

    Example:
        spawn GOBLIN
        spawn {"key":"goblin", "typeclass":"monster.Monster", "location":"#2"}
        spawn/save {"key": "grunt", prototype: "goblin"};;mobs;edit:all()
    \f
    Dictionary keys:
      |wprototype_parent|n - name of parent prototype to use. Required if
                             typeclass is not set. Can be a path or a list for
                             multiple inheritance (inherits left to right). If
                             set one of the parents must have a typeclass.
      |wtypeclass       |n - string. Required if prototype_parent is not set.
      |wkey             |n - string, the main object identifier
      |wlocation        |n - this should be a valid object or #dbref
      |whome            |n - valid object or #dbref
      |wdestination     |n - only valid for exits (object or dbref)
      |wpermissions     |n - string or list of permission strings
      |wlocks           |n - a lock-string
      |waliases         |n - string or list of strings.
      |wndb_|n<name>       - value of a nattribute (ndb_ is stripped)

      |wprototype_key|n    - name of this prototype. Unique. Used to
                             store/retrieve from db and update existing
                             prototyped objects if desired.
      |wprototype_desc|n   - desc of this prototype. Used in listings
      |wprototype_locks|n  - locks of this prototype. Limits who may use prototype
      |wprototype_tags|n   - tags of this prototype. Used to find prototype

      any other keywords are interpreted as Attributes and their values.

    The available prototypes are defined globally in modules set in
    settings.PROTOTYPE_MODULES. If spawn is used without arguments it
    displays a list of available prototypes.
    """

    key = "spawn"
    aliases = ["olc"]
