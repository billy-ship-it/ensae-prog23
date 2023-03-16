import numpy as np
import math
from heapq import *
from graphviz import Graph as gr

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
            self.graph[node1].append((node2, power_min, dist))
            self.graph[node2].append((node1, power_min, dist))
            self.nb_edges += 1      

    def get_path_with_power(self, src, dest, power):
        liste = self.connected_components_node(src)              # Cette première partie de la fonction sert à vérifier qu'il existe bien un chemin possible entre src et dest. 
        if dest not in liste:
            return None
        return self.dijkstra(src, dest, power)                   # Complexité donc en O(V*(E+V!)) d'après celle des fonction précédentes

    def dijkstra(self, s, t, power):                              # Algorithme qui retourne le plus court chemin à partir d'un trajet
        Vu = set()
        d = {s: 0}
        prédecesseurs = {}
        suivants = [(0, s)]  # Â tas de couples (d[x],x)           #Création de listes qui seront incrémentées/dépilées au fur et à mesure du parcours de la composante connexe
        while suivants != []:                                       # V occurences au plus 
            dx, x = heappop(suivants)                              # Implémentation de la priorité d'exploration de ce qui reste à explorer
            if x in Vu:
                continue
            Vu.add(x)
            for y, p, w in self.graph[x]:                         # E occurrences au plus, dans le cas ou x est "au centre" d'un graphe de rayons autour de x
                if y in Vu:
                    continue
                dy = dx + w
                if (y not in d or d[y] > dy) and power >= p:       # Double condition de puissance et de plus courte ditance
                    d[y] = dy
                    heappush(suivants, (dy, y))
                    prédecesseurs[y] = x
        path = [t]
        x = t
        if t not in d:
            return None
        while x != s:                                               # V occurences au plus
            x = prédecesseurs[x]
            path.insert(0, x)
        return path

    def connected_components(self):
        visite = {node: 0 for node in self.nodes}                                       # initialisation d'une liste pour savoir si les sommets ont déjà été visités
        compteur = 1                                                # on initialise le compteur
        for node in self.nodes:                    # V occurrences
            if visite[node] == 0:
                self.explorer(node, visite, compteur)                   # ce qui revient à modifier la liste L pour connaître les sommmets qui ont déja été parcourus 
                compteur += 1
        
        grouped = {}
        for key, value in visite.items():
            if value in grouped:
                grouped[value].append(key)
            else:
                grouped[value] = [key]
        return [nodes for nodes in grouped.values()]                                             # Complexité en O(V*V!), fonctionne donc pour un graphe de taille réduite.
    
    def explorer(self, node, visite, compteur):
        visite[node] = compteur                                # Lorsque l'on se rend sur on nouveau sommet, on le marque
        voisins = self.graph[node]
        for element in voisins:                                      # Au plus V occurrences
            voisin = element[0]
            if visite[voisin] == 0:
                self.explorer(voisin, visite, compteur)                 # On marque tous les sommets qui sont voisins avec le sommet initial

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
        left = 0  # on initialise la borne inférieure
        right = 0  # on initialise la borne supérieure
        for node1 in self.nodes:
            for element in self.graph[node1]:
                node2, power, distance = element
                if power > right:
                    right = power  # on attribue à la variable right la
                    # plus grande puissance du graphe

        while left <= right:  # Nous procédons par dichotomie
            mid = (left + right) // 2
            path = self.get_path_with_power(src, dest, mid)
            if path is not None:
                right = mid - 1
            else:
                left = mid + 1
        
        return self.get_path_with_power(src, dest, left), left
            
    def representation(self, nom):
        graphe = gr(format='png', engine="circo")  # on a un objet graphviz
        key = self.graph.keys()  # on prend les clés du dictionnaire associé au graphe
        sauv = []
        for i in key:  # on parcourt tous les sommets
            graphe.node(f"{i}", f"{i}")
            for element in self.graph[i]:  # on regarde les noeuds vers lesquels le noeud pointe
                noeud_voisin, puissance, distance = element
                if noeud_voisin not in sauv:
                    graphe.edge(f"{i}", f"{noeud_voisin}", label=f"p={puissance},\n d={distance}", color="green")
            sauv.append(i)
        graphe.render(f"{nom}.dot")
        return ()


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
                g.add_edge(node1, node2, power_min, dist=1) # will add dist=1 by default
            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)
            else:
                raise Exception("Format incorrect")
    return g
        

