import glob
import datetime
from natsort import natsorted
import pandas as pd


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
    

def get_index(start_year, parent_dir):
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
    
        files = natsorted(glob.glob("{}/{:02d}/*AFWA*".format(parent_dir, month)))

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
