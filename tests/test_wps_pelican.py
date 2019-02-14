"""Tests with WPS `Emu` service."""

import pytest

from owslib.wps import WebProcessingService, SYNC
from owslib_esgfwps import Domain, Dimension, Variable

from .common import TEST_SU_OPENDAP


@pytest.mark.online
def test_wps_emu_subset():
    headers = {'api_key': 'TOKEN'}
    wps = WebProcessingService(
        url='http://localhost:5000/wps',
        headers=headers, verify=True)
    d0 = Domain([Dimension('time', 0, 1, crs='indices')])
    v0 = Variable(uri=TEST_SU_OPENDAP, var_name='su')
    exec = wps.execute(
        'emu_subset',
        inputs=[('domain', d0), ('variable', v0)],
        mode=SYNC)
    assert exec.isSucceded()
