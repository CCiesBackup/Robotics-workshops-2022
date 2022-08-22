import random
from typing import Tuple

import planet


def get_random(*paths):
    try:
        return random.choice(list(paths))
    except IndexError:
        return 0


class ExplorationManager:
    path_select_set = False
    path_select_dir = 0
    target = None
    target_set = False
    unknown_paths = {}
    current_position = (0, 0)
    current_orientation = 0

    def __init__(self):
        self.shortest_path = None
        self.planet = planet.Planet()

    def set_target(self, target: Tuple[int, int]):
        self.target_set = True
        self.target = target
        self.shortest_path = self.planet.shortest_path(self.current_position, target)
        if self.shortest_path is None:
            self.target_set = False

    def push_scanning_results(self, position: Tuple[int, int], *directions):
        self.current_position = position
        self.unknown_paths[position] = list(directions)

    def get_directions(self, position: Tuple[int, int]) -> int:
        if self.path_select_set:
            self.path_select_set = False
            return self.path_select_dir

        if not self.target_set:
            return self.explore(position)
        else:
            for node in self.shortest_path:
                if node[0] == position:
                    return node[1]

    def set_path_select(self, direction: int):
        self.path_select_set = True
        self.path_select_dir = direction

    def rebuke(self):
        pass

    def add_path_intern(self,
                        start: Tuple[Tuple[int, int], int],
                        target: Tuple[Tuple[int, int], int],
                        weight: int):
        self.planet.add_path(start, target, weight)

    def explore(self, position: Tuple[int, int]):

        return 0
