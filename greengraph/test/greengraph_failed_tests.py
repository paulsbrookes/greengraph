from greengraph import Greengraph
from test_tools import colour_box, box_count
from mock import patch, Mock
from matplotlib import image as img
import requests
import geopy
import numpy as np
from test_tools import bearing

def location_sequence_bearing_test(start,end):
    with patch.object(geopy.geocoders.GoogleV3,'geocode') as mock_geocode:
        my_graph = Greengraph('New York','Chicago')
    array1 = np.array([start])
    array2 = np.array([start, end])
    sequence = my_graph.location_sequence(start,end,20)
    bearing_sequence = [bearing(sequence[0],point) for point in sequence[1:]]
    assert np.all([x == bearing_sequence[0] for x in bearing_sequence])
    return None

location_sequence_bearing_test([0,170],[5,175])
