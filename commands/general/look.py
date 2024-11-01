from django.conf import settings
from evennia.commands.default import general
from evennia.utils import (
    utils,
)

from server.conf.at_search import SearchReturnType

_AT_SEARCH_RESULT = utils.variable_from_module(
    *settings.SEARCH_AT_RESULT.rsplit(".", 1)
)


class CmdLook(general.CmdLook):
    """
    Syntax: look
            look <obj>
            look in <container>

    Observes your location or objects in your vicinity.
    """

    rhs_split = (" in ",)

    def look_detail(self):
        """
        Look for detail on room.
        """
        caller = self.caller
        if hasattr(self.caller.location, "get_detail"):
            detail = self.caller.location.get_detail(
                self.args, looker=self.caller
            )
            if detail:
                caller.location.msg_contents(
                    f"$You() $conj(look) closely at {self.args}.\n",
                    from_obj=caller,
                    exclude=caller,
                )
                caller.msg(detail)
                return True
        return False

    def func(self):
        """
        Handle the looking.
        """
        caller = self.caller
        if not self.args:
            target = caller.location
            if not target:
                caller.msg("You have no location to look at!")
                return
        else:
            # search, waiting to return errors so we can also check details
            target = caller.search(self.args, quiet=True)
            # if there's no target, check details
            if not target:
                # no target AND no detail means run the normal no-results message
                if not self.look_detail():
                    _AT_SEARCH_RESULT(target, caller, self.args, quiet=False)
                return
            # otherwise, run normal search result handling
            target = caller.search(self.args, return_type=SearchReturnType.ONE)
            if not target:
                return
        desc = caller.at_look(target)
        # add the type=look to the outputfunc to make it
        # easy to separate this output in client.
        self.msg(text=(desc, {"type": "look"}), options=None)
