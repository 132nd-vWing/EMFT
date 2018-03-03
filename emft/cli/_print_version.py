# coding=utf-8
"""
Prints current EMFT version
"""
import sys

import click

from emft import __version__


def print_version(ctx: click.Context, _, value):
    """
    Prints current version then exits
    """
    if not value or ctx.resilient_parsing:
        return

    click.secho(__version__, color='cyan')
    sys.exit(0)
