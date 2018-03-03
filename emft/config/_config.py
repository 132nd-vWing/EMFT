# coding=utf-8
"""
EMFT config
"""
from everett import ConfigurationError, ConfigurationMissingError, DetailedConfigurationError, InvalidKeyError, \
    InvalidValueError
from pathlib import Path
import inspect
import click

import elib
from emft.exit_ import exit_


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
    source_folder: bool = _Val(Path)
    appveyor: str = _Val(str)

    def _validate(self):
        try:
            for name, value in inspect.getmembers(self, inspect.isdatadescriptor):
                print(name)
        except ConfigurationMissingError as exc:
            click.secho(f'Missing configuration value: "{exc.key}"', err=True, color='red')
            click.echo('See README for more information.')
            exit_(1)
        except InvalidValueError as exc:
            click.secho(f'Invalid configuration value for: "{exc.key}"', err=True, color='red')
            click.echo('See README for more information.')
            exit_(1)


    def __init__(self):
        elib.config.BaseConfig.__init__(self, 'EMFT')
        self._validate()
        # except ConfigurationMissingError as exc:
        #     print(exc.key, 'missing')
        #     raise


