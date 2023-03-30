from route import *
from graph import *
from truck import *



datapath = "/home/onyxia/work/ensae-prog23/input/"
filename = "network.00.in"

g = graph_from_file("input/network.00.in")
arbre, hauteur, puissance = g.dictionnaire_kruskal()
print(g.min_power3(4, 1, arbre, hauteur, puissance), g.min_power(4, 1)[0])
print(hauteur)