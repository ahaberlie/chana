import os
from numpy.testing import assert_equal, assert_almost_equal
import datetime
import pandas as pd
import numpy as np
import xarray as xr

from chana.preproc.convert import (get_chey_date, get_index,
                                   convert_file)
                                     
# by default, this is in data/test/
test_data_dir = os.environ.get('TEST_DATA_DIR')   


def test_get_chey_date():

    filename = "AFWA_d01_2004-12-01_00_00_00"

    expected = datetime.datetime(2004, 12, 1, 0, 0, 0)

    returned = get_chey_date(filename)

    assert_equal(expected, returned)

    filename = "AFWA_d01_1992-12-01_00_00_00"

    expected = datetime.datetime(1992, 12, 1, 0, 0, 0)

    returned = get_chey_date(filename)

    assert_equal(expected, returned)

    filename = "AFWA_d01_2090-12-01_00_00_00"

    expected = datetime.datetime(2090, 12, 1, 0, 0, 0)

    returned = get_chey_date(filename)

    assert_equal(expected, returned)


def test_get_index():

    start_year = 2004

    file_dir = test_data_dir + "2004-2005/"

    returned = get_index(start_year, file_dir)

    returned = returned[~pd.isnull(returned.filename)]

    expected_files = ['AFWA_d01_2004-12-01_00_00_00',
                      'AFWA_d01_2004-12-05_00_15_00',
                      'AFWA_d01_2004-12-15_00_15_00']

    returned_files = [x[-28:] for x in returned.filename.values]

    assert_equal(expected_files, returned_files)

    expected_dates = ['2004-12-01 00:00:00', '2004-12-05 00:15:00', '2004-12-15 00:15:00']

    returned_dates = returned.time.values

    assert_equal(expected_dates, returned_dates)

    start_year = 1992

    file_dir = test_data_dir + "1992-1993/"

    returned = get_index(start_year, file_dir)

    returned = returned[~pd.isnull(returned.filename)]

    expected_files = ['AFWA_d01_1992-12-01_00_00_00',
                      'AFWA_d01_1992-12-05_00_15_00',
                      'AFWA_d01_1992-12-15_00_15_00']

    returned_files = [x[-28:] for x in returned.filename.values]

    assert_equal(expected_files, returned_files)

    expected_dates = ['1992-12-01 00:00:00', '1992-12-05 00:15:00', '1992-12-15 00:15:00']

    returned_dates = returned.time.values

    assert_equal(expected_dates, returned_dates)

    start_year = 2090

    file_dir = test_data_dir + "2090-2091/"

    returned = get_index(start_year, file_dir)

    returned = returned[~pd.isnull(returned.filename)]

    expected_files = ['AFWA_d01_2090-12-01_00_00_00',
                      'AFWA_d01_2090-12-05_00_15_00',
                      'AFWA_d01_2090-12-15_00_15_00']

    returned_files = [x[-28:] for x in returned.filename.values]

    assert_equal(expected_files, returned_files)

    expected_dates = ['2090-12-01 00:00:00', '2090-12-05 00:15:00', '2090-12-15 00:15:00']

    returned_dates = returned.time.values

    assert_equal(expected_dates, returned_dates)


def test_convert_file():

    file_dir = test_data_dir + "convert/"

    expected_variables = ['dummy1', 'dummy5']
    expected_attr1 = "Main attribute"
    expected_attr2 = "Sub attribute for dummy1"
    expected_attr6 = "Sub attribute for dummy5"

    expected_dummy1 = np.zeros((1, 3, 3))
    expected_dummy5 = 4*np.ones((1, 3, 3))

    expected_time = '2005-02-28T23:45:00.000000000'

    out_nc = convert_file(file_dir + "test_convert.nc", expected_variables)

    time = str(out_nc.Time.values[0])

    assert_equal(expected_time, time)

    data_vars = [x for x in out_nc.data_vars]

    assert_equal(expected_variables, data_vars)

    dummy1 = out_nc['dummy1'].values
    dummy5 = out_nc['dummy5'].values

    assert_almost_equal(expected_dummy1, dummy1)
    assert_almost_equal(expected_dummy5, dummy5)

    attr1 = out_nc.attrs['attr1']

    assert_equal(expected_attr1, attr1)

    attr2 = out_nc['dummy1'].attrs['attr2']
    attr6 = out_nc['dummy5'].attrs['attr6']

    assert_equal(expected_attr2, attr2)
    assert_equal(expected_attr6, attr6)
