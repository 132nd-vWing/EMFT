# coding=utf-8
import sys

import click


def exit_(code, err: bool = False):
    """
    Pause the application before exiting to give the user time to read the log
    :param code: exit code
    :param err: indicates an error
    """
    click.pause(err=err)
    sys.exit(code)
