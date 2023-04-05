from graph import *
from truck import *
from route import *
import random



def sort(filename_routeXtrucks):
    """Cette fonction trie les lignes des fichiers routestrucks
    suivant le rapport de l'utilité décroissant
    """
    with open(filename_routeXtrucks, 'r') as f:
        g = []
        lines = f.readlines()
        for k in range(len(lines)):
            lines[k] = lines[k].split()

            if len(lines[k]) == 3:
                lines[k][0] = int(lines[k][0])
                lines[k][1] = int(lines[k][1])
                lines[k][2] = float(lines[k][2])

            else:
                g.append(k)
        
    
    lines.sort(key=lambda item: item[2], reverse=True)

    with open("/home/onyxia/work/ensae-prog23/output/sorted" + str(filename_routeXtrucks[filename_routeXtrucks.find("routes"):]), 'w') as file:
        for k in range(len(lines)):
            file.write(str(lines[k][0]) + " " + str(lines[k][1]) + " " + str(lines[k][2]) + "\n")
    


def optimisation_profit_(filename_routes, filename_trucks, budget):
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


def calcul_profit_naif(B, filename_sortedroutesXtrucks):
    """ Cette fonction renvoie l'utilité et le profit pour un 
    fichier route et un fichier trucks. L'algorithme est tel que
    l'on sélectionne les trajets selon le rapport utilite/coût
    jusqu'à ce qu'on n'ait plus assez d'argent
    """

    chemin_camion = "/home/onyxia/work/ensae-prog23/input/" + filename_sortedroutesXtrucks[filename_sortedroutesXtrucks.find("trucks"):].replace("trucks", "trucks.").replace("out", "in")
    chemin_route = "/home/onyxia/work/ensae-prog23/input/" + filename_sortedroutesXtrucks[filename_sortedroutesXtrucks.find("routes"): filename_sortedroutesXtrucks.find("trucks")] + ".out"

    t = truck_from_file(chemin_camion)
    depense = 0
    profit = 0
    
    with open(filename_sortedroutesXtrucks, 'r') as f:
        lines = f.readlines()
        for k in range(len(lines)):
            lines[k] = lines[k].split()
            for j in range(0, 2):
                lines[k][j] = int(lines[k][j])

    if budget_trajet(filename_sortedroutesXtrucks) <= B: # On vérifie si on peut acheter tous les camions avec notre budget, auquel cas nous n'avons pas besoin de
        #  d'essayer d'optimiser
        return budget_trajet(filename_sortedroutesXtrucks), sum(list(map(lambda item: item[1], lines))), 0
    
    k = 0 
    
    while depense + lines[k][0] < B and k < len(lines):
        cout, utilite = lines[k][0], lines[k][1]
        profit += utilite
        depense += cout
        k += 1
    
    cout_camion_min = min(lines[k:], key=lambda item: item[0])[0]

    return depense, profit, k


def aleatoire(B, filename_sortedroutesXtrucks, nb_iteration):
    """ Cette fonction tire aléatoirement des lignes dans les
    fichier sortedroutesXtrucks pour les ajouter dans le 
    le profit total
    """

    chemin_camion = "/home/onyxia/work/ensae-prog23/input/" + filename_sortedroutesXtrucks[filename_sortedroutesXtrucks.find("trucks"):].replace("trucks", "trucks.").replace("out", "in")


    with open(filename_sortedroutesXtrucks, 'r') as f:
        lines = f.readlines()
        for k in range(len(lines)):
            lines[k] = lines[k].split()
            for j in range(0, 2):
                lines[k][j] = int(lines[k][j])

    if budget_trajet(filename_sortedroutesXtrucks) <= B:
        return budget_trajet(filename_sortedroutesXtrucks), sum(list(map(lambda item: item[1], lines)))

    dic_parent = {}
    max = 0

    for i in range(1, nb_iteration + 1):

        depense = 0
        utilite = 0
        L = []
        dic_indice = {n: 0 for n in range(0, len(lines))}

        while depense < B:

            indice = random.randint(0, len(lines) - 1)
            if dic_indice[indice] == 0:
                depense += lines[indice][0]
                utilite += lines[indice][1]
                L.append(lines[indice])
            
            dic_indice[indice] = 1

        if max < utilite:
            max = utilite

        dic_parent[i] = (L, depense, utilite)
        print(utilite)

    return max

            
def calcul_profit_beta(B, filename_sortedroutesXtrucks, stop, beta):
    """ Cette fonction est une variante de la fonction calcul_profit_naif
    L'idée est qu'on prend les "stop" premiers trajets rangés par ordre
    décroissant suivant le rapport utilité, coût. Ensuite pour le budget restant, 
    on prend les trajets suivant avec la probabilité beta.
    """
    chemin_camion = "/home/onyxia/work/ensae-prog23/input/" + filename_sortedroutesXtrucks[filename_sortedroutesXtrucks.find("trucks"):].replace("trucks", "trucks.").replace("out", "in")
    depense = 0
    profit = 0

    with open(filename_sortedroutesXtrucks, 'r') as f:
        lines = f.readlines()
        for k in range(len(lines)):
            lines[k] = lines[k].split()
            for j in range(0, 2):
                lines[k][j] = int(lines[k][j])

    if budget_trajet(filename_sortedroutesXtrucks) <= B:
        return budget_trajet(filename_sortedroutesXtrucks), sum(list(map(lambda item: item[1], lines)))

    indice_stop = int(calcul_profit_naif(B, filename_sortedroutesXtrucks)[2] *stop//1)

    k = 0

    while depense + lines[k][0] < B and k < indice_stop:
        cout, utilite = lines[k][0], lines[k][1]
        profit += utilite
        depense += cout
        k += 1

    j = indice_stop

    while depense + lines[j][0] < B and j < len(lines) - 1:
        if random.random() < beta:
            cout, utilite = lines[j][0], lines[j][1]
            profit += utilite
            depense += cout
        j += 1

    return depense, profit


    
        






