from typing import Dict, List
from queue import PriorityQueue


class Dijkstra(object):
    """
    Implementation of the Dijkstra algorithm using a priority queue. This
    utility helps find all shortest paths in a phrase graph in a segmentation.
    """
    def __init__(self, edges: Dict):
        self.edges = edges
        self.n = len(edges)
        self.distance = [float('inf')] * self.n
        self.previous = [-1] * self.n

        self.distance[self.n - 1] = 0.0
        self.distance[self.n - 1] = 0

        # we init values in variable constructor
        # for i in range(self.n):
        #    self.distance[i] = None
        #    self.previous[i] = None

        pqueue = PriorityQueue(self.n)
        pqueue.put((self.distance[self.n-1], self.n - 1))
        while not pqueue.empty():
            v = pqueue.get_nowait()
            nodes = self.edges[v[1]]
            for u in nodes:
                d = self.length(u, v[1]) + self.distance[v[1]]
                if d < self.distance[u]:
                    self.distance[u] = d
                    self.previous[u] = v[1]
                    pqueue.put((self.distance[u], u))

    def length(self, u: int, v: int) -> float:
        """
        The length between two nodes u and v. In a phrase graph, this
        length is equal to 1.0/(v-u).
        :param u: 
        :param v: 
        :return: the length between u and v.
        """
        if u == v:
            return 0.0
        else:
            return float(1)/(v - u)

    def shortestPaths(self) -> list:
        """
        Finds all shortest paths on this graph, between vertex <code>0</code>
        and vertex <code>n-1</code>.
        :return: all shortest paths.
        """
        return self.shortestPathsInternal(self.n - 1)

    def shortestPathsInternal(self, v: int) -> list:
        """
        Finds all shortest paths on this graph, between vertex <code>0</code>
	    and vertex <code>v</code>.
        :param v: a vertex 
        :return: all shortest paths
        """
        nodes = self.edges[v]
        if not nodes:
            stop = []
            stop.append(v)
            list = []
            list.append(stop)
            return list
        else:
            vList = []
            for u in nodes:
                d = self.length(u, v) + self.distance[v]
                if self.distance[u] == d:
                    #  recursively compute the paths from u
                    uList = self.shortestPathsInternal(u)
                    for list in uList:
                        list.append(v)
                        vList.append(list)

            return vList

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
            strItems.append('(dist: {},  prev: {})'.format(self.distance[i], self.previous[i]))

        return '\n'.join(strItems)