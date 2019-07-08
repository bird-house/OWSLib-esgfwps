"""Tests with WPS `Pelican` service:
https://github.com/bird-house/pelican
"""

import pytest

from owslib.wps import WebProcessingService, SYNC
from owslib_esgfwps import Domain, Domains, Dimension, Variable, Variables

from .common import TEST_SU_OPENDAP


@pytest.mark.online
def test_wps_pelican_subset():
    headers = {'COMPUTE-TOKEN': 'TOKEN'}
    wps = WebProcessingService(
        url='http://localhost:5000/wps',
        headers=headers, verify=True)
    d0 = Domain(dict(time=Dimension(0, 1, crs='indices')))
    v0 = Variable(uri=TEST_SU_OPENDAP, var_name='su')
    exec = wps.execute(
        'pelican_subset',
        inputs=[('domain', Domains([d0])), ('variable', Variables([v0]))],
        mode=SYNC)
    assert exec.isSucceded()
