import GraphGenerator
import ShortestPathAbstract
import math


def test_dijkstra(start, target, paths):
    algorithm = ShortestPathAbstract.DijkstraAlgorithm(paths)

    shortest_path = algorithm.find_shortest_path(start, target)
    return shortest_path


if __name__ == '__main__':
    print(test_dijkstra((8, -1), (9, 2), GraphGenerator.planet_cherry()))
