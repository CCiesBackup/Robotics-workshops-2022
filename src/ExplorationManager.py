import random
from typing import Tuple

import planet

# Designed for testing the odometry module
from CommunicationFactory import CommunicationFactory


def get_random(*paths):
    try:
        return random.choice(list(paths))
    except IndexError:
        return 0


class ExplorationManager:
    path_select_set = False
    path_select_dir = 0
    last_direction = None
    target = None
    target_set = False
    unknown_paths = {}
    # unknown paths are only updated with the values confirmed by the server
    # hence "unknown_paths_temp" where the scanning results are temporarily stored
    unknown_paths_temp = []
    current_position = (0, 0)
    current_orientation = 0
    path_changed = False
    directions_for_exploration_calculated = False
    exploration_directions = []

    def __init__(self):
        self.shortest_path = None
        self.planet = planet.Planet()

    def set_target(self, target: Tuple[int, int]):
        if target == self.target and not self.path_changed:
            return
        print(f"New target set! : {target}")
        self.target_set = True
        self.target = target
        print("Calculating shortest path to the target... ")
        # self.shortest_path = self.planet.shortest_path(self.current_position, target)
        # if self.shortest_path is None:
        #    self.target_set = False
        self.path_changed = False

    def push_scanning_results(self, *directions):
        for direction in directions:
            self.unknown_paths_temp.append(direction)

    def update_current_position(self, current_position: Tuple[int, int]):
        self.current_position = current_position
        # The scanned paths will be added to the dict only after validation of the data by the server
        # That is, after the path message arrived.
        # So, the right way of doing it is push_scanning_results -> send_path_message

        # making sure that no values are lost/overwritten
        # because I can never know who uses this function etc.
        # just making sure (:
        try:
            unknown_paths_content = self.unknown_paths[current_position]
            # avoiding NullPointerException and such
            # type Exception because I'm not really well-versed in Python and its inbuilt exception types
        except Exception:
            unknown_paths_content = []

        self.unknown_paths[current_position] = \
            self.list_union_no_repetitions(self.unknown_paths_temp, unknown_paths_content)
        self.unknown_paths_temp.clear()

    def update_current_orientation(self, current_orientation: int):
        self.current_orientation = current_orientation

    def update_current_data(self, current_position, current_orientation):
        self.update_current_position(current_position)
        self.update_current_orientation(current_orientation)

    def list_union_no_repetitions(self, list1, list2):
        final_list = list(set().union(list1, list2))
        return final_list

    def __get_directions_intern(self):
        position = self.current_position

        if not self.target_set:
            return self.explore(position)
        else:
            for node in self.shortest_path:
                if node[0] == position:
                    return node[1]

    def get_directions(self) -> int:
        self.last_direction = self.__get_directions_intern()
        self.path_will_be_explored(self.current_position, self.last_direction)
        return self.last_direction

    def path_will_be_explored(self, position, direction):
        unknown_directions_list = self.unknown_paths[position]
        if direction in unknown_directions_list:
            unknown_directions_list.remove(direction)


    def set_path_select(self, direction: int):
        self.path_select_set = True
        self.path_select_dir = direction
        # If the server selects some other way than the one selected by the algorithm
        self.unknown_paths[self.current_position].append(self.last_direction)
        self.path_will_be_explored(self.current_position, direction)

    def paths_changed(self):
        # it signals the need to relaunch the shortest way algorithm
        self.path_changed = True

    def rebuke(self):
        for i in range(3):
            print("Sorry, we have to work on the sensors and scanning paths again")
            print("ERROR! " * 5)

    def add_path_intern(self,
                        start: Tuple[Tuple[int, int], int],
                        target: Tuple[Tuple[int, int], int],
                        weight: int):
        self.planet.add_path(start, target, weight)

    # Sort of a depth-first search
    def explore(self, position: Tuple[int, int]):
        
        if len(self.unknown_paths) == 0:
            return self.exploration_complete()
        
        if self.has_unexplored_paths(position):
            return random.choice(self.unknown_paths[position])
        else:
            directions = self.get_closest_neighbour_with_unknown_paths(position)
            

    def exploration_complete(self):
        com = CommunicationFactory.get_initialized_instance()
        com.send_exploration_completed("No text. Sorry :(")
        # 128 is our stop code
        return 128

    def get_neighbours(self, position):
        neighbours = []
        neighbours_dict = self.planet.get_paths()[position]
        for direction, target in neighbours_dict:
            neighbours.append((direction, target))
        return neighbours

    def has_unexplored_paths(self, position):
        if position[1] in self.unknown_paths.keys():
            return True
        else:
            return False

    def get_reverse_direction(self, direction):
        return (direction + 180) % 360

    def get_closest_neighbour_with_unknown_paths(self, position):
        neighbours = self.get_neighbours(position)
        eligible_neighbours = []
        for neighbour in neighbours:
            if self.has_unexplored_paths(neighbour):
                eligible_neighbours.append(neighbour)
