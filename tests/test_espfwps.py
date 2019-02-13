"""Tests for `owslib-esgfwps` package."""

from owslib_esgfwps import Domain, Dimension, Variable


def test_domain():
    d0 = Domain([
        Dimension('time', 0, 1, crs='indices'),
        Dimension('lat', 40, 60, crs='values'),
        Dimension('lon', 0, 20, crs='values'),
    ])
    assert len(d0.dimensions) == 3
    assert d0.dimensions[0]['start'] == 0
    assert d0.dimensions[0]['end'] == 1
    assert d0.dimensions[0]['crs'] == 'indices'
    assert 'dimensions' in d0.json
    assert len(Domain.from_json(d0.json).dimensions) == 3


def test_variable():
    v0 = Variable(uri='http://data.test.org/tas.nc', var_name='tas')
    assert v0.var_name == 'tas'
    assert v0.uri == 'http://data.test.org/tas.nc'
    assert 'uri' in v0.json
    assert Variable.from_json(v0.json).var_name == 'tas'
