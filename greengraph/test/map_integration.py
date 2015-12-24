from mock import patch
from mock import Mock
from greengraph import Map
import requests
from matplotlib import image as img
from StringIO import StringIO

with open('image.txt','r') as source:
    text = source.read()

lat=51
long=30
satellite=True
zoom=10
size=(400,400)
sensor=False

params=dict(
    sensor= str(sensor).lower(),
    zoom= zoom,
    size= "x".join(map(str, size)),
    center= ",".join(map(str, (lat, long) )),
    style="feature:all|element:labels|visibility:off"
    )
base="http://maps.googleapis.com/maps/api/staticmap?"

text = requests.get(base, params=params).content # Fetch our PNG image data
text = 'hello'

image = Mock()
image.content = text
patch_get = Mock(return_value=image)


with patch.object(requests,'get',patch_get) as mock_get:
    with patch.object(img,'imread') as mock_imread:
        london_map = Map(52, 0)

print mock_get.mock_calls
print mock_imread.mock_calls
print london_map.count_green()
