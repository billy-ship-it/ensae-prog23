
from graph import *
from truck import *
from route import *


def optimisation_profit(filename_routes, filename_trucks, budget):
    routes = route_from_file(filename_routes)
    camions = truck_from_file(filename_trucks)
    couts = []
    utilites = []

    for t in routes:                            # En supposant que chaque trajet t de routes.x.out est de la forme [puissance_minimale, utilité]
        puissance = t[0]
        cout_min = camions.camion_moins_cher(puissance)
        t.append(cout_min)
        t.reverse()
        t.pop()                                 #Les trajets sont désormais de la forme [cout_min, utilité]
        couts.append(t[0])
        utilites.append(t[1])
    n = len(couts)
    M = [[0 for j in range(budget+1)] for i in range(n+1)]

    for i in range(1, n+1):
        for j in range(1, budget+1):
            if couts[i-1] > j:
                M[i][j] = M[i-1][j]
            else:
                M[i][j] = max(M[i-1][j], utilites[i-1] + M[i-1][j-couts[i-1]])
    max_value = M[n][budget]
    selected_items = []

    i, j = n, budget

    while i > 0 and j > 0:
        if M[i][j] != M[i-1][j]:
            selected_items.append(i-1)
            j -= couts[i-1]
        i -= 1
    selected_items.reverse()

    return (max_value, selected_item)


def knapsack(B, filename_trucks, filename)