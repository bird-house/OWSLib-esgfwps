# -*- coding: utf-8 -*-

"""
The `owslib-esgfwps` package is an extension for `OWSLib` to support the
ESGF WPS profile.

Example
-------
In this example we are using a local installation of the Pelican WPS service:
https://github.com/bird-house/pelican

Use the `owslib-esgfwps` extension to execute the `pelican_subset` WPS process::

    >>> from owslib.wps import WebProcessingService
    >>> from owslib_esgfwps import Domain, Dimension, Variable
    >>> wps = WebProcessingService(url='http://localhost:5000/wps')
    >>> d0 = Domain(dict(time=Dimension(0, 1, crs='indices')))
    >>> OPENDAP_URL = 'http://nowhere/tas.nc'
    >>> v0 = Variable(uri=OPENDAP_URL, var_name='tas')
    >>> from owslib_esgfwps import Domains, Variables
    >>> exec = wps.execute('pelican_subset', inputs=[('domain', Domains([d0])), ('variable', Variables([v0]))])
"""

import json
import yaml
from uuid import uuid4

from owslib.wps import ComplexDataInput


class ParameterError(Exception):
    pass


class Parameter(object):
    def __init__(self):
        pass

    @property
    def json(self):
        raise NotImplementedError

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    @property
    def params(self):
        return {}

    def __repr__(self):
        params = ''
        for key, value in self.params.items():
            params += "{}='{}',".format(key, value)
        return "{}({})".format(self.__class__.__name__, params.strip(","))


class WPSParameter(ComplexDataInput, Parameter):
    def __init__(self):
        super(WPSParameter, self).__init__(
            value=None,
            mimeType="application/json",
            encoding=None,
            schema=None)

    @property
    def value(self):
        return json.dumps(self.json)

    @value.setter
    def value(self, value):
        if value:
            self.from_json(yaml.safe_load(value))


class Output(Parameter):
    def __init__(self, id=None, uri=None, domain=None, mimetype=None):
        super(Output, self).__init__()
        self._id = id or uuid4().hex
        self._uri = uri
        self._domain = domain
        self._mimetype = mimetype

        if not self._uri:
            raise ParameterError('Variable must have a uri.')

    @property
    def id(self):
        return self._id

    @property
    def uri(self):
        return self._uri

    @property
    def domain(self):
        return self._domain

    @property
    def mimetype(self):
        return self._mimetype

    @property
    def json(self):
        data = dict(uri=self.uri)
        if self.id:
            data['id'] = self.id
        if self.domain:
            data['domain'] = self.domain
        if self.mimetype:
            data['mime-type'] = self.mimetype
        return data

    @classmethod
    def from_json(cls, data):
        # TODO: use mimetype as key
        new_data = data.copy()
        if 'mime-type' in data:
            new_data['mimetype'] = data['mime-type']
            del new_data['mime-type']
        return cls(**new_data)

    @property
    def params(self):
        return self.json


class Outputs(Parameter):
    def __init__(self, outputs=None):
        super(Outputs, self).__init__()
        self._outputs = outputs or []

    @property
    def outputs(self):
        return self._outputs

    @property
    def json(self):
        return [output.json for output in self.outputs]

    @classmethod
    def from_json(cls, data):
        outputs = [Output.from_json(output) for output in data]
        return cls(outputs=outputs)

    @classmethod
    def from_owslib(cls, process_outputs):
        for output in process_outputs:
            if output.identifier == 'output':
                return cls.from_json(data=yaml.safe_load(output.data[0]))
        return cls(outputs=[])

    @property
    def params(self):
        return dict(outputs=[output.id for output in self.outputs])


class Variable(Parameter):
    def __init__(self, uri, var_name=None, id=None, domain=None):
        super(Variable, self).__init__()
        self._name = uuid4().hex
        self._uri = uri
        self._id = None
        self._domain = domain

        if id:
            self._id = id
            if '|' in id:
                var_name, self._name = id.split('|')
            else:
                raise ParameterError('Variable id must contain a variable name and id.')
        if var_name:
            self._var_name = var_name
            if not id:
                self._id = '{}|{}'.format(var_name, self._name)

        if not self._id:
            raise ParameterError('Variable must have an id.')

    @property
    def name(self):
        return self._name

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
    def domain(self):
        return self._domain

    @property
    def json(self):
        data = dict(uri=self.uri, id=self.id)
        if self.domain:
            data['domain'] = self.domain
        return data

    @property
    def params(self):
        return dict(id=self.id)


