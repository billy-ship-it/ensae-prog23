from route import *
from graph import *
from truck import *



data_path_routes = "/home/onyxia/work/ensae-prog23/output/"

filename_trucks = "/home/onyxia/work/ensae-prog23/input/trucks.2.in"

t = truck_from_file(filename_trucks)
for k in range(5, 10):
    print(construction_knapstack(data_path_routes + "routes." + str(k) + ".out", filename_trucks))
