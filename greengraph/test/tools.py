from random import random
import numpy as np
from mock import Mock, patch
import requests
from matplotlib import image as img
from greengraph import Map

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
    red_probability = 0.333
    green_probability = 0.333
    for (x,y), value in np.ndenumerate(green_array[:,:,1]):
        ran = random()
        if ran < red_probability:
            green_array[x,y,0], multi_array[x,y,0] = 0, 1
        elif ran < green_probability + red_probability:
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

def bearing((lat1,long1),(lat2,long2)):
    lat1_r = lat1*np.pi/180.0
    long1_r = long1*np.pi/180.0
    lat2_r = lat2*np.pi/180.0
    long2_r = long2*np.pi/180.0
    y = np.sin(lat2_r-lat1_r)*np.cos(long2_r)
    x = np.cos(long1_r)*np.sin(long2_r) \
        - np.sin(long1_r)*np.cos(long2_r)*np.cos(lat2_r-lat1_r)
    return np.arctan2(x,y)*180.0/np.pi

def map_count(left,bottom,right,top,size=(400,400)):
    [lat, long] = [0.0, 0.0]
    image_array = colour_box((left,bottom,right,top),size=size)
    patch_imread = Mock(return_value=image_array)
    patch_get = Mock()
    patch_get.content = ''
    with patch.object(requests,'get',patch_get) as mock_get:
        with patch.object(img,'imread',patch_imread) as mock_imread:
            my_map = Map(lat, long)
    return my_map.count_green()
