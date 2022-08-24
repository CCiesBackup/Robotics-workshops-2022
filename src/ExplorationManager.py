import random
from typing import Tuple

import planet

# Designed for testing the odometry module
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
    unknown_paths_temp = []
    current_position = (0, 0)
    current_orientation = 0
    path_changed = False

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
        #self.shortest_path = self.planet.shortest_path(self.current_position, target)
        #if self.shortest_path is None:
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
        self.unknown_paths[current_position] = self.unknown_paths_temp

    def update_current_orientation(self, current_orientation: int):
        self.current_orientation = current_orientation

    def update_current_data(self, current_position, current_orientation):
        self.update_current_position(current_position)
        self.update_current_orientation(current_orientation)

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
        return self.last_direction


    def set_path_select(self, direction: int):
        self.path_select_set = True
        self.path_select_dir = direction

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
        local_list = self.unknown_paths[position]
        if len(local_list) > 0:
            direction = random.choice(local_list)

            return direction
        else:
            further_direction = self.explore_further(position)
            return further_direction if further_direction is not None else self.exploration_complete()

    def exploration_complete(self):
        # to be implemented: we know that the exploration has been completed
        return 0

    def explore_further(self, position):
        # here we get the closest neighbour that has some unexplored paths
        # and return the direction to this neighbour.
        # to be implemented recursively
        # some data structure keeping the checked nodes should also be implemented
        # return none if the neighbour doesn't have any a) unexplored paths or
        # b) it doesn't have any unvisited neighbours

        return 0

    def get_reverse_direction(self, direction):
        return (direction + 180) % 360
