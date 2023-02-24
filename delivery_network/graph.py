import numpy as np
import math


class Graph:
    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0

    def __str__(self):
        """Prints the graph as a list of neighbors for each node 
        (one per line)"""
        if not self.graph:
            output = "The Graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is 
        added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        if node1 not in self.graph[node2]:
            self.graph[node1].append([node2, power_min, dist])
            self.graph[node2].append([node1, power_min, dist])
            self.nb_edges += 1        
    
    def get_path_with_power(self, src, dest, power):
        """ 
        Cette fonction renvoie None si il n'existe pas de chemin entre la  
        source et la destination, le chemin le plus court s'il existe
        """
        if dest not in self.connected_components_node(src):
            return None
        tableau = self.initialisation_tableau(src, dest, power)
        arrivee = False
        case_grise = [src]
        while not arrivee:
            tableau = self.parcourir_graphe(tableau, src, dest, arrivee, case_grise, power)
            if self.noeud_min(tableau, src, case_grise) == dest:
                break
        return self.explorer_noeud_precedent(dest, src, tableau, [])
    
    def initialisation_tableau(self, src, dest, power):
        """
        Cette fonction permet d'initialiser le tableau que nous utilisons pour
        la fonction get_path_with_power. Elle renvoie un tableau avec la 
        distance par rapport au point de départ. On met 0 pour la source,
        et inf pour les autres sommets
        """
        tableau = np.zeros((1, len(self.connected_components_node(src))+1))
        for k in range(len(self.connected_components_node(src)) + 1):
            tableau[0][k] = math.inf
        tableau[0, src] = 0
        return tableau

    def parcourir_graphe(self, tableau, src, dest, arrivee, case_grise, power):
        """
        Cette fonction permet de remplir le tableau que nous utilisons pour 
        l'algorithme de recherche du plus court chemin
        """
        noeud = self.noeud_min(tableau, src, case_grise)
        nouveau_tableau = self.creation_ligne(tableau, src, case_grise)
        # # on crée un nouveau tableau avec la nouvelle ligne avec dans 
        # la colonne départ le nouveau noeud 
        Voisins = self.noeuds_voisins(noeud)
        for k in range(1, len(self.connected_components_node(src)) + 1):
            puissance_arete = self.puissance(noeud, k)
            if k in Voisins and k not in case_grise and self.puissance(noeud, k) <= power:
                nouveau_tableau[-1][k] = self.distance(noeud, k) + nouveau_tableau[-2][noeud]
                if nouveau_tableau[- 2][k] < nouveau_tableau[- 1][noeud] + self.distance(noeud, k):  # si l'ancienne distance était plus courte, on la garde
                    nouveau_tableau[- 1][k] = nouveau_tableau[- 2][k] 
            elif k in case_grise:
                nouveau_tableau[- 1][k] = math.inf
            else:
                nouveau_tableau[- 1][k] = nouveau_tableau[- 2][k]
        nouveau_tableau[- 1][noeud] = math.inf
        return nouveau_tableau

    def creation_ligne(self, tableau, src, case_grise):
        """ 
        Cette fonction crée une nouvelle ligne et l'ajoute au tableau
        """
        nouvelle_ligne = np.zeros((1, len(self.connected_components_node(src)) + 1))
        nouvelle_ligne[0][0] = self.noeud_min(tableau, src, case_grise)
        tableau = np.vstack([tableau, nouvelle_ligne])
        return tableau
    
    def noeud_min(self, tableau, src, case_grise):
        """
        Cette fonction renvoie le noeud de la dernière ligne du tableau ayant
        la distance minimale de telle sorte à pourvoir explorer les
        voisins de ce noeud
        """
        noeud_min = 0
        min_ligne_precedente = math.inf
        for k in range(1, len(self.connected_components_node(src)) + 1):
            if tableau[- 1][k] < min_ligne_precedente:
                noeud_min = k
                min_ligne_precedente = tableau[- 1][k]
        case_grise.append(noeud_min)
        return noeud_min
    
    def distance(self, noeud, voisin):
        """
        Cette fonction renvoie la distance
        entre deux noeuds
        """
        liste = self.graph[noeud]
        for element in liste:
            distance = element[2]
            noeud_voisin = element[0]
            if noeud_voisin == voisin:
                return distance
    
    def puissance(self, noeud, voisin):
        liste = self.graph[noeud]
        for element in liste:
            noeud_voisin = element[0]
            power = element[1]
            if noeud_voisin == voisin:
                return power

    def noeuds_voisins(self, node):
        """
        Cette fonction renvoie la liste des noeuds voisins
        """
        liste = self.graph[node]
        if len(liste) == 1:
            return liste
        else:
            liste = np.array(liste)
            liste = liste[:, 0]
            return liste

    def explorer_noeud_precedent(self, noeud, src, tableau, CHEMIN):
        """
        Cette fonction ajoute dans la liste chemin les noeuds par 
        lesquels le chemin doit passer
        """
        while noeud != src:
            CHEMIN.append(noeud)
            noeud = int(self.noeud_precedent(noeud, tableau))
        CHEMIN.append(src)
        CHEMIN.reverse()
        return CHEMIN
        
    def noeud_precedent(self, node, tableau):
        """
        Cette fonction renvoie le noeud qui précède node
        """
        liste = tableau[:, node]
        minimum_liste = min(liste)
        for k in range(0, len(liste)):
            if liste[k] == minimum_liste:
                return tableau[k][0]  # renvoie le noeud precedent

    def connected_components(self):
        L = [0]*self.nb_nodes  # initialisation d'une liste pour savoir si les 
        #  sommet ont déja été parcourus
        compteur = 1  # on initialise le compteur
        for node in range(1, self.nb_nodes + 1):
            if L[node - 1] == 0:
                self.explorer(node, L, compteur)  # ce qui revient à modifier
            #  la liste L pour connaître les sommmets qui ont déja été parcours 
                compteur += 1
        LIST = []
        for compteur in range(1, max(L) + 1):
            V = []
            for node in range(1, self.nb_nodes + 1):
                if L[node - 1] == compteur: 
                    V.append(node)  # On met dans la même liste tous les 
                    # sommets qui sont reliés entre eux
            LIST.append(V)
        return LIST
    
    def explorer(self, node, L, compteur):
        L[node - int(1)] = compteur  # Lorsque l'on se rend sur on nouveau  
        # sommet, on le marque
        element = self.graph[node]
        for noeud in element:
            voisin = noeud[0]
            if L[voisin - 1] == 0:
                self.explorer(voisin, L, compteur)  # On marque 
    #  tous les sommets qui sont voisins avec le sommet initial

    def connected_components_node(self, node):
        L = self.connected_components()
        for element in L:
            if node in element:
                return element

    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: 
        {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))
    
    def min_power(self, src, dest):
        """
        Should return path, min_power. 
        """
        raise NotImplementedError
    


    def creation_bijection(self):
        """
        Cette fonction crée une bijection entre des sommets et des numéros
        """
        liste = self.nodes
        nouvelle_liste = Graph([i for i in range(1, len(liste) + 1)])
        self = nouvelle_liste
        for k in range(len(liste)):
            dictionnaire = self.graph[liste[k]]
            for element in dictionnaire:
                voisin = element[0]
                power = element[1]
                dist = element[2]
                nouvelle_liste.add_edge(k + 1, self.indice(voisin) + 1, power)
        self = nouvelle_liste
        return self


    def indice(self, node):
        liste = self.nodes
        for k in range(len(liste)):
            if liste[k] == node:
                return k

def graph_from_file(filename):
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 
        power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters: 
    -----------
    filename: str
        The name of the file

    Outputs: 
    -----------
    G: Graph
        An object of the class Graph with the graph from file_name.
    """
    with open(filename, "r") as file:
        n, m = map(int, file.readline().split())
        g = Graph(range(1, n+1))
        for _ in range(m):
            edge = list(map(int, file.readline().split()))
            if len(edge) == 3:
                node1, node2, power_min = edge
                g.add_edge(node1, node2, power_min) # will add dist=1 by default
            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)
            else:
                raise Exception("Format incorrect")
    return g
