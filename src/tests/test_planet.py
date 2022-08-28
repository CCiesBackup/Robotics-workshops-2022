#!/usr/bin/env python3

import unittest

import GraphGenerator
import ShortestPathAbstract
from planet import Direction, Planet


class TestRoboLabPlanet(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        MODEL YOUR TEST PLANET HERE (if you'd like):

        """
        # Initialize your data structure here
        self.planet = Planet()
        # self.planet.add_path(...)

    def test_integrity(self):
        paths = self.planet.get_paths()
        paths.clear()

        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 1), Direction.WEST), ((0, 0), Direction.WEST), 1)

        # Yeah sorry, I don't like this Direction enum
        test_structure = {
            (0, 0): {Direction.NORTH: ((0, 1), Direction.SOUTH, 1), Direction.WEST: ((0, 1), Direction.WEST, 1)},
            (0, 1): {Direction.WEST: ((0, 0), Direction.WEST, 1), Direction.SOUTH: ((0, 0), Direction.NORTH, 1)}
        }
        self.assertEqual(test_structure, self.planet.get_paths(), "Adding paths to the planet doesn't work correctly!")

    def test_empty_planet(self):
        paths = self.planet.get_paths()
        # Here we make sure that in the structure there are no paths added anywhere else
        # For example, that it doesn't take the paths from the test above
        paths.clear()
        # This planet is really empty!
        self.assertEqual(self.planet.get_paths(), {}, "An empty planet should be empty!")


    def test_target(self):
        # Test that the shortest path algorithm works!
        algorithm = ShortestPathAbstract.DijkstraAlgorithm(GraphGenerator.planet_cherry())
        # the shortest path between the nodes (8, -1) and (4, -1) on planet cherry
        shortest_path_test = [((8, -1), 270), ((6, -2), 270), ((5, -2), 270), ((4, -1), None)]
        self.assertEqual(shortest_path_test, algorithm.find_shortest_path((8, -1), (4, -1)),
                         "The calculated shortest path wasn't correct!")



    def test_target_not_reachable(self):
        algorithm = ShortestPathAbstract.DijkstraAlgorithm(GraphGenerator.planet_cherry())
        shortest_path_fail = algorithm.find_shortest_path((8, -1), (19, 0))
        self.assertIsNone(shortest_path_fail, "The SP algorithm should return None if the shortest path doesn't exist!")

    def test_same_length(self):
        algorithm = ShortestPathAbstract.DijkstraAlgorithm(GraphGenerator.planet_cherry())
        shortest_path_length = 3
        shortest_path_calculated = algorithm.find_shortest_path((7, 0), (7, 2))
        self.assertIsNotNone(shortest_path_calculated, "The algorithm failed the same length test!")
        self.assertEqual(shortest_path_length, len(shortest_path_calculated),
                         "The algorithm fails if two parallel paths are equal!")


    def test_target_with_loop(self):
        algorithm = ShortestPathAbstract.DijkstraAlgorithm(GraphGenerator.planet_cherry())
        shortest_path_one_point = algorithm.find_shortest_path((19, 0), (19, -1))
        test_structure = [((19, 0), 0), ((19, -1), None)]
        self.assertEqual(test_structure, shortest_path_one_point, "It gets stuck if there is only one point left!")


    def test_target_not_reachable_with_loop(self):
        algorithm = ShortestPathAbstract.DijkstraAlgorithm(GraphGenerator.planet_cherry())
        path = algorithm.find_shortest_path((6, 1), (7, 1))
        self.assertIsNone(path, "Unreachable target - should be None and it should terminate (:")



if __name__ == "__main__":
    unittest.main()
