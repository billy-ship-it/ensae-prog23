import numpy as np
import math
from heapq import *


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
