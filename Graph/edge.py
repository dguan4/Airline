"""
Edge class for this graph
@author David Guan
"""


class Edge:
    def __init__(self, distance, start, destination):
        """
        Constructor for the Edge class
        :param distance: distance from start to destination
        :param start: starting location
        :param destination: ending location, destination
        :return: nothing
        """
        self.distance = distance
        self.start = start
        self.destination = destination


