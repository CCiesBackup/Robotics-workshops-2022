
# Test here all the functionalities, including the messages
# path scanning
# everything
# you can take the process payload method from the communication module
# and process your own payload in order to see
# if it works
import time

import GraphGenerator
from ExplorationManager import ExplorationManager

if __name__ == '__main__':

    explorer = ExplorationManager()
    explorer.TEST_INSERT_GRAPH_INTO_THE_PLANET(GraphGenerator.planet_cherry())
    explorer.push_scanning_results([180])
    explorer.update_current_position((8, 1))
    explorer.push_scanning_results([90, 270, 0])
    explorer.update_current_position((8, 3))
    explorer.path_will_be_explored((8, 1), 180)
    explorer.update_current_position((5, -2))
    explorer.update_current_position((5, -2))
    explorer.update_current_position((5, -2))
    explorer.update_current_position((5, -2))
    explorer.set_target((4, -1))
    print(explorer.get_directions())
    explorer.update_current_position((4, -1))
    print(explorer.get_directions())