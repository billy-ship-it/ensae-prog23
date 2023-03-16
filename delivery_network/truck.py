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
            for numero, caracteristique in self.truck.items():
                output += f"camion {numero} a une puissance  de  {caracteristique[0]} et coûte {caracteristique[1]}\n"
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
        

#calculer le budget pour effectuer tous les trajets
#calculer pour un trajet donnée avec une certaine utilité, le camion le moins cher qui a la puissance suffisante pour
#pouvoir faire le trajet

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
    """
    budget = 0
    t = truck_from_file(filename_trucks)  # ici on a accès à un graphe
    puissance_trie = t.camion_trie_puissance()        
    with open(filename_trucks.replace("trucks", "routes").replace("in", "out"), 'r') as file:
        puissance = file.readlines()
        for k in range(1, len(puissance)):
            puissance[k] = puissance[k].split()
            puissance[k] = int(puissance[k][0])
    for k in range(1, len(puissance)):
        for camion in list(puissance_trie.keys()):
            if puissance_trie[camion] >= puissance[k]:
                budget += t.cout[camion]
                break
    return budget

