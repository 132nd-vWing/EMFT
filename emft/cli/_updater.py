# coding=utf-8
import sys

import elib

from emft import __version__


def update():
    logger = elib.custom_logging.get_logger('EMFT')
    if hasattr(sys, 'frozen'):
        logger.debug('running frozen EMFT')
        elib.updater.Updater('132nd-vWing/EMFT', __version__, 'emft.exe').update()
    else:
        logger.debug('running scripted EMFT')
