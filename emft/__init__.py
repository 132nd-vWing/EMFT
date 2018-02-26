# coding=utf-8
"""
EMFT package
"""
import sys
import elib
from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution('emft').version
except DistributionNotFound:  # pragma: no cover
    if getattr(sys, 'frozen', False):
        __version__ = elib.exe_version.get_product_version(sys.executable)
    else:
        # package is not installed
        __version__ = 'not installed'
