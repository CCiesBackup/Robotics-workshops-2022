from abc import ABC, abstractmethod
from typing import List, Tuple, Dict


class ShortestPathAbstract(ABC):
    @abstractmethod
    def find_shortest_path(self, start, target, paths) -> List[Tuple[Tuple[int, int], int]]:
        pass


class Vertex:
    visited = False
    path = []

    def __init__(self, location: Tuple[int, int]):
        self.location = location
        self.weight = 999999


class DijkstraAlgorithm(ShortestPathAbstract):
    vertices = {}
    __extern_paths = None

    def find_shortest_path(self, start, target, paths) -> List[Tuple[Tuple[int, int], int]]:
        none_left = False
        self.__extern_paths = paths
        last_direction = 0
        for node in paths:
            self.vertices[node] = Vertex(node)

        current_node = self.vertices[start]
        self.vertices[start].visited = True
        self.vertices[start].weight = 0

        while not none_left:
            # exit the loop if the target has been reached
            if current_node == self.vertices[target]:
                break
            # returns a dictionary with directions from the current node -> (localization, direction, weight)
            directions_dict = paths[current_node.location]
            # reference for the outgoing vertex with the smallest weight. by default it has the weight of 999999
            least_weight = (Vertex(0, 0), -1)

            for direction, edge in directions_dict:
                # edge[0] = localization of the vertex as a tuple
                if self.vertices[edge[0]].weight > (edge[2] + current_node.weight):
                    self.vertices[edge[0]].weight = (edge[2] + current_node.weight)
                    self.vertices[edge[0]].path.append(Tuple[current_node.location, direction])
                # find the unvisited vertex with the smallest weight
                if self.vertices[edge[0]].weight < least_weight[0].weight and not least_weight[0].visited:
                    least_weight = (self.vertices[edge[0]], direction)
            # jump to the next vertex if exists and not default reference
            if least_weight[1] != -1:
                current_node = least_weight[0]
                least_weight[0].visited = True
                last_direction = least_weight[1]
            else:
                # if no such vertex exists, move back to some previous vertex and continue looking over there
                current_node = self.__recul(current_node)
                if current_node is None:
                    none_left = True
        if current_node == self.vertices[target]:
            return current_node.path.append(Tuple[current_node.location, last_direction])
        else:
            return None

    def __recul(self, vertex: Vertex):
        previous_paths = vertex.path[::-1]
        if previous_paths.__len__() == 0:
            return None
        previous = previous_paths[0]
        ref_vertex = Vertex(0, 0)
        for localization, direction in previous:
            if self.vertices[localization].visited:
                continue
            if self.vertices[localization].weight <= ref_vertex:
                ref_vertex = self.vertices[localization]
                ref_vertex.path.append(Tuple[previous.location, direction])

        if ref_vertex.weight == 999999:
            return self.__recul(self.vertices[previous[0]])
        else:
            return ref_vertex
