#imports
import numpy as np
import pandas as pd
from datetime import datetime

def get_sum(geo_df, groupby=None):
    r"""Calculates the sum of given slices.  The argument
    groupby identifies the column on which to sum over.  If
    none, all slices are summed up. In other words, a single
    MCS can be counted multiple times every hour. If not none, 
    the given pandas GeoDataFrame is grouped by the given column.
    In other words, if grouped by 'storm_num' or similar, the 
    MCS is counted only once.  This could also be used to groupby
    unique dates to calculate MCS days.
    
    Parameters
    ----------
    geo_df: pandas GeoDataFrame
        Base directory in which to save the csv file.
    groupby: str
        If none, simple sum of all slices.  If not none,
        the maximum value added to the sum for a given group 
        is 1.
        
    Returns
    -------
    result: ndarray (N, M)
        The resulting daily sum for a given geo_df
    """

    df = pd.read_csv(geo_df)
    sum_type = groupby
    result = []

    if sum_type == None:
        #loop through each group by day and sum slices
        slice_sum = 0
        for row in df.iterrows():
            slice_sum += 1

        result = np.array([slice_sum])

    else:
        #groupby
        #loop through each group and sum slices
        #multiply by 1 and add to overall sum
        for gid, group in df.groupby(sum_type):
            slice_sum = 0
            tmp = 0
            for sid, sli in group.iterrows():
                tmp += 1
            slice_sum += 1*tmp
            column = sli[sum_type]

            result.append([column, slice_sum])
            
        result = np.array(result)
    
    return result
        
def get_count(geo_df, groupby=None):
    r"""Calculates the count of given MCS slices.  The argument
    groupby identifies the column on which to count over.  If
    none, all slices are counted up. In other words, a single
    MCS can contribute dozens of slices to the count. If not none, 
    the given pandas GeoDataFrame is grouped by the given column.
    In this way, only one MCS is counted.  This could also be useful
    for counting MCS days if grouped by unique dates.
    
    Parameters
    ----------
    geo_df: pandas GeoDataFrame
        Base directory in which to save the csv file.
    groupby: str
        If none, simple sum of all slices.  If not none,
        the maximum value added to the sum for a given group 
        is 1.
        
    Returns
    -------
    result: ndarray (N, M)
        The resulting daily sum for a given geo_df
    """

    sum_type = groupby
    if sum_type == None:
        #loop through each group and count slices
    
    else:
        #groupby
        #loop through each group and add to counts

    return result
    
    
#more functions here

