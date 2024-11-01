"""
Tickers command module.
"""

from evennia.commands.default import system


class CmdTickers(system.CmdTickers):
    """
    Syntax: tickers

    Note: Tickers are created, stopped and manipulated in Python code
    using the TickerHandler. This is merely a convenience function for
    inspecting the current status.
    """

    key = "tickers"
    help_category = "Building"
    locks = "cmd:perm(tickers) or perm(Builder)"
