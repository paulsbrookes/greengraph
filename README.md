Greengraph coursework.

Greengraph is a package which allows you to plot the fraction of green space to
be found between two locations. It includes two classes:

1. greengraph.Map which has two mandatory arguments: a latitude and a longitude.
Given these arguments Map will retrieve an aerial photograph from Google Maps at
that location. It then has methods Map.green, Map.count_green and Map.show_green
to identify green pixels in the image, count the number of green pixels and
return this green image.

2. greengraph.Greengraph which must be supplied with the names of two locations
and which has methods Greengraph.geolocate, Greengraph.location_sequence and
Greengraph.green_between which will return the co-ordinates of a given location,
create a sequence of co-ordinates between two pairs of co-ordinates and calculate
the fraction of green space at each of these locations.

Greengraph comes with a command line interface. 

usage: greengraph [-h] [--steps STEPS] [--out OUT] [--start START] [--end END]

Plot the amount of green space between two locations.

optional arguments:
-h, --help     show this help message and exit
--steps STEPS  Number of steps plotted. Default value = 20.
--out OUT      Name of output file. "*.png" or "*.pdf"
--start START  Start location for plot. Default location is London.
--end END      End location of plot. Default location is Cambridge.
