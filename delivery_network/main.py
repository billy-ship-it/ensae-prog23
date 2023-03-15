import time
import math
from heapq import *
import numpy
import random
import graph 


data_path = "input/"
file_name = "routes.1.in"


#Q 10

def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        data = []
        for line in lines:
            numbers = [int(num) for num in line.split()]
            data.append(numbers)
    return data


def trajet_aleatoire(filename):                             # Attention ici, la notation semble indiquer qu'il s'agit d'un fichier quelconque, mais la fonction ne fonctionne qu'avec un fichier de type 'route'
    trajets= read_file(data_path+file_name)
    trajet_considere = random.choice(trajets)
    return trajet_considere[0:2]

G= graph.graph_from_file("input/network.1.in") 

src = trajet_aleatoire("input/routes.1.in")[0]
dest = trajet_aleatoire("input/routes.1.in")[1]

start = time.perf_counter()

G.min_power(src,dest)

end = time.perf_counter()
