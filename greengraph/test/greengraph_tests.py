from greengraph import Greengraph
from test_tools import colour_box, box_count
from mock import patch, Mock
from matplotlib import image as img
import requests
import geopy

def geolocate_test():
    return_location = [[0,(1,2)]]
    patch_geocode = Mock(return_value = return_location)
    with patch.object(requests,'get') as mock_get:
        with patch.object(geopy.geocoders.GoogleV3,'geocode',patch_geocode) \
            as mock_geocode:
            my_graph = Greengraph('New York','Chicago')
            location = my_graph.geolocate('London')
    mock_geocode.assert_called_with('London',exactly_one=False)
    assert location == (1,2)
    return None

def green_between_test(steps=400):
    pixel_arrays = [colour_box((0,0,x,x)) for x in range(steps)]

    patch_imread = Mock()
    patch_imread.side_effect = pixel_arrays

    with patch.object(requests,'get') as mock_get:
        with patch.object(img,'imread',patch_imread) as mock_imread:
            mygraph=Greengraph('New York','Chicago')
            data = mygraph.green_between(steps)

    assert [box_count(0,0,x,x) for x in range(steps)] == data
    return None

def location_sequence_test():
    my_graph = Greengraph('New York','Chicago')
    start = [0,0]
    end = [1,1]
    array1 = np.array([start])
    array2 = np.array([start, end])
    assert not mygraph.location_sequence(start,end,0)
    assert np.all(my_graph.location_sequence(start,end,1)==array1)
    assert np.all(my_graph.location_sequence(start,end,2)==array2)
    return None

geolocate_test()
green_between_test()
location_sequence_test()
