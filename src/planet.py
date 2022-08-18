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
    #Das mit den nested dictionaries, das war schon so in den Templates
    #Es ist zweifelsohne nicht die beste Lösung, aber ich halte mich dabei an die Templates!
    __paths = Dict[Tuple[int, int], Dict[Direction, Tuple[Tuple[int, int], Direction, Weight]]]

    def __init__(self):
        self.__paths = {}

    def add_path(self,
                 start: Tuple[Tuple[int, int], Direction],
                 target: Tuple[Tuple[int, int], Direction],
                 weight: int):

            getter_start = self.__get_dict_paths(start[0])
            getter_target = self.__get_dict_paths(target[0])
            start_value_dictionary = getter_start[0]
            target_value_dictionary = getter_target[0]

            #Tutor: Make sure that the initialized dictionaries are still referenced to __paths
            start_value_dictionary[start[1]] = Tuple[target[0], target[1], weight]
            target_value_dictionary[target[1]] = Tuple[start[0], start[1], weight]
            if getter_start[1]:
                self.__reference_dicts(start[0], start_value_dictionary)
            if getter_target[1]:
                self.__reference_dicts(target[0], target_value_dictionary)



    def __reference_dicts(self, value: Tuple[int, int],
                          dictionary: Dict[Direction, Tuple[Tuple[int, int], Direction, Weight]]):
        self.__paths[value] = dictionary

    def __get_dict_paths(self, value: Tuple[int, int]) -> \
        Dict[Direction, Tuple[Tuple[int, int], Direction, Weight]]:
            if value in self.__paths:
                return self.__paths[value], False
            else:
                return {}, True


    def get_paths(self) -> \
            Dict[Tuple[int, int],
                 Dict[Direction,
                      Tuple[Tuple[int, int], Direction, Weight]
                 ]
            ]:

        return self.__paths



    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Optional[List[Tuple[Tuple[int, int], Direction]]]:



        pass
