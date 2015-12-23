from greengraph import Greengraph
import numpy as np

mygraph=Greengraph('New York','Chicago')
start = [0,0]
end = [1,1]
array1 = np.array([start])
array2 = np.array([start, end])
assert not mygraph.location_sequence(start,end,0)
assert np.all(mygraph.location_sequence(start,end,1)==array1)
assert np.all(mygraph.location_sequence(start,end,2)==array2)
