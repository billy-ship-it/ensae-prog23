from graph import *
data_path = "/home/onyxia/work/ensae-prog23/input/"
file_name = "network.02.in"

g = graph_from_file(data_path + file_name)
print(g.representation("graphique")) 