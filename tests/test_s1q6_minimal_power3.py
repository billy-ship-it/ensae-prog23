# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network")

from graph import graph_from_file
import unittest   # The test framework
from graph import *

# Ce premier test vérifie si les trajets renvoyés sont les mêmes
class Test_MinimalPower(unittest.TestCase):
    def test_network0(self):
        g = graph_from_file("input/network.00.in")
        arbre, hauteur, puissance = g.dictionnaire_kruskal()
        self.assertEqual(g.min_power3(1, 4, arbre, hauteur, puissance), g.min_power(1, 4))
        self.assertEqual(g.min_power3(2, 4, arbre, hauteur, puissance), g.min_power(2, 4))

    def test_network1(self):
        g = graph_from_file("input/network.04.in")
        arbre, hauteur, puissance = g.dictionnaire_kruskal()
        self.assertEqual(g.min_power3(1, 4, arbre, hauteur, puissance), g.min_power(1, 4))

if __name__ == '__main__':
    unittest.main()



