import re
import math

class Trucks:
    def __init__(self, trucks):
        self.truck = dict([(n, []) for n in range(1, trucks + 1)])
        self.nb_trucks = trucks
        self.puissance = dict([(n, []) for n in range(1, trucks + 1)])
        self.cout = dict([(n, []) for n in range(1, trucks + 1)])

    def __str__(self):
        if not self.truck:
            output = "le catalogue est vide"
        else:
            output = f"le catalogue est composé de {self.nb_trucks} camion(s).\n"
            for numero, (puissance, cout) in self.truck.items():
                output += f"camion {numero} a une puissance  de  {puissance} et coûte {cout}\n"
        return output

    def camion_cout_min(self):
        """ Cette fonction renvoie le camion qui a le plus petit
        cout du catalogue
        """
        return min(self.cout, key=self.cout.get)
    
    def camion_puissance_min(self):
        """ Cette fonction renvoie le camion qui a la plus
        petite puissance du catalogue
        """
        return min(self.puissance, key=self.puissance.get)

    def camion_puissance_max(self):
        """ Cette fonction renvoie le camion qui a la plus
        grande puissance du catalogue
        """
        return max(self.puissance, key=self.puissance.get)
    
    def camion_trie_puissance(self):
        """Cette fonction renvoie un dictionnaire trié suivant 
        la puissance croissante des camions du catalogue
        """
        return dict(sorted(self.puissance.items(), key=lambda item :item[1]))

    def camion_trie_cout(self):
        """Cette fonction renvoie un dictionnaire trié suivant 
        le coût croissant des camions du catalogue
        """
        return dict(sorted(self.cout.items(), key=lambda item : item[1]))
        
    def camion_moins_cher(self, puissance):
        """ Cette fonction renvoie le camion le moins cher avec
        la puissance suffisante pour faire le trajet
        """
        puissance_trie = self.camion_trie_puissance()  # on trie les camions par ordre croissant de puissance
        dict_cout = {}
        for camion in list(puissance_trie.keys()):
            if self.puissance[camion] >= puissance:  # si la puissance du camion est suffisante, on recrée un dictionnaire
                dict_cout[camion] = self.cout[camion]
        if len(dict_cout) == 0:
            return 
        return min(dict_cout, key=dict_cout.get)


def truck_from_file(filename):
    """ créer un dictionnaire avec pour clés les catégories de camions et en
    arguments la puissance et le coût du camion

    La fonction prend en entrée des fichiers du type trucks.nombre.in
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
        for k in range(len(lines)):
            lines[k] = lines[k].split()
            for j in range(len(lines[k])):
                lines[k][j] = int(lines[k][j])
        nombre_camions = lines[0][0]
        t = Trucks(nombre_camions)
        for k in range(1, nombre_camions + 1):
            t.truck[k] = tuple(lines[k])
            t.puissance[k] = (lines[k][0])
            t.cout[k] = (lines[k][1])
        return t


def budget_trajets(filename_trucks):
    """ Cette fonction calcule le budget qui serait nécéssaire pour couvrir
    l'ensemble des trajets
    Ici la foncion marche si les différents camions du catalogue ont des 
    puissances différentes
    """
    budget = 0
    t = truck_from_file(filename_trucks)  # ici on a accès à un graphe
    puissance_trie = t.camion_trie_puissance()  # on a un dictionnaire trié selon la puissance croissante des camions      
    with open(filename_trucks.replace("trucks", "routes").replace("in", "out"), 'r') as file:
        puissance = file.readlines()
        for k in range(1, len(puissance)):
            puissance[k] = puissance[k].split()
            puissance[k] = int(puissance[k][0])
    for k in range(1, len(puissance)):
        for camion in list(puissance_trie.keys()):
            if puissance_trie[camion] >= puissance[k]:  # 2 camions peuvent-ils avoir la même puissance?
                budget += t.cout[camion]
                break
    return budget


def rapport(filename_routesout, filename_truck):
    t = truck_from_file(filename_truck)
    cout = t.cout
    puissance = t.puissance
    power_max = t.puissance[t.camion_puissance_max()]

    numero_routes = re.sub("[^0-9]", "", filename_routesout).replace("23", "")
    numero_trucks = re.sub("[^0-9]", "", filename_truck).replace("23", "")

    with open(filename_routesout, 'r') as f:
        lines = f.readlines()
        with open("/home/onyxia/work/ensae-prog23/output/" + "routes" + numero_routes + "trucks" + numero_trucks + ".out", 'w') as file:
            for k in range(1, len(lines)):
                lines[k] = lines[k].split()
                lines[k] = list(map(int, lines[k]))   
                power, utilite = lines[k]
                if power <= power_max:
                    file.write(str(t.cout[t.camion_moins_cher(power)]) + " " + str(utilite) + " " + str(utilite/t.cout[t.camion_moins_cher(power)]) +"\n")