# coding=utf-8
"""
Command line interface
"""

import click
import elib

from emft import __version__
from emft.config import CONFIG
from emft.context import CONTEXT

LOGGER = elib.custom_logging.get_logger('EMFT', use_click_handler=True, log_to_file=True)
elib.custom_logging.set_root_logger(LOGGER)


@click.group(invoke_without_command=True)
@click.option('-d', '--debug', help='More console output', default=False, show_default=True)
def cli(debug: bool = False):
    """
    Main CLI entry-point
    """
    CONTEXT.debug = debug or CONFIG.debug
    if CONTEXT.debug:
        elib.custom_logging.set_handler_level('EMFT', 'ch', 'debug')
    LOGGER.debug(f'EMFT {__version__}')
