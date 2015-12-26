from mock import patch
from mock import Mock
from greengraph import Map
from random import random
import requests
from matplotlib import image as img
from StringIO import StringIO
import numpy as np

def colour_box((left,bottom,right,top),**kwargs):
    colour = 1
    intensity = 1

    if 'pixels' in kwargs.keys():
        pixels = kwargs['pixels']
        size = (pixels.shape[0],pixels.shape[1])
    elif 'size' in kwargs.keys():
        size = kwargs['size']
        pixels = np.zeros([size[0],size[1],3])
    else:
        size = (400,400)
        pixels = np.zeros([size[0],size[1],3])
    if 'colour' in kwargs.keys():
        colour = kwargs['colour']
    if 'intensity' in kwargs.keys():
        intensity = kwargs['intensity']

    if not  (0 <= left <= right < size[0] and \
            0 <= bottom <= top < size[1]):
                raise ValueError(
                    "Require 0 <= left <= right < " + str(size[0]) + " and 0 <="
                    "bottom <= top < " + str(size[1]) + ".")

    pixels[left:right,bottom:top,colour] = intensity
    return pixels

def box_count(left,bottom,right,top):
    return abs(right-left)*abs(top-bottom)

def multi_speckle(size=(400,400)):
    green_array = np.zeros([size[0],size[1],3])
    multi_array = np.zeros([size[0],size[1],3])
    for (x,y), value in np.ndenumerate(green_array[:,:,1]):
        ran = random()
        if ran < 0.333:
            green_array[x,y,0], multi_array[x,y,0] = 0, 1
        elif ran < 0.666:
            green_array[x,y,1], multi_array[x,y,1] = 1, 1
        else:
            green_array[x,y,2], multi_array[x,y,2] = 0, 1
    return multi_array, green_array

def single_colour_speckle(**kwargs):
    colour = 1
    if 'pixels' in kwargs.keys():
        pixels = kwargs['pixels']
    elif 'size' in kwargs.keys():
        size = kwargs['size']
        pixels = np.zeros([size[0],size[1],3])
    else:
        pixels = np.zeros([400,400,3])
    if 'colour' in kwargs.keys():
        colour = kwargs['colour']
    count = 0
    for (x,y), value in np.ndenumerate(pixels[:,:,0]):
        if random() > 0.5:
            pixels[x,y,colour] = 1
            count += 1
    return pixels, count

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
    return None

def count_green_box_test(left,bottom,right,top,size=(400,400)):
    [lat, long] = [0.0, 0.0]
    image_array = colour_box((left,bottom,right,top),size=size)
    patch_imread = Mock(return_value=image_array)
    patch_get = Mock()
    patch_get.content = ''
    with patch.object(requests,'get',patch_get) as mock_get:
        with patch.object(img,'imread',patch_imread) as mock_imread:
            my_map = Map(lat, long)
    assert my_map.count_green() == box_count(left,bottom,right,top)
    return None

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
    return None

def count_green_random_test(size=(400,400)):
    image_array, count = single_colour_speckle()
    patch_imread = Mock(return_value=image_array)
    with patch.object(requests,'get') as mock_get:
        with patch.object(img,'imread',patch_imread) as mock_imread:
            my_map = Map(0,0)
    assert my_map.count_green() == count
    return None

def show_green_test(size=(400,400)):
    multi_array, green_array = multi_speckle(size)
    patch_imread = Mock(return_value=multi_array)
    with patch.object(requests,'get') as mock_get:
        with patch.object(img,'imread',patch_imread) as mock_imread:
            my_map = Map(0,0)
    multi_array_green = img.imread(StringIO(my_map.show_green()))[:,:,0:3]
    assert np.all(green_array == multi_array_green)
    return None


default_params_test()
show_green_test()
count_green_box_test(10,10,60,60)
count_green_box_test(0,0,0,0)
count_green_box_test(0,0,1,1)
count_green_box_test(0,0,399,399)
for x in range(10):
    count_green_random_test()
green_test()
