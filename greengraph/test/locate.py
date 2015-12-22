from greengraph import Greengraph

graph = Greengraph('New York','Chicago')
assert graph.geolocate('London') == (51.5073509, -0.1277583)
print "Co-ordinates of London were obtained correctly. \n Test successful."
