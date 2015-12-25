from mock import patch, Mock
from matplotlib import image as img
import requests
from greengraph import Greengraph
import numpy as np
from matplotlib import pyplot as plt

def green_box(left,bottom,right,top,size=(400,400)):
    if not  (0 <= left <= right < size[0] and \
            0 <= bottom <= top < size[1]):
                raise ValueError(
                    "Require 0 <= left <= right < " + str(size[0]) + " and 0 <="
                    "bottom <= top < " + str(size[1]) + ".")
    image_array = np.zeros([size[0],size[1],3])
    image_array[:,:,:] = 1
    image_array[left:right,bottom:top,0] = 0
    image_array[left:right,bottom:top,2] = 0
    return image_array

def box_count(left,bottom,right,top):
    return abs(right-left)*abs(top-bottom)

steps = 400
image_arrays = [green_box(0,0,x,x) for x in range(steps)]

patch_imread = Mock()
patch_imread.side_effect = image_arrays

with patch.object(requests,'get') as mock_get:
    with patch.object(img,'imread',patch_imread) as mock_imread:
        mygraph=Greengraph('New York','Chicago')
        data = mygraph.green_between(steps)

assert [box_count(0,0,x,x) for x in range(steps)] == data
