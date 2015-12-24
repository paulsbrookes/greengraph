from mock import patch
from mock import Mock
from greengraph import Map
import requests
from matplotlib import image as img
from StringIO import StringIO

patch_get = Mock()
patch_get.content = ''

image_array = img.imread('image.png')
patch_imread = Mock(return_value=image_array)

with patch.object(requests,'get',patch_get) as mock_get:
    with patch.object(img,'imread',patch_imread) as mock_imread:
        my_map = Map(0, 0)

print mock_get.mock_calls
print mock_imread.mock_calls
print my_map.count_green()
