"""Tests for `owslib-esgfwps` package.

See compatibility examples:
https://github.com/ESGF/esgf-compute-api/blob/devel/docs/source/cwt.compat.rst
"""

from owslib_esgfwps import (
    Output,
    Outputs,
    Domain,
    Domains,
    Dimension,
    Variable,
    Variables,
    Operation,
    Operations
)


def test_output_compat():
    data = {
        "uri": "http://test.org/output.nc",
        "id": "tas_avg_mon",
        "domain": {"id": "d0"},
        "mime-type": "x-application/netcdf",
    }
    # from json
    output = Output.from_json(data)
    assert output.uri == data['uri']
    # json
    assert output.json['uri'] == data['uri']


def test_outputs():
    output = Output(id="tas_avg_mon", uri="http://test.org/output.nc")
    outputs = Outputs([output])
    assert Outputs.from_json(outputs.json).outputs[0].uri == output.uri
    assert output.id in str(outputs)


def test_dimension_compat():
    dim_data = {"start": 0.0, "end": 90.0, "step": 1, "crs": "indices"}
    # from json
    dim = Dimension.from_json(dim_data)
    assert dim.start == 0.0
    assert dim.end == 90.0
    assert dim.step == 1
    assert dim.crs == 'indices'
    # json
    assert dim.json['start'] == 0.0
    assert dim.json['end'] == 90.0
    assert dim.json['step'] == 1
    assert dim.json['crs'] == 'indices'


def test_dimension():
    dim = Dimension(0, 1, crs='indices')
    assert dim.start == 0
    assert dim.end == 1
    assert dim.crs == 'indices'
    assert Dimension.from_json(dim.json).start == 0
    assert str(dim) == "Dimension(start='0',end='1',step='1',crs='indices')"


def test_domain_compat():
    d0_data = {
        "id": "d0",
        "latitude": {"start": 0.0, "end": 45.0, "step": 1.5, "crs": "values", },
        "longitude": {"start": 10, "end": 20, "crs": "indices", },
        "time": {"start": 1981, "end": 2016, "crs": "values", }, }
    # from json
    d0 = Domain.from_json(d0_data)
    assert d0.id == 'd0'
    assert len(d0.dimensions) == 3
    # json
    assert d0.json['id'] == 'd0'
    assert 'time' in d0.json
    assert 'latitude' in d0.json
    assert 'longitude' in d0.json


def test_domain():
    d0 = Domain(dict(
        time=Dimension(0, 1, crs='indices'),
        lat=Dimension(40, 60, crs='values'),
        lon=Dimension(0, 20, crs='values'),))
    assert len(d0.dimensions) == 3
    assert d0.dimensions['time'].start == 0
    assert d0.dimensions['time'].end == 1
    assert d0.dimensions['time'].crs == 'indices'
    assert 'id' in d0.json
    assert 'time' in d0.json
    assert 'lat' in d0.json
    assert 'lon' in d0.json
    assert len(Domain.from_json(d0.json).dimensions) == 3
    assert d0.id in str(d0)


def test_domains():
    d0 = Domain(dict(time=Dimension(0, 1, crs='indices')))
    domains = Domains([d0])
    assert Domains.from_json(domains.json).domains[0].id == d0.id
    assert d0.id in str(domains)


def test_variable_compat():
    tas_data = {"id": "tas|v0", "uri": "http://somewhere/test.nc", "domain": "d0"}
    # from json
    tas = Variable.from_json(tas_data)
    assert tas.id == 'tas|v0'
    assert tas.var_name == 'tas'
    assert tas.uri == 'http://somewhere/test.nc'
    assert tas.domain == 'd0'
    # json
    assert tas.json['id'] == 'tas|v0'
    assert tas.json['uri'] == 'http://somewhere/test.nc'
    assert tas.json['domain'] == 'd0'


def test_variable():
    tas = Variable(uri='http://data.test.org/tas.nc', var_name='tas')
    assert tas.var_name == 'tas'
    assert tas.uri == 'http://data.test.org/tas.nc'
    assert 'uri' in tas.json
    assert 'id' in tas.json
    assert Variable.from_json(tas.json).var_name == 'tas'
    assert tas.id in str(tas)


def test_variables():
    tas = Variable(uri='http://data.test.org/tas.nc', var_name='tas')
    vars = Variables([tas])
    assert Variables.from_json(vars.json).variables[0].var_name == 'tas'
    assert 'tas' in str(vars)


def test_operation_compat():
    op_data = {
        "name": "CDS.timeBin",
        "input": ["v0"],
        "result": "cycle",
        "domain": "d0",
        "axes": "time",
        "bins": "t|month|ave|year", }
    # from json
    op = Operation.from_json(op_data)
    assert op.name == op_data['name']
    assert op.input == op_data['input']
    assert op.result == op_data['result']
    assert op.domain == op_data['domain']
    assert op.axes == op_data['axes']
    assert op.bins == op_data['bins']
    # json
    assert op.json['name'] == op_data['name']


def test_operation():
    d0 = Domain(dict(time=Dimension(0, 1, crs='indices')))
    tas = Variable(uri='http://data.test.org/tas.nc', var_name='tas')
    operation = Operation('subset', domain=d0, input=[tas])
    assert operation.name == 'subset'
    assert operation.domain == d0.id
    assert operation.input[0] == tas.name
    assert 'domain' in operation.json
    assert Operation.from_json(operation.json).name == 'subset'
    assert str(operation) == "Operation(name='subset')"


def test_operations():
    operation = Operation('subset', domain='d0', input=['tas'])
    operations = Operations([operation])
    assert Operations.from_json(operations.json).operations[0].name == operation.name
    assert operation.name in str(operations)
