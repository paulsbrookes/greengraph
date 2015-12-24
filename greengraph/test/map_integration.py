from mock import patch
from mock import Mock
from greengraph import Map
import requests
from matplotlib import image as img
from StringIO import StringIO
import numpy as np

base="http://maps.googleapis.com/maps/api/staticmap?"

[lat, long] = [51.0, 0.0]
patch_get = Mock()
patch_get.content = ''

[left,bottom,right,top] = [10,10,60,60]
image_array = np.zeros([400,400,3])
image_array[:,:,:] = 1
image_array[left:right,bottom:top,0] = 0
image_array[left:right,bottom:top,2] = 0
#image_array = img.imread('image.png')
patch_imread = Mock(return_value=image_array)

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

assert my_map.count_green() == 2500
