from mock import patch, Mock
from greengraph import Map
from random import random
import requests
from matplotlib import image as img
from StringIO import StringIO
import numpy as np
from tools import colour_box, multi_speckle, box_count, single_colour_speckle, box_count, map_count

def green_test():
    box1 = (0,0,50,50)
    box2 = (100,100,150,150)

    pixels = colour_box(box1,intensity=0.5)
    pixels = colour_box(box2,pixels=pixels,intensity=0.5)
    pixels = colour_box(box1,pixels=pixels,intensity=0.25,colour=0)
    pixels = colour_box(box2,pixels=pixels,intensity=0.75,colour=2)

    truth_array1 = colour_box(box1,intensity=True)
    truth_array2 = colour_box(box1,intensity=True)
    truth_array2 = colour_box(box2,pixels=truth_array2,intensity=True)
    truth_array3 = colour_box((0,0,0,0),intensity=True)

    patch_imread = Mock(return_value=pixels)
    with patch.object(requests,'get') as mock_get:
        with patch.object(img,'imread',patch_imread) as mock_imread:
            my_map = Map(0,0)

    assert np.all(truth_array2[:,:,1] == my_map.green(0))
    assert np.all(truth_array1[:,:,1] == my_map.green(1))
    assert np.all(truth_array3[:,:,1] == my_map.green(10))


def default_params_test():
    [lat, long] = [51.0, 0.0]
    [left,bottom,right,top]=[0,0,0,0]
    image_array = colour_box((left,bottom,right,top))
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


def count_green_random_test(size=(400,400),repeats=10):
    for i in range(10):
        image_array, count = single_colour_speckle()
        patch_imread = Mock(return_value=image_array)
        with patch.object(requests,'get') as mock_get:
            with patch.object(img,'imread',patch_imread) as mock_imread:
                my_map = Map(0,0)
                assert my_map.count_green() == count


def show_green_test(size=(400,400)):
    multi_array, green_array = multi_speckle(size)
    patch_imread = Mock(return_value=multi_array)
    with patch.object(requests,'get') as mock_get:
        with patch.object(img,'imread',patch_imread) as mock_imread:
            my_map = Map(0,0)
    multi_array_green = img.imread(StringIO(my_map.show_green()))[:,:,0:3]
    assert np.all(green_array == multi_array_green)


def count_green_box_test():
    assert map_count(10,10,60,60) == box_count(10,10,60,60)
    assert map_count(0,0,0,0) == box_count(0,0,0,0)
    assert map_count(0,0,1,1) == box_count(0,0,1,1)
    assert map_count(0,0,399,399) == box_count(0,0,399,399)
