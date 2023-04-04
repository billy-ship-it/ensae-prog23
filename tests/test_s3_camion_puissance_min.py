import sys 
sys.path.append("delivery_network")
from truck import *
import unittest

class Test_MST(unittest.TestCase):
    def test_trucks0(self):
        g = truck_from_file("input/trucks.0.in")
        self.assertEqual(g.camion_puissance_min(), 1)

    def test_truck1(self):
        g = truck_from_file("input/trucks.1.in")
        self.assertEqual(g.camion_puissance_min(), 1)

    def test_truck2(self):
        g = truck_from_file("input/trucks.2.in")
        self.assertEqual(g.camion_puissance_min(), 1)
if __name__ == '__main__':
    unittest.main()