# -*- coding: utf-8 -*-

"""
The `owslib-esgfwps` package is an extension for `OWSLib` to support the
ESGF WPS profile.

Example
-------
In this example we are using a local installatin of the Pelican WPS service:
https://github.com/bird-house/pelican

Use the `owslib-esgfwps` extension to execute the `pelican_subset` WPS process::

    >>> from owslib.wps import WebProcessingService
    >>> from owslib_esgfwps import Domain, Dimension, Variable
    >>> wps = WebProcessingService(url='http://localhost:5000/wps')
    >>> d0 = Domain([Dimension('time', 0, 1, crs='indices')])
    >>> OPENDAP_URL = 'http://'
    >>> v0 = Variable(uri=OPENDAP_URL, var_name='su')
    >>> exec = wps.execute('pelican_subset', inputs=[('domain', d0), ('variable', v0)])
"""

__author__ = """Carsten Ehbrecht"""
__email__ = 'ehbrecht@dkrz.de'
__version__ = '0.1.0'

import json
from uuid import uuid4

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
        self._name = name or uuid4().hex

    @property
    def name(self):
        return self._name

    @property
    def json(self):
        data = dict(name=self.name)
        return [data]

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
        params = "{}='{}'".format('name', self.name)
        return "{}({})".format(self.__class__.__name__, params)


class Variable(Parameter):
    def __init__(self, uri, var_name=None, id=None, name=None):
        super(Variable, self).__init__(name)
        self._uri = uri
        self._id = None

        if id:
            self._id = id
            if '|' in id:
                var_name, name = id.split('|')
            else:
                raise ParameterError('Variable id must contain a variable name and id.')
        if var_name:
            self._var_name = var_name
            if not id:
                self._id = '{}|{}'.format(var_name, self.name)

        if not self._id:
            raise ParameterError('Variable must have an id.')

    @property
    def id(self):
        return self._id

    @property
    def var_name(self):
        return self._var_name

    @property
    def uri(self):
        return self._uri

    @property
    def json(self):
        data = dict(uri=self.uri, id=self.id)
        return [data]


class Dimension(Parameter):
    def __init__(self, name=None, start=None, end=None, step=1, crs=None):
        super(Dimension, self).__init__(name)
        self._start = start
        self._end = end
        self._step = step
        self.crs = crs or "values"

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def step(self):
        return self._step

    @property
    def crs(self):
        return self._crs

    @crs.setter
    def crs(self, value):
        if value in ["values", "indices"]:
            self._crs = value
        else:
            raise ValueError

    @property
    def json(self):
        data = {}
        data[self.name] = dict(start=self.start, end=self.end, step=self.step, crs=self.crs)
        return data

    @classmethod
    def from_json(cls, data):
        name = list(data.keys())[0]
        new_data = dict(name=name)
        new_data.update(data[name])
        return cls(**new_data)


class Domain(Parameter):
    def __init__(self, dimensions=None, mask=None, name=None):
        super(Domain, self).__init__(name)
        self._dimensions = dimensions
        self._mask = mask

    @property
    def id(self):
        return self.name

    @property
    def dimensions(self):
        return self._dimensions

    @property
    def mask(self):
        return self._mask

    @property
    def json(self):
        data = dict(id=self.id)
        for dim in self.dimensions:
            data.update(dim.json)
        return [data]

    @classmethod
    def from_json(cls, data):
        dimensions = []
        for key in list(data.keys()):
            if key not in ['id', 'mask']:
                dimensions.append(Dimension.from_json({key: data[key]}))
                del data[key]
        data['dimensions'] = dimensions
        data['name'] = data['id']
        del data['id']
        return cls(**data)


class Operation(Parameter):
    def __init__(self, name=None, domain=None, inputs=None, result=None):
        super(Operation, self).__init__(name)
        self._domain = domain
        self._inputs = inputs
        self._result = result or uuid4().hex

    @property
    def domain(self):
        if hasattr(self._domain, 'name'):
            return self._domain.name
        return self._domain

    @property
    def inputs(self):
        names = []
        for inpt in self._inputs:
            if hasattr(inpt, 'name'):
                names.append(inpt.name)
            else:
                names.append(inpt)
        return names

    @property
    def result(self):
        return self._result

    @property
    def json(self):
        data = dict(
            name=self.name,
            domain=self.domain,
            input=self.inputs,
            result=self.result)
        return [data]

    @classmethod
    def from_json(cls, data):
        data['inputs'] = data['input']
        del data['input']
        return cls(**data)
