import numpy as np
import os
from numpy.testing import assert_equal, assert_almost_equal

from chana.analysis.climo import (get_sum, get_count)
                                     
test_data_dir = os.environ.get('TEST_DATA_DIR')    


def test_get_sum():

    #the key here is to create a npy file that represents a
    #sum result for any case we want to possibly try. This
    #is accomplished by creating an analysis that you are
    #highly confident is correct for the cases
    #the purpose of this is to make sure that future changes
    #do not break the analysis
    #The point is to get through the asserts without any issues
    
    true_sum = #whatever you find in the manual analysis
    
    sum = #call to get_sum
    
    #assert_almost_equal should be used whenver you think there
    #may be floating points.  I also use it when comparing grids.
    assert_almost_equal(sum, true_sum)

def test_get_count():

    #this one might be easier because it is just an integer
    
    true_count = #whatever you find in the manual analysis
    
    count = #call to get_count
    
    #assert_equal works only with integers
    assert_equal(true_count, count)
    
