"""
Detail command module.
"""

from commands.command import Command


class CmdDetail(Command):
    """
    sets a detail on a room

    Usage:
        detail[/del] <key> [= <description>]
        detail <key>;<alias>;... = description

    Example:
        detail
        detail walls = The walls are covered in ...
        detail castle;ruin;tower = The distant ruin ...
        detail/del wall
        detail/del castle;ruin;tower

    This command allows to show the current room details if you enter it
    without any argument.  Otherwise, sets or deletes a detail on the current
    room, if this room supports details like an extended room. To add new
    detail, just use the 'detail' command, specifying the key, an equal sign
    and the description.  You can assign the same description to several
    details using the alias syntax (replace key by alias1;alias2;alias3;...).
    To remove one or several details, use the @detail/del switch.
    """

    key = "detail"
    locks = "cmd:perm(Builder)"
    help_category = "Building"

    def func(self):
        location = self.caller.location
        if not self.args:
            details = location.db.details
            if not details:
                self.msg(
                    f"|rThe room {location.get_display_name(self.caller)} doesn't have any"
                    " details.|n"
                )
            else:
                details = sorted(
                    [
                        "|y{}|n: {}".format(key, desc)
                        for key, desc in details.items()
                    ]
                )
                self.msg("Details on Room:\n" + "\n".join(details))
            return

        if not self.rhs and "del" not in self.switches:
            detail = location.return_detail(self.lhs)
            if detail:
                self.msg(
                    "Detail '|y{}|n' on Room:\n{}".format(self.lhs, detail)
                )
            else:
                self.msg("Detail '{}' not found.".format(self.lhs))
            return

        method = "add_detail" if "del" not in self.switches else "remove_detail"
        if not hasattr(location, method):
            self.caller.msg("Details cannot be set on %s." % location)
            return
        for key in self.lhs.split(";"):
            # loop over all aliases, if any (if not, this will just be
            # the one key to loop over)
            getattr(location, method)(key, self.rhs)
        if "del" in self.switches:
            self.caller.msg(f"Deleted detail '{self.lhs}', if it existed.")
        else:
            self.caller.msg(f"Set detail '{self.lhs}': '{self.rhs}'")
