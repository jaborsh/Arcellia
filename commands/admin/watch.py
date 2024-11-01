from commands.command import Command
from server.conf import logger


class CmdWatch(Command):
    """
    Command to start watching a character.

    Usage:
      watch <character>

    This command allows an admin to start watching a character. Once
    watching, the admin will receive updates about the character's
    actions and movements.
    """

    key = "watch"
    aliases = ["snoop"]
    locks = "cmd:perm(Admin)"
    help_category = "Admin"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            if caller.ndb._watching:
                self._stop_watching(caller)
                return

            return self.msg("Syntax: watch <character>")

        target = caller.search(self.args.strip(), global_search=True)
        if not target:
            self.msg("Character not found.")
            return

        if caller == target:
            return self.msg("You cannot watch yourself.")
        elif (watching := target.ndb._watching or None) and caller == watching:
            return self.msg(f"{target.name} is already watching you.")

        if caller.ndb._watching:
            self._stop_watching(caller)

        self._start_watching(caller, target)

    def _start_watching(self, watcher, target):
        watcher.ndb._watching = target
        if not target.ndb._watchers:
            target.ndb._watchers = list()
        target.ndb._watchers.append(watcher)
        self.msg(f"You start watching {target.name}.")
        logger.log_info("%s started watching %s." % (watcher, target))

    def _stop_watching(self, watcher):
        target = watcher.ndb._watching
        target.ndb._watchers.remove(watcher)
        watcher.ndb._watching = None
        self.msg(f"You stop watching {target.name}.")
