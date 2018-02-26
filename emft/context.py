# coding=utf-8
"""
Manages context
"""
from pathlib import Path

import elib


class _Val:

    def __init__(self, parser: callable):
        """
        Initialize properties of the descriptor.

        :param default: default value of the property if it isn't set yet
        :param parser:
        """
        self.parser = parser
        self.name = None
        self.owner = None

    def _value(self, instance):
        return self.parser(getattr(instance, '_data')[self.name])

    def __get__(self, instance, owner=None):
        if instance is None:
            return self

        if self.parser is Path:
            return self._value(instance).absolute()
        else:
            return self._value(instance)

    def __set__(self, instance, value):
        getattr(instance, '_data')[self.name] = self.parser(value)

    def __set_name__(self, owner, name):
        self.owner = owner
        self.name = name


class Context:
    """
    EMFT main context
    """
    debug: bool = _Val(bool)
    source_folder: Path = _Val(Path)
    branch: str = _Val(str)
    current_dir: Path = _Val(Path)
    repo: elib.repo.Repo = None
    appveyor: str = _Val(str)

    def __init__(self):
        self._data = {}


CONTEXT = Context()
