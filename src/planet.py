#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
from enum import IntEnum, unique
from typing import Optional, List, Tuple, Dict

import ShortestPathAbstract


@unique
class Direction(IntEnum):
    """ Directions in shortcut """
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270


Weight = int

"""
Weight of a given path (received from the server)

Value:  -1 if blocked path
        >0 for all other paths
        never 0
"""


class Planet:
    __paths = Dict[Tuple[int, int], Dict[Direction, Tuple[Tuple[int, int], Direction, Weight]]]

    def __init__(self):
        self.shortest_path_algorithm = None
        self.__paths = {}

    def add_path(self,
                 start: Tuple[Tuple[int, int], Direction],
                 target: Tuple[Tuple[int, int], Direction],
                 weight: int):
        # print(f"Added path from: {start[0]}, exit direction:{start[1]}")
        # print(f"Path leads to: {target[0]}, entrance direction:{target[1]}")
        getter_start = self.__get_dict_paths(start[0])
        getter_target = self.__get_dict_paths(target[0])
        start_value_dictionary = getter_start[0]
        target_value_dictionary = getter_target[0]

        # here we don't have to bind it again because it's a call by reference
        start_value_dictionary[start[1]] = (target[0], target[1], weight)
        target_value_dictionary[target[1]] = (start[0], start[1], weight)
        # but if it's been empty before, we have to reference it with the new dictionary
        if getter_start[1]:
            self.__reference_dicts(start[0], start_value_dictionary)
        if getter_target[1]:
            self.__reference_dicts(target[0], target_value_dictionary)

    def __reference_dicts(self, value: Tuple[int, int],
                          dictionary: Dict[Direction, Tuple[Tuple[int, int], Direction, Weight]]):
        self.__paths[value] = dictionary
    # the true/false value tells us if we have created a new dictionary variable ({}) or not,
    # false means that we use an existing one
    # its important for referencing
    def __get_dict_paths(self, key: Tuple[int, int]):
        if key in self.__paths:
            return self.__paths[key], False
        else:
            return {}, True

    # a getter for paths
    def get_paths(self) -> \
            Dict[Tuple[int, int],
                 Dict[Direction,
                      Tuple[Tuple[int, int], Direction, Weight]
                 ]
            ]:

        return self.__paths

    def print_paths(self):
        print(self.__paths)


    # allows to change the used algorithm dynamically during execution of the program
    def set_shortest_path_algorithm(self, algorithm: ShortestPathAbstract):
        self.shortest_path_algorithm = algorithm

    # the dijkstra returns the shortest path in the following format:
    # Calculating the shortest path from (6, 1) to (8, -1)
    # [((6, 1), 270), ((6, 3), 270), ((5, 3), 270), ((4, -1), 0),
    # ((5, -2), 90), ((6, -2), 90), ((8, -1), None)]

    # Couldn't return an optional:
    # TypeError: typing.Optional requires a single type. Got a list instead.
    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]):
        # we hardcode it here since we will not be using any other shortest path implementation
        # I want to make sure that nobody forgets it
        # I will leave the other methods like the algorithm setter just in case
        self.shortest_path_algorithm = ShortestPathAbstract.DijkstraAlgorithm(self.__paths)
        shortest_path = \
            self.shortest_path_algorithm.find_shortest_path(start, target)
        return shortest_path

    # this method will only be used for testing
    # so that we don't have to tip in all the paths manually
    def TESTING_set_paths_from_outside(self, graph):
        # print("the graph has been set!")
        self.__paths = graph