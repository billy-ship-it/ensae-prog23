
from graph import *
from truck import *
from route import *



def sort(filename_routeXtrucks):
    """Cette fonction trie les lignes des fichiers routestrucks
    suivant le rapport de l'utilité décroissant
    """
    with open(filename_routeXtrucks, 'r') as f:
        lines = f.readlines()
        for k in range(len(lines)):
            lines[k] = lines[k].split()
            for j in range(0, 2):
                lines[k][j] = int(lines[k][j])
            lines[k][2] = float(lines[k][2])
    lines.sort(key=lambda item: item[2], reverse=True)

    with open( "/home/onyxia/work/ensae-prog23/output/sorted" + str(filename_routeXtrucks[filename_routeXtrucks.find("routes"):]), 'w') as file:
        for k in range(len(lines)):
            file.write(str(lines[k][0]) + " " + str(lines[k][1]) + " " + str(lines[k][2]) + "\n")
    


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

def calcul_profit(B, filename_sortedroutesXtrucks):
    t = truck_from_file("/home/onyxia/work/ensae-prog23/input" + filename_sortedroutesXtrucks[filename_sortedroutesXtrucks.find(trucks):].replace("out", "in"))
    depense = 0
    profit = 0
    k = 0

    cout_camion_min = t.cout[t.camion_cout_min()]

    with open(filename_sortedroutesXtrucks, 'r') as f:
        lines = f.readlines()
        for k in range(len(lines)):
            lines[k] = lines[k].split()
            for j in range(0, 2):
                lines[k][j] = int(lines[k][j])
    
    while depense < B:
        cout, utilite = lines[k][0:1]
        profit += utilite
        depense += cout
        k += 1

    marge = B - depense

    if marge < cout_camion_min:
        return profit, depense
    else:
        while marge >= cout_camion_min:
            cout, utilite = lines[k][0:1]
            profit += utilite
            depense





