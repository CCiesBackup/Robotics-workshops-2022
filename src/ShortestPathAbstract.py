from abc import ABC, abstractmethod
from typing import List, Tuple, Dict


class ShortestPathAbstract(ABC):
    @abstractmethod
    def find_shortest_path(self, start, target, paths) -> List[Tuple[Tuple[int, int], int]]:
        pass


class DijkstraAlgorithm(ShortestPathAbstract):
    list = List[Tuple[Tuple[1, 2], 3]]

    def find_shortest_path(self, start, target, paths) -> List[Tuple[Tuple[int, int], int]]:




        return list
