"""Tests for `owslib-esgfwps` package."""

from owslib_esgfwps import Domain, Dimension, Variable, Operation


def test_dimension():
    dim = Dimension('time', 0, 1, crs='indices')
    assert dim.name == 'time'
    assert dim.start == 0
    assert dim.end == 1
    assert dim.crs == 'indices'
    assert Dimension.from_json(dim.json).name == 'time'


def test_domain():
    d0 = Domain([
        Dimension('time', 0, 1, crs='indices'),
        Dimension('lat', 40, 60, crs='values'),
        Dimension('lon', 0, 20, crs='values'),
    ])
    assert len(d0.dimensions) == 3
    assert d0.dimensions[0].start == 0
    assert d0.dimensions[0].end == 1
    assert d0.dimensions[0].crs == 'indices'
    assert 'id' in d0.json[0]
    assert 'time' in d0.json[0]
    assert 'lat' in d0.json[0]
    assert 'lon' in d0.json[0]
    assert len(Domain.from_json(d0.json[0]).dimensions) == 3


def test_variable():
    tas = Variable(uri='http://data.test.org/tas.nc', var_name='tas')
    assert tas.var_name == 'tas'
    assert tas.uri == 'http://data.test.org/tas.nc'
    assert 'uri' in tas.json[0]
    assert 'id' in tas.json[0]
    assert Variable.from_json(tas.json[0]).var_name == 'tas'


def test_operation():
    d0 = Domain([Dimension('time', 0, 1, crs='indices')])
    tas = Variable(uri='http://data.test.org/tas.nc', var_name='tas')
    operation = Operation('subset', domain=d0, inputs=[tas])
    assert operation.name == 'subset'
    assert operation.domain == d0.name
    assert operation.inputs[0] == tas.name
    assert 'domain' in operation.json[0]
    assert Operation.from_json(operation.json[0]).name == 'subset'
