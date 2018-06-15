# coding=UTF-8

import unittest
import logging
from pyVitk.Dijkstra2 import Graph, dijkstra, shortest_path

# setup the logger
logger = logging.getLogger(__name__)
if not len(logger.handlers):
    # file handler
    hdlr = logging.FileHandler('unittest.log', encoding='utf8')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.DEBUG)

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

        logger.debug(G)

        logger.debug(dijkstra(G, 'a'))

        logger.debug('shortest path with min: {}'.format(shortest_path(G, 'a', 'e')))

        logger.debug('shortest path with max: {}'.format(shortest_path(G, 'a', 'e', find_min=False)))

    def test_shortest_path_2(self):
        s = "Wikipedia tiếng Việt là phiên bản tiếng Việt của dự án Wikipedia"
        logger.debug("Shortestpath of {}".format(s))
        G = Graph()
        G.add_vertex('<s>')
        G.add_vertex('</s>')
        G.add_vertex('Wikipedia')
        G.add_vertex('tiếng')
        G.add_vertex('Việt')
        G.add_vertex('là')
        G.add_vertex('phiên')
        G.add_vertex('bản')
        G.add_vertex('phiên bản')
        G.add_vertex('của')
        G.add_vertex('dự')
        G.add_vertex('án')
        G.add_vertex('dự án')

        G.add_edge('<s>', 'Wikipedia', 1)
        G.add_edge('Wikipedia', 'tiếng', 1)
        G.add_edge('tiếng', 'Việt', 1)
        G.add_edge('Việt', 'là', 1)
        G.add_edge('là', 'phiên', 1)
        G.add_edge('phiên', 'bản', 1)
        G.add_edge('là', 'phiên bản', 1)
        G.add_edge('bản', 'của', 1)
        G.add_edge('phiên bản', 'của', 1)
        G.add_edge('của', 'dự', 1)
        G.add_edge('dự', 'án', 1)
        G.add_edge('án', 'Wikipedia', 1)
        G.add_edge('Wikipedia', '</s>', 1)

        logger.debug(G)

        logger.debug(dijkstra(G, '<s>'))

        logger.debug('shortest path with min: {}'.format(shortest_path(G, '<s>', '</s>')))

        logger.debug('shortest path with max: {}'.format(shortest_path(G, '<s>', '</s>', find_min=False)))