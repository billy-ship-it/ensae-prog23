from graph import Graph, graph_from_file


data_path = "input/"
file_name = "network.01.in"

g = graph_from_file(data_path + file_name)
print(g)

#Q 10


import time
import math
from heapq import *
import numpy
import random
from graph import (Graph, graph_from_file) 

G=graph_from_file ('routes.1.in')  # Problème routes.1.in n'est pas sous le format graphe

(src,dest) = random.sample(G.nodes,2)


start = time.perf_counter()

min_power (G,src,dest )

end = time.perf_counter ()