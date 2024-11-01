"""
Describe command module.
"""

from evennia.utils.eveditor import EvEditor

from commands.command import Command


def _desc_load(caller):
    return caller.db.evmenu_target.db.desc or ""


def _desc_save(caller, buf):
    """
    Save line buffer to the desc prop. This should
    return True if successful and also report its status to the user.
    """
    caller.db.evmenu_target.db.desc = buf
    caller.msg("Saved.")
    return True


def _desc_quit(caller):
    caller.attributes.remove("evmenu_target")
    caller.msg("Exited editor.")


class CmdDescribe(Command):
    """
    Syntax: desc[/switch] [<obj> =] <description>

    Switches:
      edit - Open up a line editor for more advanced editing.
      del - Delete the description of an object. If another state is given, its
            description will be deleted.
      spring | summer | autumn | winter - room description to use in respective
                                          in-game season
      <other> - room description to use with an arbitrary room state.

    Sets the description an object. If an object is not given,
    describe the current room, potentially showing any additional stateful
    descriptions. The room states only work with rooms.

    Examples:
        desc/winter A cold winter scene.
        desc/edit/summer
        desc/burning This room is burning!
        desc A normal room with no state.
        desc/del/burning

    Rooms will automatically change season as the in-game time changes. You can
    set a specific room-state with the |wroomstate|n command.
    """

    key = "describe"
    aliases = ["desc"]
    switch_options = None
    locks = "cmd:perm(desc) or perm(Builder)"
    help_category = "Building"

    def parse(self):
        super().parse()

        self.delete_mode = "del" in self.switches
        self.edit_mode = not self.delete_mode and "edit" in self.switches

        self.object_mode = "=" in self.args

        # all other switches are names of room-states
        self.roomstates = [
            state for state in self.switches if state not in ("edit", "del")
        ]

    def edit_handler(self):
        if self.rhs:
            self.msg(
                "|rYou may specify a value, or use the edit switch, but not both.|n"
            )
            return
        if self.args:
            obj = self.caller.search(self.args)
        else:
            obj = self.caller.location or self.msg(
                "|rYou can't describe oblivion.|n"
            )
        if not obj:
            return

        if not (
            obj.access(self.caller, "control")
            or obj.access(self.caller, "edit")
        ):
            self.caller.msg(
                f"You don't have permission to edit the description of {obj.key}."
            )
            return

        self.caller.db.eveditor_target = obj
        self.caller.db.eveditor_roomstates = self.roomstates
        # launch the editor
        EvEditor(
            self.caller,
            loadfunc=_desc_load,
            savefunc=_desc_save,
            quitfunc=_desc_quit,
            key="desc",
            persistent=True,
        )
        return

    def show_stateful_descriptions(self):
        location = self.caller.location
        room_states = location.room_states
        season = location.get_season()
        time_of_day = location.get_time_of_day()
        stateful_descs = location.all_desc()

        output = [
            f"Room {location.get_display_name(self.caller)} "
            f"Season: {season}. Time: {time_of_day}. "
            f"States: {', '.join(room_states) if room_states else 'None'}"
        ]
        other_active = False
        for state, desc in stateful_descs.items():
            if state is None:
                continue
            if state == season or state in room_states:
                output.append(f"Room state |w{state}|n |g(active)|n:\n{desc}")
                other_active = True
            else:
                output.append(f"Room state |w{state}|n:\n{desc}")

        active = " |g(active)|n" if not other_active else ""
        output.append(f"Room state |w(default)|n{active}:\n{location.db.desc}")

        sep = "\n" + "-" * 78 + "\n"
        self.caller.msg(sep.join(output))

    def func(self):
        caller = self.caller
        if (
            not self.args
            and "edit" not in self.switches
            and "del" not in self.switches
        ):
            if caller.location:
                # show stateful descs on the room
                self.show_stateful_descriptions()
                return
            else:
                caller.msg("You have no location to describe!")
                return

        if self.edit_mode:
            self.edit_handler()
            return

        if self.object_mode:
            # We are describing an object
            target = caller.search(self.lhs)
            if not target:
                return
            desc = self.rhs or ""
        else:
            # we are describing the current room
            target = caller.location or self.msg(
                "|rYou don't have a location to describe.|n"
            )
            if not target:
                return
            desc = self.args

        roomstates = self.roomstates
        if target.access(self.caller, "control") or target.access(
            self.caller, "edit"
        ):
            if not roomstates or not hasattr(target, "add_desc"):
                # normal description
                target.db.desc = desc
                caller.msg(
                    f"The description was set on {target.get_display_name(caller)}."
                )
            elif roomstates:
                for roomstate in roomstates:
                    if self.delete_mode:
                        target.remove_desc(roomstate)
                        caller.msg(
                            f"The {roomstate}-description was deleted, if it existed."
                        )
                    else:
                        target.add_desc(desc, room_state=roomstate)
                        caller.msg(
                            f"The {roomstate}-description was set on"
                            f" {target.get_display_name(caller)}."
                        )
            else:
                target.db.desc = desc
                caller.msg(
                    f"The description was set on {target.get_display_name(caller)}."
                )
        else:
            caller.msg(
                "You don't have permission to edit the description "
                f"of {target.get_display_name(caller)}."
            )
