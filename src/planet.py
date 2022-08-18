#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
from enum import IntEnum, unique
from typing import Optional, List, Tuple, Dict


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
        self.__paths = {}

    def add_path(self,
                 start: Tuple[Tuple[int, int], Direction],
                 target: Tuple[Tuple[int, int], Direction],
                 weight: int):
        start_value_dictionary = self.__paths[start[0]]
        start_value_dictionary[start[1]] = Tuple[target[0], target[1], weight]






    def get_paths(self) -> \
            Dict[Tuple[int, int],
                 Dict[Direction,
                      Tuple[Tuple[int, int], Direction, Weight]
                 ]
            ]:

        return self.__paths



    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Optional[List[Tuple[Tuple[int, int], Direction]]]:



        pass
