# coding=utf-8
"""
EMFT config
"""

from pathlib import Path

import elib


class _Val(elib.config.ConfigProp):

    def __get__(self, instance, owner=None):
        if self.parser is Path:
            return super(_Val, self).__get__(instance, owner).absolute()

        return super(_Val, self).__get__(instance, owner)


class Config(elib.config.BaseConfig):
    """
    EMFT config
    """

    debug: bool = _Val(bool, default='false')
    source_folder: bool = _Val(Path, default='false')
    appveyor: str = _Val(str)

    def __init__(self):
        elib.config.BaseConfig.__init__(self, 'EMFT')
