from greengraph import Greengraph
from tools import colour_box, box_count
from mock import patch, Mock
from matplotlib import image as img
import requests
import geopy
import numpy as np
from tools import bearing
from nose.tools import assert_almost_equal

def location_sequence_bearing_test(start=[0,0],end=[0,179]):
    with patch.object(geopy.geocoders.GoogleV3,'geocode') as mock_geocode:
        my_graph = Greengraph('New York','Chicago')
    array1 = np.array([start])
    array2 = np.array([start, end])
    sequence = my_graph.location_sequence(start,end,20)
    bearing_sequence = [bearing(sequence[0],point) for point in sequence[1:]]
    for x in bearing_sequence:
	assert_almost_equal(x, bearing_sequence[0], delta = 1e-6)
