from route import *
from graph import *
from truck import *



data_path_routes = "/home/onyxia/work/ensae-prog23/output/"
filename_routes = "routes.1.out"

filename_trucks = "/home/onyxia/work/ensae-prog23/input/trucks.0.in"

t = truck_from_file(filename_trucks)

for j in range(0, 3):
    for k in range(1, 10):
        print(rapport("/home/onyxia/work/ensae-prog23/output/" + "routes." + str(k) + ".out", "/home/onyxia/work/ensae-prog23/input/trucks." + str(j) + ".in"))
