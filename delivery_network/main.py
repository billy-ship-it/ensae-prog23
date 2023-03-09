from graph import *

data_path = "/home/onyxia/work/ensae-prog23/input/"
file_name = "network.00.in"

g = graph_from_file(data_path + file_name)

print(kruskal(g))