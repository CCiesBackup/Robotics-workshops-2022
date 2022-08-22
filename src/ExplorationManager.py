import random
from typing import Tuple

from planet import Planet


def get_random(*paths):
    try:
        return random.choice(list(paths))
    except IndexError:
        return 0


class ExplorationManager:
    target = None
    target_set = False
    unknown_paths = {}
    current_position = Tuple[0, 0]


    def __init__(self):
        self.shortest_path = None
        self.planet = Planet()

    def set_target(self, current_pos: Tuple[int, int], target: Tuple[int, int]):
        self.target_set = True
        self.target = target
        self.shortest_path = self.planet.shortest_path(current_pos, target)
        if self.shortest_path is None:
            self.target_set = False

    def push_scanning_results(self, position: Tuple[int, int], *directions):
        self.current_position = position
        self.unknown_paths[position] = list(directions)

    def get_directions(self, position: Tuple[int, int]) -> int:
        if not self.target_set:
            return self.explore(position)
        else:
            for node in self.shortest_path:
                if node[0] == position:
                    return node[1]


    def explore(self, position: Tuple[int, int]):

        return 0

