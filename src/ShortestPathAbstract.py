from abc import ABC, abstractmethod
from typing import List, Tuple, Dict

# Strategy pattern in action
class ShortestPathAbstract(ABC):
    @abstractmethod
    def find_shortest_path(self, start, target) -> List[Tuple[Tuple[int, int], int]]:
        pass


class DijkstraAlgorithm(ShortestPathAbstract):
    # visited = bool
    # node = Tuple[int, int]
    # node_that_updated_the_value = node
    # smallest_weight = int
    # path_data = Dict[node, Tuple[visited, smallest_weight, node_that_updated_the_value]]
    path_data = {}

    def __init__(self, paths):
        # here we filter out the paths with the weight -1
        to_be_deleted = []
        paths
        for node in paths:
            inner_dict = paths[node]
            for direct in inner_dict:
                weight = inner_dict[direct][2]
                if weight == -1:
                    to_be_deleted.append((node, direct))
        # avoiding runtime error with the list
        for position in to_be_deleted:
            paths[position[0]].pop(position[1])
        self.paths = paths
        # in the beginning we don't know the way, so every node has the weight of infinity
        for node in paths:
            self.path_data[node] = [False, float('inf'), None]

    # update_estimates
    # choose next vertex
    # intern dictionary?
    # treat negative values
    def find_shortest_path(self, start, target) -> List[Tuple[Tuple[int, int], int]]:

        self.path_data[start] = (True, 0, None)
        # print(f"Calculating the shortest path from {start} to {target}")
        # not checking for the start vertex for the sake of reducing the comparison amount
        if target not in self.paths.keys():
            return None

        target_found = False
        current_vertex = start
        while not target_found:
            # It shows how the dijkstra algorithm works
            # It is just about updating the estimates and choosing the next vertex to consider
            self.__update_estimates(current_vertex, target)
            current_vertex = self.__choose_next_vertex(current_vertex)
            if current_vertex == target:
                target_found = True
            if current_vertex is None:
                break

        if not target_found:
            return None
        else:
            return self.__backtrace(target)

    def __choose_next_vertex(self, current_vertex):
        unexplored_neighbours_list = self.__get_unexplored_neighbours_list(current_vertex)
        if len(unexplored_neighbours_list) == 0:
            return self.__get_previous_vertex(current_vertex)
        else:
            next_vertex = self.__get_smallest_weight_neighbour(unexplored_neighbours_list)
            self.path_data[next_vertex][0] = True
            return next_vertex

    # for reasons of scarce robot memory, we store just the vertex that updated the next one and then
    # reconstruct the way to the start using this data
    def __backtrace(self, target_vertex):
        response = []
        input_vertex = None
        input_direction = None
        previous_vertex = (0, 0)
        vertex = target_vertex
        while previous_vertex is not None:
            # here I need to cut off the start
            previous_vertex = self.__get_previous_vertex(vertex)
            input_vertex = vertex
            # make here insert 0 and avoid reversing it in the return
            response.append((input_vertex, input_direction))
            input_direction = self.__find_previous_vertex_direction(vertex)
            vertex = self.__get_previous_vertex(vertex)

        return response[::-1]

    def __update_estimates(self, current_vertex, target):
        visited = True
        neighbours = self.__get_neighbours(current_vertex)
        for values in neighbours.values():
            current_neighbour = values[0]
            if self.path_data[current_neighbour][0] == visited:
                continue
            current_weight = self.path_data[current_neighbour][1]
            path_weight = self.__get_weight_direct_neighbour(current_vertex, current_neighbour)
            new_weight = self.path_data[current_vertex][1] + path_weight
            if new_weight < current_weight:
                self.path_data[current_neighbour][1] = new_weight
                self.path_data[current_neighbour][2] = current_vertex

    def __get_weight_direct_neighbour(self, start_node, target_node):
        weight = 0
        neighbours = self.__get_neighbours(start_node)
        for values in neighbours.values():
            if values[0] == target_node:
                weight = values[2]
        if weight == 0:
            raise AttributeError("This method can only be used with directly neighbouring nodes!")
        return weight if weight > 0 else float('inf')

    def __get_smallest_weight_neighbour(self, vertex_list):
        smallest_neighbour = None
        smallest_weight = float('inf')
        for neighbour in vertex_list:
            if self.path_data[neighbour][1] < smallest_weight:
                smallest_weight = self.path_data[neighbour][1]
                smallest_neighbour = neighbour
        return smallest_neighbour

    def __get_unexplored_neighbours_list(self, vertex):
        unexplored_neighbours_list = []
        for neighbour in self.__get_neighbour_nodes_list(vertex):
            if not self.path_data[neighbour][0]:
                unexplored_neighbours_list.append(neighbour)
        return unexplored_neighbours_list

    def __get_previous_vertex(self, vertex):
        return self.path_data[vertex][2]

    def __get_neighbours(self, node):
        return self.paths[node]

    def __get_neighbour_nodes_list(self, vertex):
        neighbours_list = []
        for values in self.__get_neighbours(vertex).values():
            neighbours_list.append(values[0])
        return neighbours_list

    def __find_previous_vertex_direction(self, vertex):
        previous_vertex = self.__get_previous_vertex(vertex)
        if previous_vertex is None:
            return None
        paths_local = self.paths[previous_vertex]
        for value in paths_local:
            if paths_local[value][0] == vertex:
                return value


class ShortestPathUsingC(ShortestPathAbstract):
    # The C programming language will most likely be about 45 times faster
    # at processing the data than Python. If the time allows it, I want definitely
    # to try writing the shortest path calculation subroutine in C and then executing it from Python
    def find_shortest_path(self, start, target, paths) -> List[Tuple[Tuple[int, int], int]]:
        pass
