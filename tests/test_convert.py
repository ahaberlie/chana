import os
from numpy.testing import assert_equal, assert_almost_equal
import datetime
import pandas as pd

from chana.preproc.convert import (get_chey_date, get_index)
                                     
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
