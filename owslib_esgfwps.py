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

import json
from uuid import uuid1

from owslib.wps import ComplexDataInput


class ParameterError(Exception):
    pass


class Parameter(ComplexDataInput):
    def __init__(self, name=None):
        super(Parameter, self).__init__(
            value=None,
            mimeType="application/json",
            encoding=None,
            schema=None)
        self._data = {}
        self._data['name'] = name or uuid1().hex

    @property
    def name(self):
        return self._data['name']

    @property
    def json(self):
        return self._data

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    @property
    def value(self):
        return json.dumps(self.json)

    @value.setter
    def value(self, value):
        if value:
            self.from_json(json.loads(value))

    def __repr__(self):
        params = ''
        for key in self._data:
            params += "{}='{}', ".format(key, self._data[key])
        return "{}({})".format(self.__class__.__name__, params.strip(', '))


class Variable(Parameter):
    def __init__(self, uri, var_name=None, id=None, name=None):
        super(Variable, self).__init__(name)
        self._data['uri'] = uri

        if id:
            self._data['id'] = id
            if '|' in id:
                var_name, name = id.split('|')
            else:
                raise ParameterError('Variable id must contain a variable name and id.')
        if var_name:
            self._data['var_name'] = var_name
            if not id:
                self._data['id'] = '{}|{}'.format(var_name, self.name)

        if 'id' not in self._data:
            raise ParameterError('Variable must have an id.')
        if 'var_name' not in self._data:
            raise ParameterError('Variable must have a var_name.')

    @property
    def id(self):
        return self._data['id']

    @property
    def var_name(self):
        return self._data['var_name']

    @property
    def uri(self):
        return self._data['uri']


class Dimension(Parameter):
    def __init__(self, name=None, start=None, end=None, step=1, crs="values"):
        super(Dimension, self).__init__(name)
        self._data['start'] = start
        self._data['end'] = end
        self._data['step'] = step
        self._data['crs'] = crs

    @property
    def start(self):
        return self._data['start']

    @property
    def end(self):
        return self._data['end']

    @property
    def step(self):
        return self._data['step']

    @property
    def crs(self):
        return self._data['crs']

    @crs.setter
    def crs(self, value):
        if value in ["values", "indices"]:
            self._data['crs'] = value
        else:
            raise ValueError


class Domain(Parameter):
    def __init__(self, dimensions=None, mask=None, name=None):
        super(Domain, self).__init__(name)
        if dimensions:
            self._data['dimensions'] = [dim.json if isinstance(dim, Dimension) else dim for dim in dimensions]
        else:
            self._data['dimensions'] = []
        self._data['mask'] = mask

    @property
    def dimensions(self):
        return self._data['dimensions']

    @property
    def mask(self):
        return self._data['mask']