class Variables(WPSParameter):
    def __init__(self, variables=None):
        super(Variables, self).__init__()
        self._variables = variables or []

    @property
    def variables(self):
        return self._variables

    @property
    def json(self):
        return [var.json for var in self.variables]

    @classmethod
    def from_json(cls, data):
        variables = [Variable.from_json(var) for var in data]
        return cls(variables=variables)

    @property
    def params(self):
        return dict(variables=[var.id for var in self.variables])


class Dimension(Parameter):
    def __init__(self, start=None, end=None, step=1, crs=None):
        super(Dimension, self).__init__()
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
        return dict(start=self.start, end=self.end, step=self.step, crs=self.crs)

    @property
    def params(self):
        return self.json


class Domain(Parameter):
    def __init__(self, dimensions=None, mask=None, id=None):
        super(Domain, self).__init__()
        self._id = id or uuid4().hex
        self._dimensions = dimensions or {}
        self._mask = mask

    @property
    def id(self):
        return self._id

    @property
    def dimensions(self):
        return self._dimensions

    @property
    def mask(self):
        return self._mask

    @property
    def json(self):
        data = dict(id=self.id)
        if self.mask:
            data['mask'] = self.mask
        for dim_id, dim in self.dimensions.items():
            data[dim_id] = dim.json
        return data

    @classmethod
    def from_json(cls, data):
        new_data = {}
        new_data['id'] = data['id']
        new_data['mask'] = data.get('mask')
        new_data['dimensions'] = {}
        for key in list(data.keys()):
            if key not in ['id', 'mask']:
                new_data['dimensions'][key] = Dimension.from_json(data[key])
        return cls(**new_data)

    @property
    def params(self):
        return dict(id=self.id)


class Domains(WPSParameter):
    def __init__(self, domains=None):
        super(Domains, self).__init__()
        self._domains = domains or []

    @property
    def domains(self):
        return self._domains

    @property
    def json(self):
        return [domain.json for domain in self.domains]

    @classmethod
    def from_json(cls, data):
        domains = [Domain.from_json(domain) for domain in data]
        return cls(domains=domains)

    @property
    def params(self):
        return dict(domains=[domain.id for domain in self.domains])


class Operation(Parameter):
    def __init__(self, name=None, domain=None, input=None, result=None, axes=None, bins=None):
        super(Operation, self).__init__()
        self._name = name or uuid4().hex
        self._domain = domain
        self._input = input
        self._result = result or uuid4().hex
        self._axes = axes
        self._bins = bins

    @property
    def name(self):
        return self._name

    @property
    def domain(self):
        if hasattr(self._domain, 'id'):
            return self._domain.id
        return self._domain

    @property
    def input(self):
        names = []
        for inpt in self._input:
            if hasattr(inpt, 'name'):
                names.append(inpt.name)
            else:
                names.append(inpt)
        return names

    @property
    def result(self):
        return self._result

    @property
    def axes(self):
        return self._axes

    @property
    def bins(self):
        return self._bins

    @property
    def json(self):
        data = dict(
            name=self.name,
            domain=self.domain,
            input=self.input,
            result=self.result)
        return data

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    @property
    def params(self):
        return dict(name=self.name)


class Operations(WPSParameter):
    def __init__(self, operations=None):
        super(Operations, self).__init__()
        self._operations = operations or []

    @property
    def operations(self):
        return self._operations

    @property
    def json(self):
        return [op.json for op in self.operations]

    @classmethod
    def from_json(cls, data):
        operations = [Operation.from_json(op) for op in data]
        return cls(operations=operations)

    @property
    def params(self):
        return dict(operations=[op.name for op in self.operations])
