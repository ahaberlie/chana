import glob
import datetime
from natsort import natsorted
import pandas as pd
import xarray as xr
import numpy as np


def get_chey_date(fname):
    r"""Converts Cheyenne filename to a datetime.
    
    Parameters
    ----------
    fname: str
        Cheyenne filename
        
    Returns
    -------
    datetime: datetime
        Datetime representation of given filename.
    """    

    return datetime.datetime.strptime(fname[-19:], '%Y-%m-%d_%H_%M_%S')


def get_index(start_year, parent_dir, file_prefix='AFWA'):
    r"""Associates a Cheyenne filename with a 15 minute
    period during a given simulation year, which starts in October
    and ends in September.
    
    Parameters
    ----------
    start_year: int
        The year at the start of the simulation.
        
    parent_dir: str
        The top directory in which to look for files.
        This is expected to have the simulation year 
        within it (e.g., 2004-2005/).
    file_prefix: str
        Leading filename prefix, can either be AFWA or pgrb3D. Default 'AFWA'.
        
    Returns
    -------
    df: pandas DataFrame
        DataFrame of datetime / filename pairs.
    """  
    
    dfs = []
    
    drng = pd.date_range(start='{}-10-01 00:00:00'.format(start_year), 
                         end='{}-09-30 23:45:00'.format(start_year+1), freq='15T')
    
    index = {k.strftime("%Y-%m-%d %H:%M:%S"): None for k in drng}
    
    for month in range(1, 13):
    
        files = natsorted(glob.glob("{}/{:02d}/{}*".format(parent_dir, month, file_prefix)))

        for file in files:
            
            dtime = get_chey_date(file).strftime("%Y-%m-%d %H:%M:%S")
            
            index[dtime] = file

    data_items = index.items()
    data_list = list(data_items)
    df = pd.DataFrame.from_dict(data_list)
    df.columns = ['time', 'filename']
    dfs.append(df)
    df = pd.concat(dfs)
        
    return df


def convert_file(filename, fields):
    r"""For a given netCDF file at 'filename', preprocess the file
    by converting times to datetime, making it a coordinate, and
    then only saving those variables given in 'var' in the newly
    output netCDF file.

    Parameters
    ----------
    filename: str
        Location of the netCDF file.

    fields: list
        List of vars to include in the converted file.

    Returns
    -------
    dset: xarray Dataset
        Converted information in an xarray representation.
    """

    ds = xr.open_dataset(filename)

    dtime = datetime.datetime.strptime(ds.Times.values[0].decode('utf8'), '%Y-%m-%d_%H:%M:%S')

    coord_dict = {'Time': (('Time'), np.array([dtime]))}

    var_dict = {}

    for field in fields:

        var_dict[field] = (('Time', 'south_north', 'west_east'), ds[field])

    dset = xr.Dataset(var_dict, coords=coord_dict)
    dset.attrs = ds.attrs

    for field in fields:

        for attr in ds[field].attrs.keys():
            dset[field].attrs[attr] = ds[field].attrs[attr]

    return dset
