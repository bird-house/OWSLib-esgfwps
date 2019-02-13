# -*- coding: utf-8 -*-

"""
The `owslib-esgfwps` package is an extension for `OWSLib` to support the
ESGF WPS profile.

Example
-------
Use the `owslib-esgfwps` extension to execute the `emu_subset` WPS process::

    >>> from owslib.wps import WebProcessingService
    >>> from owslib_esgfwps import Domain, Dimension, Variable
    >>> wps = WebProcessingService(url='http://localhost:5000/wps')
    >>> d0 = Domain([Dimension('time', 0, 1, crs='indices')])
    >>> OPENDAP_URL = 'http://'
    >>> v0 = Variable(uri=OPENDAP_URL, var_name='su')
    >>> exec = wps.execute('emu_subset', inputs=[('domain', d0), ('variable', v0)])
"""

__author__ = """Carsten Ehbrecht"""
__email__ = 'ehbrecht@dkrz.de'
__version__ = '0.1.0'

from .extension import (
    ParameterError,
    Parameter,
    Domain,
    Dimension,
    Variable,
)
