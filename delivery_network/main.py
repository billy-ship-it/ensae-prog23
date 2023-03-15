from graph import Graph, graph_from_file


data_path = "/home/onyxia/work/ensae-prog23/input/"
file_name = "network.01.in"



#Q 10


import time
import math
from heapq import *
import numpy
import random



def trajet_aleatoire (filename):                             # Attention ici, la notation semble indiquer qu'il s'agit d'un fichier quelconque, mais la fonction ne fonctionne qu'avec un fichier de type 'route'
    with open (filename, "r") as file:
        trajets = list(map(int,file.readline().split()))
        trajet_considere = random.choice(trajets)
    return trajet_considere[0:2]


G = graph_from_file(data_path + file_name) 
print(G)


src = trajet_aleatoire("input/routes.1.in")[0]
dest = trajet_aleatoire("input/routes.1.in")[1]


start = time.perf_counter()

G.min_power(src,dest)

end = time.perf_counter()
