import unittest
import pyVitk.Dijkstra as Dijkstra

class DijkstraTestCase(unittest.TestCase):
    def setUp(self):
        None

    def tearDown(self):
        self.edges = None

    def test_shortest_path(self):
        self.edges = {}
        for v in range(6):
            self.edges[v] = []
        self.edges[5].append(4)
        self.edges[4].append(3)
        self.edges[4].append(2)
        self.edges[3].append(2)
        self.edges[3].append(1)
        self.edges[2].append(1)
        self.edges[1].append(0)

        d = Dijkstra.Dijkstra(self.edges)
        print('edges before sort: {}'.format(d))

        paths = d.shortestPaths()
        print('Shortest paths: {}'.format(paths))

    def test_shortest_path_2(self):
        self.edges = {}
        for v in range(3):
            self.edges[v] = []
        self.edges[2].append(1)
        self.edges[2].append(0)
        self.edges[1].append(0)

        d = Dijkstra.Dijkstra(self.edges)
        print('edges before sort: {}'.format(d))

        paths = d.shortestPaths()
        print('Shortest paths: {}'.format(paths))