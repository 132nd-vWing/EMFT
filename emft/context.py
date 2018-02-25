# coding=utf-8
"""
Manages context
"""
import elib

_LOGGER = elib.custom_logging.get_logger('EMFT')

_DEFAULT = {
    'debug': False,
}


class _Val:

    def __init__(self, parser: callable):
        self.name = None
        self.owner = None
        self.parser = parser

    def _get_default(self):
        if self.name in _DEFAULT:
            return _DEFAULT[self.name]

        _LOGGER.error(f'missing value in configuration: {self.name}')

    def __get__(self, instance, owner):
        if not instance:
            return self

        if owner is not self.owner:
            raise RuntimeError(f'owners differ: "{owner}" vs "{self.owner}"')

        try:
            return getattr(instance, '_data')[self.name]
        except KeyError:
            return self._get_default()

    def __set_name__(self, owner, name):
        self.name = name
        self.owner = owner


class Context:
    """
    EMFT main context
    """
    debug: bool = _Val(bool)
    branch: str = _Val(str)

CONTEXT = Context()
