import sys 
sys.path.append("delivery_network")
from truck import *
import unittest

class Test_MST(unittest.TestCase):
    def test_truck0(self):
        g = truck_from_file("input/trucks.0.in")
        self.assertEqual(g.camion_moins_cher(1000000), 1)
        self.assertEqual(g.camion_moins_cher(3000000), 2)

    def test_truck1(self):
        g = truck_from_file("input/trucks.1.in")
        self.assertEqual(g.camion_moins_cher(2000000 - 1), 4)
        self.assertEqual(g.camion_moins_cher(6500000 - 1), 13)


    def test_truck2(self):
        g = truck_from_file("input/trucks.2.in")
        self.assertEqual(g.camion_moins_cher(9983000 - 1), 9983)
if __name__ == '__main__':
    unittest.main()