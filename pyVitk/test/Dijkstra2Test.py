import unittest
from pyVitk.Dijkstra2 import Graph, dijkstra, shortest_path

class DijkstraTestCase(unittest.TestCase):
    def setUp(self):
        None

    def tearDown(self):
        self.edges = None

    def test_shortest_path(self):
        # To run an example
        G = Graph()
        G.add_vertex('a')
        G.add_vertex('b')
        G.add_vertex('c')
        G.add_vertex('d')
        G.add_vertex('e')

        G.add_edge('a', 'b', 2)
        G.add_edge('a', 'c', 8)
        G.add_edge('a', 'd', 5)
        G.add_edge('b', 'c', 1)
        G.add_edge('c', 'e', 3)
        G.add_edge('d', 'e', 4)

        print(G)

        print(dijkstra(G, 'a'))

        print('shortest path with min: {}'.format(shortest_path(G, 'a', 'e')))

        print('shortest path with max: {}'.format(shortest_path(G, 'a', 'e', find_min=False)))
