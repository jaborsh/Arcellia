"""
Search and multimatch handling

This module allows for overloading two functions used by Evennia's
search functionality:

    at_search_result:
        This is called whenever a result is returned from an object
        search (a common operation in commands).  It should (together
        with at_multimatch_input below) define some way to present and
        differentiate between multiple matches (by default these are
        presented as 1-ball, 2-ball etc)
    at_multimatch_input:
        This is called with a search term and should be able to
        identify if the user wants to separate a multimatch-result
        (such as that from a previous search). By default, this
        function understands input on the form 1-ball, 2-ball etc as
        indicating that the 1st or 2nd match for "ball" should be
        used.

This module is not called by default, to use it, add the following
line to your settings file:

    SEARCH_AT_RESULT = "server.conf.at_search.at_search_result"

"""

from enum import Enum

from django.conf import settings
from django.utils.translation import gettext as _

_MULTIMATCH_TEMPLATE = settings.SEARCH_MULTIMATCH_TEMPLATE


class SearchReturnType(Enum):
    DEFAULT = 1
    ALL = 2
    ONE = 3
    MULTIPLE = 4


def at_search_result(matches, caller, query="", quiet=False, **kwargs):
    """
    This is a generic hook for handling all processing of a search
    result, including error reporting.

    Args:
        matches (list): This is a list of 0, 1 or more typeclass instances,
            the matched result of the search. If 0, a nomatch error should
            be echoed, and if >1, multimatch errors should be given. Only
            if a single match should the result pass through.
        caller (Object): The object performing the search and/or which should
        receive error messages.
    query (str, optional): The search query used to produce `matches`.
        quiet (bool, optional): If `True`, no messages will be echoed to caller
            on errors.

    Keyword Args:
        nofound_string (str): Replacement string to echo on a notfound error.
        multimatch_string (str): Replacement string to echo on a multimatch error.

    Returns:
        processed_result (Object or None): This is always a single result
            or `None`. If `None`, any error reporting/handling should
            already have happened.

    """

    error = ""
    if not matches:
        # no results.
        error = kwargs.get("nofound_string") or _("Could not find '{query}'.").format(
            query=query
        )
        matches = None
    elif len(matches) > 1:
        return_quantity = kwargs.get("return_quantity", 1)
        return_type = kwargs.get("return_type", SearchReturnType.DEFAULT)
        if return_type == SearchReturnType.ONE:
            return matches[return_quantity - 1]
        elif return_type == SearchReturnType.MULTIPLE:
            matches = matches[:return_quantity]
            return matches
        elif return_type == SearchReturnType.ALL:
            return matches

        multimatch_string = kwargs.get("multimatch_string")
        if multimatch_string:
            error = "%s\n" % multimatch_string
        else:
            error = _(
                "More than one match for '{query}' (please narrow target):\n"
            ).format(query=query)

        for num, result in enumerate(matches):
            # we need to consider that result could be a Command, where .aliases
            # is a list of strings
            if hasattr(result.aliases, "all"):
                # result is a typeclassed entity where `.aliases` is an AliasHandler.
                aliases = result.aliases.all(return_objs=True)
                # remove pluralization aliases
                aliases = [
                    alias.db_key
                    for alias in aliases
                    if alias.db_category != "plural_key"
                ]
            else:
                # result is likely a Command, where `.aliases` is a list of strings.
                aliases = result.aliases

            error += _MULTIMATCH_TEMPLATE.format(
                number=num + 1,
                name=(
                    result.get_display_name(caller)
                    if hasattr(result, "get_display_name")
                    else query
                ),
                aliases=" [{alias}]".format(alias=";".join(aliases)) if aliases else "",
                info=result.get_extra_info(caller),
            )
        matches = None
    else:
        # exactly one match
        matches = matches[0]

    if error and not quiet:
        caller.msg(error.strip())
    return matches
