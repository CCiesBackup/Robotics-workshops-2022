import random
from typing import Tuple

import ShortestPathAbstract
import planet
from CommunicationFactory import CommunicationFactory

# return random path from the paths received by scanning
# meant to facilitate testing odometry when I'm working on the exploration module
def get_random(*paths):
    try:
        return random.choice(list(paths))
    except IndexError:
        return 0

# The class encapsulating the exploration logic. planet.py serves as a model in the sense of MVC
# Though admittedly, we haven't been sticking to this concept tightly
class ExplorationManager:
    # parameters for handling path select
    path_select_set = False
    path_select_dir = 0
    # use this one if no path select message has been received
    last_direction = None
    target = None
    target_set = False
    # the data structures containing the unknown paths
    unknown_paths = {}
    # unknown paths are only updated with the values confirmed by the server
    # hence "unknown_paths_temp" where the scanning results are temporarily stored
    unknown_paths_temp = []
    # parameters containing the data regarding current position and orientation of the robot
    current_position = (0, 0)
    current_orientation = 0
    # For path unveiled: if true, we have to recalculate the shortest path
    # because it is possible that a path that we want to use has just been blocked
    path_changed = False
    directions_for_exploration_calculated = False
    # directions for exploration
    # variables for storing data, so that we don't have to calculate the same path
    # at every node
    exploration_directions = []
    calculated_directions_to_next_neighbour_with_unknown_nodes = False
    path_to_the_next_neighbour_with_unexplored_paths = []
    # this variable is meant to stop the recursion if a better way has already been found
    search_path_found_weight = float('inf')

    def __init__(self):
        self.visited_vertices = set([])
        self.shortest_path = None
        self.planet = planet.Planet()

    def did_I_visit_this_vertex(self, vertex):
        return vertex in self.visited_vertices

    # I have written it on Nico's laptop
    def update_unknown_paths(self):
        print(f"Before the update: temp: {self.unknown_paths_temp}, norm: {self.unknown_paths}")
        if len(self.unknown_paths_temp) == 0:
            # print("length is 0. return from update_unknown_paths")
            return
        position = self.current_position
        # try catch block is here because I do not know if the lookup of a key returns None or an exception
        # if the key is not disponible
        try:
            unknown_paths_content = self.unknown_paths[position]
            if unknown_paths_content is None:
                unknown_paths_content = []
            # avoiding NullPointerException and such
            # type Exception because I'm not really well-versed in Python and its inbuilt exception types
        except Exception:
            unknown_paths_content = []
        inner_path_dict = self.planet.get_paths()[self.current_position]
        for direction in self.unknown_paths_temp:
            if direction not in inner_path_dict.keys():
                unknown_paths_content.append(direction)
        # If we get a path with pathUnveiled, we know that it is there
        # but we don't know if it doesn't have any unexplored paths at the second end
        for direction in self.known_but_not_visited(self.current_position):
            unknown_paths_content.append(direction)
        if len(unknown_paths_content) > 0:
            self.unknown_paths[position] = unknown_paths_content
        self.unknown_paths_temp.clear()
        print(f"After the update: {self.unknown_paths_temp}, norm: {self.unknown_paths}")

    # the method used for setting a target, it is also called by the communication class
    # after receiving a target message from the server

    def known_but_not_visited(self, position):
        known_but_not_visited_list = []
        inner_dict = self.planet.get_paths()[position]
        for direction in inner_dict:
            if inner_dict[direction][0] not in self.visited_vertices and inner_dict[direction][2] != -1:
                known_but_not_visited_list.append(direction)
        return known_but_not_visited_list

    def set_target(self, target: Tuple[int, int]):
        if target == self.target:
            return
        if target == self.current_position:
            self.target_reached()
            self.set_path_select(128)
            return
        # print(f"New target set! : {target}")
        self.target_set = True
        self.target = target
        self.shortest_path = self.planet.shortest_path(self.current_position, target)
        # If no way has been found, we will just continue the exploration
        if self.shortest_path is None:
            self.target_set = False
        self.path_changed = False

    # this method is used to provide this class with the data regarding the unknown paths that
    # have been discovered
    def push_scanning_results(self, directions, ready=False):
        # the values will be stored in a temporary variable, waiting for position confirmation from
        # the server
        self.unknown_paths_temp = directions
        # given that we call the ready function before scanning, the update from there wouldn't work
        if ready:
            self.update_unknown_paths()

    def update_current_position(self, current_position: Tuple[int, int]):
        self.current_position = current_position
        # Quick fix: It will be useful to track visited vertices for optimization purposes
        # We need it because otherwise we wouldn't be able to differentiate the paths discovered by
        # the robot from the paths received from the server with the pathUnveiled message
        self.visited_vertices.add(current_position)
        # The scanned paths will be added to the dict only after validation of the data by the server
        # That is, after the path message arrived.
        # So, the right way of doing it is push_scanning_results -> send_path_message
        # and the path message reception will call this function and the one below
        # moving the unknown paths from the temp list into the main data structure

        self.update_unknown_paths()

    # a simple setter for the current orientation
    def update_current_orientation(self, current_orientation: int):
        self.current_orientation = current_orientation

    # a method combining the two other data setters
    # It's used to be able to actually track or execute some code alongside updating internal data of
    # the class
    def update_current_data(self, current_position, current_orientation):
        self.search_path_found_weight = float('inf')
        self.update_current_position(current_position)
        self.update_current_orientation(current_orientation)

    # A simple method used to unify two lists into one without any repetitions nor any data losses
    def list_union_no_repetitions(self, list1, list2):
        final_list = list(set().union(list1, list2))
        return final_list

    # The method capsuling the logic of differentiating between the corresponding cases and
    # returning a single direction. It also manages the path select by server logic
    def __get_directions_intern(self):
        if not self.path_select_set:
            position = self.current_position

            if not self.target_set:
                # Here we get a direction from the exploration part
                return self.explore(position)
            else:
                # Here we've got code for handling target-oriented navigation
                # If path_unveiled disclosed some new information, recalculate the shortest path
                # (a part of the previous shortest path could be blocked or there could be a better
                # way available)
                if self.path_changed:
                    self.set_target(self.target)
                # This means that we've reached the target
                if position == self.target:
                    return self.target_reached()
                # If, for any reason, the calculated shortest path is set to None
                # and it hasn't been handled so far, then set target_set to False
                # and get the direction this way (either path select or exploration)
                if self.shortest_path is None:
                    self.target_set = False
                    return self.__get_directions_intern()
                # Here we extract the direction from the shortest path list
                # I prefer this approach to simply removing nodes from the data structure and taking
                # the first one, for the reasons of security
                for node in self.shortest_path:
                    # None at the end will never be returned because of position == self.target
                    if node[0] == position:
                        return node[1]
                # If we got here, it means a logistical mistake, the robot physically lost the way
                # or didn't take the turn properly
                # in this unlikely case, we will just recalculate the shortest way and go from there on
                still_here = True
                if still_here:
                    self.set_target(self.target)
                    return self.__get_directions_intern()
        # Here, we return the path select direction received from the server
        # and set the boolean to false, because this direction would be no more valid
        else:
            self.path_select_set = False
            return self.path_select_dir

    # this method will be called from the outside to get the next direction to go to
    # it will be called twice, second time to check if there's been a path select message from the
    # server
    # so, the first calculation will be called with path_select_check = False,
    # the second one with path_select_check = True
    # On second thought, I should just encapsulate the entire logic in here,
    # but I didn't really have much time to think about it, since
    # I was also working on the communication part and attending to my other personal obligations
    def get_directions(self, path_select_check=False) -> int:
        # if no path select message has been received,
        # just go on with the previously calculated direction
        if path_select_check and not self.path_select_set:
            # path will be explored removes the path to be explored from the unknown paths list
            self.path_will_be_explored(self.current_position, self.last_direction)
            return self.last_direction
        # if we come here with path select check, the
        # path select message has been received
        # in such case, this method returns the direction from the path select payload
        # This method will return the path select from the server at second attempt
        # if such a message has been received at all
        self.last_direction = self.__get_directions_intern()
        # the path will only be removed from the unknown paths list if the exploration has been confirmed
        # (we are sure that the path select won't select any other direction instead)
        if path_select_check:
            self.path_will_be_explored(self.current_position, self.last_direction)
        return self.last_direction

    # a simple method used to communicate that the target set has been reached
    def target_reached(self):
        # I really hope that the singleton works as expected
        com = CommunicationFactory.get_initialized_instance()
        com.send_target_reached("No comment.")
        # 128 is our stop code, we use it at the main function in the while loop
        return 128

    # method removing paths from the unknown paths list
    def path_will_be_explored(self, position, direction):
        # print(self.unknown_paths)
        unknown_directions_list = self.unknown_paths[position]
        if direction in unknown_directions_list:
            unknown_directions_list.remove(direction)
        if len(self.unknown_paths[position]) == 0:
            self.unknown_paths.pop(position)

    # a simple method receiving the path select payload from the server, through the communication class
    def set_path_select(self, direction: int):
        self.calculated_directions_to_next_neighbour_with_unknown_nodes = False
        self.path_select_set = True
        self.path_select_dir = direction

    def paths_changed(self):
        # it signals the need to relaunch the shortest way algorithm
        # if a pathUnveiled message has been received
        self.path_changed = True
        self.calculated_directions_to_next_neighbour_with_unknown_nodes = False

    # if we believe that we've completed the exploration, but it apparently hasn't been the case
    def rebuke(self):
        pass

    # a method to add some paths to the underlying data structure
    def add_path_intern(self,
                        start: Tuple[Tuple[int, int], int],
                        target: Tuple[Tuple[int, int], int],
                        weight: int):
        self.planet.add_path(start, target, weight)

    # it returns a direction for exploration
    def explore(self, position: Tuple[int, int]):
        if len(self.unknown_paths) == 0:
            print(f"unknown paths = {self.unknown_paths}")
            print(f"exploration complete! paths = {self.planet.get_paths()}")
            return self.exploration_complete()
        if not self.calculated_directions_to_next_neighbour_with_unknown_nodes:
            if self.has_unexplored_paths(position):
                return self.unknown_paths[position][0]
            else:
                directions = self.get_closest_neighbour_with_unknown_paths(position)
                return directions
        else:
            direction = self.path_to_the_next_neighbour_with_unexplored_paths[0]
            self.path_to_the_next_neighbour_with_unexplored_paths.remove(direction)
            if len(self.path_to_the_next_neighbour_with_unexplored_paths) == 0:
                self.calculated_directions_to_next_neighbour_with_unknown_nodes = False
            return direction

    def exploration_complete(self):
        com = CommunicationFactory.get_initialized_instance()
        com.send_exploration_completed("No text. Sorry :(")
        # 128 is our stop code
        return 128

    def get_neighbours(self, position):
        neighbours = []
        neighbours_dict = self.planet.get_paths()[position]
        for direction in neighbours_dict:
            neighbours.append((direction, neighbours_dict[direction][0]))
        return neighbours

    def has_unexplored_paths(self, position):
        if position in self.unknown_paths.keys() and len(self.unknown_paths[position]) != 0:
            return True
        else:
            return False

    def get_reverse_direction(self, direction):
        return (direction + 180) % 360

    def get_closest_neighbour_with_unknown_paths(self, position):
        recursion_results = {}
        direction_dict = self.planet.get_paths()[position]
        # at first, we use this function because we don't want to use costly recursion if the
        # sought neighbour is directly next to the current position
        for direction in direction_dict:
            neigh_position = direction_dict[direction][0]
            if self.has_unexplored_paths(neigh_position):
                return direction
        ###########
        # If we got here: No direct neighbour has unexplored paths
        for direction in direction_dict:
            neigh_position = direction_dict[direction][0]
            neigh_weight = direction_dict[direction][2]
            recursion_results[direction] = self.explor_target_search_recursive(
                neigh_position, neigh_weight, []
            )

        smallest_weight_direction = (999999, [])
        for direction in recursion_results:
            new_weight = recursion_results[direction][0]
            if new_weight < smallest_weight_direction[0]:
                smallest_weight_direction = (new_weight, direction)

        if smallest_weight_direction[0] < 99999:
            desired_direction = smallest_weight_direction[1]
            self.path_to_the_next_neighbour_with_unexplored_paths = \
                recursion_results[desired_direction][1]
            self.calculated_directions_to_next_neighbour_with_unknown_nodes = True
            return desired_direction
        else:
            some_target_node = random.choice(list(self.unknown_paths.keys()))
            self.calculated_directions_to_next_neighbour_with_unknown_nodes = True
            shortest_path = self.planet.shortest_path(position, some_target_node)
            return self.process_shortest_path_template_format(shortest_path)

    def explor_target_search_recursive(self, position, weight, direction_history: list):
        # Avoiding stack overflow error
        # The function call amount grows exponentially
        # and at length 5 we are at 3^5 = 243 function calls
        # I believe it's the maximum that our brick can handle
        # if the target hasn't been found, we will use another method,
        # efficient only at high distances

        # The recursion will not continue if we already know a more efficient path
        if len(direction_history) > 5 or weight > self.search_path_found_weight:
            return 999999, direction_history
        if self.has_unexplored_paths(position):
            self.search_path_found_weight = weight
            return weight, direction_history
        else:
            investigated_node_values = []
            directions_dict = self.planet.get_paths()[position]
            for direction in directions_dict:
                neigh_position = directions_dict[direction][0]
                neigh_weight = weight + directions_dict[direction][2]
                # lists in python are mutable - hence the copy
                historial = direction_history.copy()
                historial.append(direction)
                investigated_node_values.append(
                    self.explor_target_search_recursive(neigh_position, neigh_weight, historial))

            return self.tuple_min(investigated_node_values)

    def tuple_min(self, tuple_list):
        smallest_vertex = (999999, [])
        for tuple_x in tuple_list:
            if tuple_x[0] < smallest_vertex[0]:
                smallest_vertex = tuple_x
        return smallest_vertex

    # Calculating the shortest path from (6, 1) to (8, -1)
    # [((6, 1), 270), ((6, 3), 270), ((5, 3), 270), ((4, -1), 0),
    # ((5, -2), 90), ((6, -2), 90), ((8, -1), None)]
    def process_shortest_path_template_format(self, shortest_path):
        formatted_list = [node[1] for node in shortest_path if node[1] is not None]
        first_direction = formatted_list[0]
        formatted_list.remove(first_direction)
        self.path_to_the_next_neighbour_with_unexplored_paths = formatted_list
        return first_direction

    # for testing purposes only!
    # I could use unit tests instead, but it's too much typing with graphs
    def TEST_INSERT_GRAPH_INTO_THE_PLANET(self, graph):
        self.planet.TESTING_set_paths_from_outside(graph)

    def TEST_PRINT_INNER_PATHS(self):
        self.planet.print_paths()

