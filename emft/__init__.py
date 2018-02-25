# coding=utf-8
"""
EMFT package
"""
from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution('emft').version
except DistributionNotFound:  # pragma: no cover
    __version__ = 'not installed'
