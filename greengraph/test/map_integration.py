from mock import patch
from mock import Mock
from greengraph import Map
import requests
from matplotlib import image as img
from StringIO import StringIO
import numpy as np

def green_box(left,bottom,right,top,size=(400,400)):
    image_array = np.zeros([size(0),size(1),3])
    image_array[:,:,:] = 1
    image_array[left:right,bottom:top,0] = 0
    image_array[left:right,bottom:top,2] = 0
    return image_array

def box_count(left,bottom,right,top):
    return abs(right-left)*abs(top-bottom)

def box_test(left,bottom,right,top):
    [lat, long] = [51.0, 0.0]
    image_array = green_box(left,bottom,right,top)
    patch_imread = Mock(return_value=image_array)
    patch_get = Mock()
    patch_get.content = ''
    with patch.object(requests,'get',patch_get) as mock_get:
        with patch.object(img,'imread',patch_imread) as mock_imread:
            my_map = Map(lat, long)
    assert my_map.count_green() == box_count(left,bottom,right,top)
    return None

box_test(10,10,60,60)
box_test(0,0,0,0)
box_test(1,1,0,0)
box_test(0,0,400,400)

def default_params_test():
    [lat, long] = [51.0, 0.0]
    [left,bottom,right,top]=[0,0,0,0]
    image_array = green_box(left,bottom,right,top)
    patch_imread = Mock(return_value=image_array)
    patch_get = Mock()
    patch_get.content = ''
    with patch.object(requests,'get',patch_get) as mock_get:
        with patch.object(img,'imread',patch_imread) as mock_imread:
            my_map = Map(lat, long)
    mock_get.assert_called_with(
        "http://maps.googleapis.com/maps/api/staticmap?",
        params={
            'sensor':'false',
            'zoom':10,
            'size':'400x400',
            'center':'51.0,0.0',
            'style':'feature:all|element:labels|visibility:off',
            'maptype':'satellite'
        }
    )
    return None

default_params_test()
