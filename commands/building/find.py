"""
Find command module.
"""

import re

from django.conf import settings
from django.db.models import Max, Min, Q
from evennia.objects.models import ObjectDB
from evennia.utils import utils
from evennia.utils.utils import dbref, inherits_from

from commands.command import Command
from server.conf import logger

CHAR_TYPECLASS = settings.BASE_CHARACTER_TYPECLASS
ROOM_TYPECLASS = settings.BASE_ROOM_TYPECLASS
EXIT_TYPECLASS = settings.BASE_EXIT_TYPECLASS


class CmdFind(Command):
    """
    Search the database for objects

    Usage:
      find[/switches] <name or dbref or *account> [= dbrefmin[-dbrefmax]]
      locate - this is a shorthand for using the /loc switch.

    Switches:
      room       - only look for rooms (location=None)
      exit       - only look for exits (destination!=None)
      char       - only look for characters (BASE_CHARACTER_TYPECLASS)
      exact      - only exact matches are returned.
      loc        - display object location if exists and match has one result
      startswith - search for names starting with the string, rather than containing

    Searches the database for an object of a particular name or exact #dbref.
    Use *accountname to search for an account. The switches allows for
    limiting object matches to certain game entities. Dbrefmin and dbrefmax
    limits matches to within the given dbrefs range, or above/below if only
    one is given.
    """

    key = "find"
    aliases = ["search", "locate", "where"]
    switch_options = ("room", "exit", "char", "exact", "loc", "startswith")
    locks = "cmd:perm(find) or perm(Builder)"
    help_category = "Building"

    def func(self):
        """Search functionality"""
        caller = self.caller
        switches = self.switches

        if not self.args or (not self.lhs and not self.rhs):
            caller.msg("Usage: find <string> [= low [-high]]")
            return

        if (
            "locate" in self.cmdstring
        ):  # Use option /loc as a default for locate command alias
            switches.append("loc")

        searchstring = self.lhs

        try:
            # Try grabbing the actual min/max id values by database aggregation
            qs = ObjectDB.objects.values("id").aggregate(
                low=Min("id"), high=Max("id")
            )
            low, high = sorted(qs.values())
            if not (low and high):
                raise ValueError(
                    f"{self.__class__.__name__}: Min and max ID not returned by aggregation;"
                    " falling back to queryset slicing."
                )
        except Exception as e:
            logger.log_trace(e)
            # If that doesn't work for some reason (empty DB?), guess the lower
            # bound and do a less-efficient query to find the upper.
            low, high = 1, ObjectDB.objects.all().order_by("-id").first().id

        if self.rhs:
            try:
                # Check that rhs is either a valid dbref or dbref range
                bounds = tuple(
                    sorted(
                        dbref(x, False)
                        for x in re.split("[-\s]+", self.rhs.strip())
                    )
                )

                # dbref() will return either a valid int or None
                assert bounds
                # None should not exist in the bounds list
                assert None not in bounds

                low = bounds[0]
                if len(bounds) > 1:
                    high = bounds[-1]

            except AssertionError:
                caller.msg("Invalid dbref range provided (not a number).")
                return
            except IndexError as e:
                logger.log_err(
                    f"{self.__class__.__name__}: Error parsing upper and lower bounds of query."
                )
                logger.log_trace(e)

        low = min(low, high)
        high = max(low, high)

        is_dbref = utils.dbref(searchstring)
        is_account = searchstring.startswith("*")

        restrictions = ""
        if self.switches:
            restrictions = ", %s" % ", ".join(self.switches)

        if is_dbref or is_account:
            if is_dbref:
                # a dbref search
                result = caller.search(
                    searchstring, global_search=True, quiet=True
                )
                string = "|wExact dbref match|n(#%i-#%i%s):" % (
                    low,
                    high,
                    restrictions,
                )
            else:
                # an account search
                searchstring = searchstring.lstrip("*")
                result = caller.search_account(searchstring, quiet=True)
                string = "|wMatch|n(#%i-#%i%s):" % (low, high, restrictions)

            if "room" in switches:
                result = (
                    result if inherits_from(result, ROOM_TYPECLASS) else None
                )
            if "exit" in switches:
                result = (
                    result if inherits_from(result, EXIT_TYPECLASS) else None
                )
            if "char" in switches:
                result = (
                    result if inherits_from(result, CHAR_TYPECLASS) else None
                )

            if not result:
                string += "\n   |RNo match found.|n"
            elif not low <= int(result[0].id) <= high:
                string += f"\n   |RNo match found for '{searchstring}' in #dbref interval.|n"
            else:
                result = result[0]
                string += (
                    f"\n|g   {result.get_display_name(caller)}"
                    f"{result.get_extra_display_name_info(caller)} - {result.path}|n"
                )
                if (
                    "loc" in self.switches
                    and not is_account
                    and result.location
                ):
                    string += (
                        f" (|wlocation|n: |g{result.location.get_display_name(caller)}"
                        f"{result.get_extra_display_name_info(caller)}|n)"
                    )
        else:
            # Not an account/dbref search but a wider search; build a queryset.
            # Searches for key and aliases
            if "exact" in switches:
                keyquery = Q(
                    db_key__iexact=searchstring, id__gte=low, id__lte=high
                )
                aliasquery = Q(
                    db_tags__db_key__iexact=searchstring,
                    db_tags__db_tagtype__iexact="alias",
                    id__gte=low,
                    id__lte=high,
                )
            elif "startswith" in switches:
                keyquery = Q(
                    db_key__istartswith=searchstring, id__gte=low, id__lte=high
                )
                aliasquery = Q(
                    db_tags__db_key__istartswith=searchstring,
                    db_tags__db_tagtype__iexact="alias",
                    id__gte=low,
                    id__lte=high,
                )
            else:
                keyquery = Q(
                    db_key__icontains=searchstring, id__gte=low, id__lte=high
                )
                aliasquery = Q(
                    db_tags__db_key__icontains=searchstring,
                    db_tags__db_tagtype__iexact="alias",
                    id__gte=low,
                    id__lte=high,
                )

            # Keep the initial queryset handy for later reuse
            result_qs = ObjectDB.objects.filter(
                keyquery | aliasquery
            ).distinct()
            nresults = result_qs.count()

            # Use iterator to minimize memory ballooning on large result sets
            results = result_qs.iterator()

            # Check and see if type filtering was requested; skip it if not
            if any(x in switches for x in ("room", "exit", "char")):
                obj_ids = set()
                for obj in results:
                    if (
                        (
                            "room" in switches
                            and inherits_from(obj, ROOM_TYPECLASS)
                        )
                        or (
                            "exit" in switches
                            and inherits_from(obj, EXIT_TYPECLASS)
                        )
                        or (
                            "char" in switches
                            and inherits_from(obj, CHAR_TYPECLASS)
                        )
                    ):
                        obj_ids.add(obj.id)

                # Filter previous queryset instead of requesting another
                filtered_qs = result_qs.filter(id__in=obj_ids).distinct()
                nresults = filtered_qs.count()

                # Use iterator again to minimize memory ballooning
                results = filtered_qs.iterator()

            # still results after type filtering?
            if nresults:
                if nresults > 1:
                    header = f"{nresults} Matches"
                else:
                    header = "One Match"

                string = f"|w{header}|n(#{low}-#{high}{restrictions}):"
                res = None
                for res in results:
                    string += (
                        "\n  "
                        f" |g{res.get_display_name(caller)}"
                        f"{res.get_extra_display_name_info(caller)} -"
                        f" {res.path}|n"
                    )
                if (
                    "loc" in self.switches
                    and nresults == 1
                    and res
                    and getattr(res, "location", None)
                ):
                    string += (
                        " (|wlocation|n:"
                        f" |g{res.location.get_display_name(caller)}"
                        f"{res.get_extra_display_name_info(caller)}|n)"
                    )
            else:
                string = f"|wNo Matches|n(#{low}-#{high}{restrictions}):"
                string += f"\n   |RNo matches found for '{searchstring}'|n"

        # send result
        caller.msg(string.strip())
