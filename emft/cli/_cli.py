# coding=utf-8
"""
Command line interface
"""

import click
import elib

from emft import __version__, mission_file
from emft.config import CONFIG
from emft.context import CONTEXT
from emft.exit_ import exit_
from ._setup_repo import setup_repo
from ._updater import update

LOGGER = elib.custom_logging.get_logger('EMFT')


def _run():
    update()
    setup_repo()
    mission_file.get_latest_miz_file_in_source_folder()


def _setup_logging():
    if CONTEXT.debug:
        elib.custom_logging.set_handler_level('EMFT', 'ch', 'debug')
        LOGGER.debug('debug mode is active')
    else:
        elib.custom_logging.set_handler_level('EMFT', 'ch', 'info')


@click.group(invoke_without_command=True)
@click.option('-d', '--debug', help='More console output', default=False, is_flag=True, show_default=True)
def cli(debug: bool = False):
    """
    Main CLI entry-point
    """
    CONTEXT.debug = debug or CONFIG.debug
    CONTEXT.source_folder = CONFIG.source_folder
    CONTEXT.appveyor = CONFIG.appveyor
    _setup_logging()
    LOGGER.debug(f'EMFT {__version__}')
    _run()
    LOGGER.info('all done!')
    exit_(0)
