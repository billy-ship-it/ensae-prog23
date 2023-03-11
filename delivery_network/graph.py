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
        liste = self.connected_components_node(src)
        if dest not in liste:
            return None
        return self.dijkstra(src, dest, power)

    def dijkstra(self, s, t, power):
        Vu = set()
        d = {s: 0}
        prédecesseurs = {}
        suivants = [(0, s)]  # Â tas de couples (d[x],x)
        while suivants != []:
            dx, x = heappop(suivants)
            if x in Vu:
                continue
            Vu.add(x)
            for y, p, w in self.graph[x]:
                if y in Vu:
                    continue
                dy = dx + w
                if (y not in d or d[y] > dy) and power >= p:
                    d[y] = dy
                    heappush(suivants, (dy, y))
                    prédecesseurs[y] = x
        path = [t]
        x = t
        if t not in d:
            return None
        while x != s:
            x = prédecesseurs[x]
            path.insert(0, x)
        return path
 
    def puissance_min(self, power_precedent):
        power_min = math.inf
        L = []
        for node1 in range(1, self.nb_nodes + 1):
            for element in self.graph[node1]:
                node2, puissance, distance = element
                if puissance <= power_min and puissance > power_precedent:
                    power_min = puissance
                    L.append([node1, node2, puissance, distance])
        if len(L) == 0:
            return None
        L.reverse()
        D = [L[0]]
        power_min = L[0][2]
        for k in range(len(L)):
            if L[k][2] == power_min:
                D.append(L[k])
        return D

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
        power = 0
        while not self.get_path_with_power(src, dest, power):
            power += 1
        return self.get_path_with_power(src, dest, power), power

    def indice(self, node):
        liste = self.nodes
        for k in range(len(liste)):
            if liste[k] == node:
                return k
    
    def representation(self, nom):
        graphe = gr(format='png', engine="circo") # on a un objet graphviz
        key = self.graph.keys() # on prend les clés du dictionnaire associé au graphe
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


def find(parent, i):  # permet de déterminer dans quelle composante connexe le noeud i est 
    if parent[i] == i:
        return i
    return find(parent, parent[i])


def union(parent, rank, x, y):  # parent est le dictionnaire à modifier
    """ Union est une fonction qui modifie le dictionnaire parent
    """
    xroot = find(parent, x)  # on cherche le noeud racine de x
    yroot = find(parent, y)  # on cherche le noeud racine de y

    if rank[xroot] < rank[yroot]:  # on modifie le dictionnaire parent pour attacher l'arbre le plus petit à la racine de l'arbre le plus grand
        parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parent[yroot] = xroot
    else:
        parent[yroot] = xroot
        rank[xroot] += 1


def kruskal(graph):
    result = {}
    i = 0
    e = 0 # correspond au nombre d'arêtes du nouveau graphe
    parent = {node: node for node in graph.nodes}  # on initialise le dictionnaire pour que les noeuds ne soient pas dans la même composante connexe au début
    rank = {node: 0 for node in graph.nodes}  # on initialise le dictionnaire
    L = []
    for node in graph.nodes:
        for element in graph.graph[node]:
            noeud, puissance, distance = element
            L.append([node, noeud, puissance, distance])
    L = sorted(L, key=lambda item: item[2])  # Correspond aux arêtes rangées par ordre croissant de puissance

    while e < graph.nb_nodes - 1 and i < len(L):  # L'arbre est couvrant lorsque e = nombre de noeuds - 1
        u, v, w, z = L[i]
        i += 1  # on augmente i, l'indice qui parcourt l'ensemble des arêtes
        x = find(parent, u)  # on cherche les racines du noeud u
        y = find(parent, v)  # on chercher les racines du noeud v
        if x != y:  # si les deux noeuds n'ont pas la même racine, alors ils ne sont pas dans la même composante connexe
            e += 1  # on rajoute une arête au compteur
            if u not in result:
                result[u] = [(v, w, z)]
            else:
                if (v, w, z) not in result[u]:
                    result[u].append((v, w, z))  # on rajoute dans le dictionnaire
            if v not in result:
                result[v] = [(u, w, z)]
            else:
                if (u, w, z) not in result[v]:
                    result[v].append((u, w, z))
            union(parent, rank, u, v)  # on met à jour le dictionnaire pour dire que les deux noeuds ont été reliés

    sorted_keys = sorted(result.keys())
    sorted_result = {}

    for key in sorted_keys:
        sorted_result[key] = result[key]

    graphe_final = Graph(graph.nodes)  # on construit un objet de type graphe
    for node1 in sorted_result.keys():
        for element in sorted_result[node1]:
            node2, puissance, distance = element
            if (node2, puissance, distance) not in graphe_final.graph[node1]:
                graphe_final.graph[node1].append((node2, puissance, distance))
            if (node1, puissance, distance) not in graphe_final.graph[node2]:
                graphe_final.graph[node2].append((node1, puissance, distance))

    return graphe_final
