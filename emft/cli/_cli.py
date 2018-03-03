# coding=utf-8
"""
Command line interface
"""

import shutil
from filecmp import dircmp
from pathlib import Path

import click
import elib
from emiz.new_miz import NewMiz

from emft import __version__, mission_file
from ._print_version import print_version
from emft.config import CONFIG
from emft.context import CONTEXT
from emft.exit_ import exit_
from ._setup_repo import setup_repo
from ._updater import update

LOGGER = elib.custom_logging.get_logger('EMFT')


def mirror_dir(src: Path, dst: Path):
    """
    Propagates difference between the original lua tables and the re-ordered one

    Args:
        src: source folder
        dst: destination folder
    """
    ignore = ['mission', 'mapResource', 'dictionary']
    LOGGER.debug(f'mirroring: {src} -> {dst}')

    LOGGER.debug('comparing directories')
    diff = dircmp(str(src), str(dst), ignore)

    diff_list = diff.left_only + diff.diff_files
    LOGGER.debug(f'differences: {diff_list}')

    for _diff in diff_list:
        source = Path(diff.left, _diff)
        target = Path(diff.right, _diff)
        LOGGER.debug(f'looking at: {_diff}')
        if source.is_dir():
            LOGGER.debug('isdir: {}'.format(_diff))
            if not target.exists():
                LOGGER.debug(f'creating: {_diff}')
                target.mkdir()
            mirror_dir(source, target)
        else:
            LOGGER.debug(f'copying: {_diff}')
            shutil.copy2(str(source), diff.right)
    for sub in diff.subdirs.values():
        assert isinstance(sub, dircmp)
        mirror_dir(sub.left, sub.right)


@click.command('recompose')
@click.option('-f', '--filename',
              type=click.Path(dir_okay=False, writable=True, readable=True),
              default='output.miz',
              show_default=True,
              help='Resulting MIZ file')
def _recompose(filename: str):
    """
    Recreates a MIZ file
    """
    if not filename.endswith('.miz'):
        filename = f'{filename}.miz'
    filename = Path(filename).absolute()
    path = Path('.').absolute()
    LOGGER.info(f'recomposing mission from "{path}" into "{filename}"')
    Path(filename).touch()
    NewMiz.recompose(path, filename)


def _setup_logging():
    if CONTEXT.debug:
        elib.custom_logging.set_handler_level('EMFT', 'ch', 'debug')
        LOGGER.debug('debug mode is active')
    else:
        elib.custom_logging.set_handler_level('EMFT', 'ch', 'info')


def _decompose():
    setup_repo()
    mission = mission_file.get_latest_miz_file_in_source_folder()
    if mission:
        LOGGER.info(f'decomposing mission: "{mission}"')
        NewMiz.decompose(mission, Path('.').absolute())
        LOGGER.info('all done!')
        exit_(0)
    else:
        LOGGER.error('no mission file found')
        exit_(1)


@click.group(invoke_without_command=True)
@click.option('-d', '--debug',
              default=False,
              is_flag=True,
              show_default=True,
              help='More console output')
@click.option('-v', '--version',
              is_flag=True,
              is_eager=True,
              expose_value=False,
              callback=print_version,
              help='Print version and exit')
@click.pass_context
def cli(ctx: click.Context, debug: bool = False):
    """
    Decomposes a MIZ file into its components
    """
    CONTEXT.debug = debug or CONFIG.debug
    CONTEXT.source_folder = CONFIG.source_folder
    CONTEXT.appveyor = CONFIG.appveyor
    _setup_logging()
    LOGGER.debug(f'EMFT {__version__}')
    update()
    if ctx.invoked_subcommand is None:
        ctx.invoke(_decompose)


cli.add_command(_recompose)
