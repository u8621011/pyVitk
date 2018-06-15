# coding=UTF-8

from typing import Dict, List
from queue import PriorityQueue
import logging

logger = logging.getLogger(__name__)

class Dijkstra(object):
    """
    Implementation of the Dijkstra algorithm using a priority queue. This
    utility helps find all shortest paths in a phrase graph in a segmentation.
    """
    def __init__(self, edges: Dict):
        self.edges = edges
        self.n = len(edges)
        self.distance = [float('inf')] * self.n
        self.previous = {}
        
        self.distance[self.n - 1] = 0
        self.previous[self.n - 1] = {}  # last node no previous

        pqueue = PriorityQueue(self.n)
        pqueue.put((self.distance[self.n-1], self.n - 1))
        while not pqueue.empty():
            v = pqueue.get_nowait()
            nodes = self.edges[v[1]]
            for u in nodes: # nodes are all possible next node, u is current processing next node
                d = self.distance[v[1]] + 1
                if d < self.distance[u]:
                    self.distance[u] = d

                    # we use dictionary to collect multi path of same weight and prevent duplicat pevious node added
                    # duplication means:
                    #   possible path1: 5->4->2->1
                    #   possible path2: 5->3->2->1
                    # in this case 2 will be enumerate 2 times.
                    self.previous[u] = {
                        v[1]: d
                    }
                    pqueue.put((self.distance[u], u))
                elif d == self.distance[u]: # same wight
                    self.previous[u][v[1]] = d

        logger.debug("previous nodes afer Dijkstra construct: {}".format(str(self.previous)))

    def shortestPaths(self) -> list:
        """
        Finds all shortest paths on this graph, between vertex <code>0</code>
        and vertex <code>n-1</code>.
        :return: all shortest paths.
        """
        new_path = [0] # all path start at first item
        processing_path = []
        all_shortest_paths = []
        processing_path.append(new_path)

        while len(processing_path) > 0:
            next_process_path = []
            for cur_path in processing_path:
                concatings = self.previous[cur_path[-1]]
                if concatings:
                    for prev_node, _ in concatings.items():
                        new_path = cur_path + [prev_node]   # concat path
                        next_process_path.append(new_path)
                else:
                    all_shortest_paths.append(cur_path)
            processing_path = next_process_path
    
        return all_shortest_paths

    def __str__(self):
        """
        System.out.printf("v\tdist\tprev\n");
		for (int i = 0; i < n; i++) {
			System.out.printf("%d\t%6.4f\t%d\n", i, distance[i], previous[i]);
		}
        :return: 
        """
        strItems = []
        for i in range(self.n):
            strItems.append('(dist: {},  prev: {})'.format(self.distance[i], str(self.previous[i])))

        return '\n'.join(strItems)