def find(parent, i):  # permet de dire 
    if parent[i] == i:
        return i
    return find(parent, parent[i])


def union(parent, rank, x, y):  # parent est le dictionnaire à modifier
    """ Union est une fonction qui modifie le dictionnaire parent
    """
    xroot = find(parent, x)  # on cherche le noeud racine de x
    yroot = find(parent, y)  # on cherche le noeud racine de y
    if rank[xroot] < rank[yroot]:  # on modifie le dictionnaire parent pour attacher l'arbre le plus petit à la racine de l'arbre le pluls grand
        parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parent[yroot] = xroot
    else:
        parent[yroot] = xroot
        rank[xroot] += 1


def kruskal(graph):
    result = {}
    i = 0
    e = 0
    parent = {node: node for node in graph.nodes}  # on initialise le dictionnaire
    rank = {node: 0 for node in graph.nodes}  # on initialise le dictionnaire
    L = []
    for node in graph.nodes:
        for element in graph.graph[node]:
            noeud, puissance, distance = element
            L.append([node, noeud, puissance, distance])
    L = sorted(L, key=lambda item: item[2])  # Trie les arêtes par ordre croissant de puissance
    while e < graph.nb_nodes - 1 and i < len(L):
        u, v, w, z = L[i]
        i += 1  # i est l'indice qui parcourt tous l'ensemble des arêtes
        x = find(parent, u)  # on cherche les racines du noeud u
        y = find(parent, v)  # on chercher les racines du noeud v
        if x != y:  # si les deux noeuds n'ont pas la même racine
            e += 1  # on rajoute une arête au compteur
            if u not in result:
                result[u] = [(v, w, z)]
            else:
                if (v, w, z) not in result[u]:
                    result[u].append((v, w, z))  # on rajoute dans le
                    # dictionnaire
            if v not in result:
                result[v] = [(u, w, z)]
            else:
                if (u, w, z) not in result[v]:
                    result[v].append((u, w, z))
            union(parent, rank, u, v)  # on met à jour le dictionnaire pour 
            # dire que 

    sorted_keys = sorted(result.keys())

    sorted_result = {}

    for key in sorted_keys:

        sorted_result[key] = result[key]

    graphe_final = Graph(graph.nodes)
    for node1 in sorted_result.keys():
        for element in sorted_result[node1]:
            node2, puissance, distance = element
            if (node2, puissance, distance) not in graphe_final.graph[node1]:
                graphe_final.graph[node1].append((node2, puissance, distance))
            if (node1, puissance, distance) not in graphe_final.graph[node2]:
                graphe_final.graph[node2].append((node1, puissance, distance))

    return graphe_final


    #Question 11#
    """ Il ne peut y avoir deux chemins reliant 2 sommets quelconques d'un arbre couvrant de poids minimal, puisque l'arbre n'est pas cyclique par définition.
    Parcourons désormais l'arbre couvrant de poids minimal depuis une source quelconque.
    Chaque arête d'un arbre couvrant de poids minimal sert à l'exploration d'un nouveau point : on n'accède pas à ce point depuis la source par une autre arête, 
    puisqu'il n'existe qu'un seul chemin reliant la source à ce point. Ainsi à chaque nouvelle arête comptée on ajoute un nouveau point, l'opération 
    s'arrêtant lorsque tous les points ont été explorés. Ainsi donc, pour V le nombre d'arêtes comptées dans l'arbre couvrant de poids minimal, on y recense donc V +1
     (en ajoutant la source initiale) sommets le composant.   """



    #Question 14#  


    def min_power2(self, src, dest):
        "on crée une fonction simple qui trouve le chemin unique entre deux noeuds, src et dest, de notre arbre couvrant de poids minimal"
        stack = [src]
        visited = set([src])
        parent = {src: None}
        power = {src : 0}
        power_min = 0
        while stack:
            node = stack.pop()
            "nous avons trouvé le nœud que nous recherchons, donc construisons le chemin "
            if node == dest:
                path = []
                while node:
                    if power[node] > power_min:
                        power_min = power[node]
                    path.insert(0, node)
                    node = parent[node]
                return power_min, path
            for child in self.graph[node]:
                child , pow = child[0], child[1]
                if child not in visited:
                    visited.add(child)
                    stack.append(child)
                    parent[child] = node
                    power[child] = pow 

#nous n'avons pas trouvé le nœud que nous recherchions, donc il n'y a pas de chemin   
             



        

