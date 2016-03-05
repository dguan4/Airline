"""
Graph class for this graph
@author David Guan
"""

import collections as col
import json
from vertex import Vertex
from edge import Edge
import sys
import heapq
import math
import queue as q


class Graph:
    def __init__(self):
        """
        Constructor for the graph class
        :return:
        """
        self.vertices = col.defaultdict()
        self.edges = col.defaultdict(list)

    def add_from_json(self, location):
        """
        Adds nodes and edges from the json
        Loads up the map_data from the Data folder and adds all the data into the graph
        :param location of the file
        :return:
        """
        with open(location) as file:
            data = json.load(file)
            for metros in data["metros"]:
                self.vertices[metros["code"]] = Vertex(metros)
            for routes in data["routes"]:
                start = routes["ports"][0]
                destination = routes["ports"][1]
                distance = routes["distance"]
                self.edges[start].append(Edge(distance, start, destination))
                self.edges[destination].append(Edge(distance, destination, start))

    def longest_flight(self):
        """
        Longest flight function to find the longest flight in the flights
        :return: start vertex, destination vertex, distance
        """
        distance = 0
        for code, _list in self.edges.items():
            for edge in _list:
                if edge.distance > distance:
                    distance = edge.distance
                    start = edge.start
                    destination = edge.destination
        return start, destination, distance

    def shortest_flight(self):
        """
        Shortest flight function to find the shortest flight in the flights
        :return: start vertex, destination vertex, distance
        """
        distance = sys.maxsize
        for code, _list in self.edges.items():
            for edge in _list:
                if edge.distance < distance:
                    distance = edge.distance
                    start = edge.start
                    destination = edge.destination
        return start, destination, distance

    def average_distance(self):
        """
        Average distance of all the flights in the network
        :return: the average of all the distances
        """
        total = 0
        edges = 0
        for code, _list in self.edges.items():
            for edge in _list:
                total += edge.distance
                edges += 1
        return total / edges

    def biggest_city(self):
        """
        Biggest city in the network by population size
        :return: the biggest city by code, name, and size
        """
        biggest = 0
        for code, node in self.vertices.items():
            if node.population > biggest:
                biggest = node.population
                city_code = node.code
                name = node.name
        return city_code, name, biggest

    def smallest_city(self):
        """
        Smallest city in the network by population size
        :return: the smallest city by code, name, and size
        """
        smallest = sys.maxsize
        for code, node in self.vertices.items():
            if node.population < smallest:
                smallest = node.population
                city_code = node.code
                name = node.name
        return city_code, name, smallest

    def average_city_size(self):
        """
        Average population size of all the cities in the network
        :return: average population size, rounded down
        """
        average = 0
        total = 0
        for code, node in self.vertices.items():
            average += node.population
            total += 1
        return average // total

    def continents_and_cities(self):
        """
        List of the continents and the cities in them
        :return: a list of the continents and cities in each continent
        """
        list_all = col.defaultdict(list)
        for code, node in self.vertices.items():
            list_all[node.continent].append(node.name)
        return list_all

    def hubs(self):
        """
        List the hubs of the network
        http://stackoverflow.com/questions/14795333/how-to-maintain-dictionary-in-a-heap-in-python
        The first last few lines were used from this stackoverflow post. Not sure how it exactly works but it works
        :return: a list that has the all the cities with the number of connections
        """
        cities = col.defaultdict(int)
        for code, _list in self.edges.items():
            for edge in _list:
                cities[code] += 1
        heap = [(-value, key) for key, value in cities.items()]
        largest = heapq.nsmallest(5, heap)
        largest = [(key, -value) for value, key in largest]
        return largest

    def remove_city(self, code):
        """
        Removes the city from both the vertices and edges.
        Since we do two way routes, we have to loop through the edges to see if it contains the edges
        :param code: city to remove
        :return: true or false based on whether city is removed
        """
        if code in self.vertices:
            self.vertices.pop(code)
            self.edges.pop(code)
            for _code, _list in self.edges.items():
                for edge in _list:
                    if edge.start == code or edge.destination == code:
                        _list.remove(edge)
            return True
        return False

    def remove_route(self, start, destination):
        """
        Removes the route from the edge. This removes both sides of the edges This leaves the city intact
        :param start: city to remove
        :param destination: city to remove
        :return: true or false based on whether another route is removed
        """
        if start in self.edges and destination in self.edges:
            for edge in self.edges[start]:
                if edge.destination == destination:
                    self.edges[start].remove(edge)
            for edge in self.edges[destination]:
                if edge.destination == start:
                    self.edges[destination].remove(edge)
            return True
        return False

    def add_city(self, city):
        """
        Simply adds the city to the network
        This doesn't check for anything since we raise an exception if the parameters aren't set up correctly
        And also because this function should be called from console and not directly
        :param city: dictionary set up with codes, names, population, etc
        :return: none
        """
        self.vertices[city["code"]] = Vertex(city)

    def add_route(self, distance, start, destination):
        """
        Adds a route to the network
        This takes in three parameters which are simply codes and distances, since nothing else
        Is really needed
        Note that this doesn't really do much checking and adds the route in both directions
        :param distance: distance of the route
        :param start: starting city code
        :param destination: destination city code
        :return: none
        """
        self.edges[start].append(Edge(distance, start, destination))
        self.edges[destination].append(Edge(distance, destination, start))

    def edit_city(self, code, key, val):
        """
        Edits the city information. Note that this doesn't check for anything like whether it exists or not
        :param code: code of the city
        :param key: the key to change in the city, i.e. code, name, country, etc
        :param val: the value of the key to change
        :return: none
        """
        if key == "code":
            self.vertices[val] = self.vertices.pop(code)
            setattr(self.vertices[val], key, val)
        else:
            setattr(self.vertices[code], key, val)

    def save_to_json(self):
        """
        Saves the json to disk. Sets up the files and makes sure that extra routes aren't duplicated
        :return: nothing
        """
        file = col.defaultdict(list)
        data_sources = ["http://www.gcmap.com/",
                        "http://www.theodora.com/country_digraphs.html",
                        "http://www.citypopulation.de/world/Agglomerations.html",
                        "http://www.mongabay.com/cities_urban_01.htm",
                        "http://en.wikipedia.org/wiki/Urban_agglomeration",
                        "http://www.worldtimezone.com/standard.html"]
        file["data_sources"] = data_sources
        for code, city in self.vertices.items():
            metros = {}
            for key, val in vars(city).items():
                metros[key] = val
            file["metros"].append(metros)
        for code, _list in self.edges.items():
            for edge in _list:
                routes = {"ports": [edge.start, edge.destination], "distance": edge.distance}
                second_route = {"ports": [edge.destination, edge.start], "distance": edge.distance}
                if second_route not in file["routes"]:
                    file["routes"].append(routes)
        with open('../Data/save.json', 'w') as outfile:
            json.dump(file, outfile, indent=4)

    def route_info(self, route):
        """
        Checks if a route is valid
        If so, calculate the cost and time and total distance of the route

        :param route an array or list of routes. Start from the first index to the last
        :return: the distance, cost, and time
        """
        total_distance = 0
        cost_mult = 0.35
        cost = 0
        time = 0
        if route[0] in self.edges:
            for i in range(len(route) - 1):
                for edge in self.edges[route[i]]:
                    if edge.destination == route[i + 1]:
                        total_distance += edge.distance
                        cost += cost_mult * edge.distance
                        time += self.calc_time(edge.distance)
                        outgoing = len(self.edges[edge.destination])
                        # if this airport is not the last one since we don't need to calculate layover for last
                        if i is not len(route) - 2:
                            time += 2 - ((1 / 6) * (outgoing - 1))
                        if cost_mult > 0:
                            cost_mult -= 0.05
                        break;
                    else:
                        if edge == self.edges[route[i]][-1]:
                            return
        return total_distance, round(cost, 2), round(time, 2)

    def calc_time(self, distance):
        """
        Calculates the time needed for the distance
        This is all in hours
        It takes 32 minutes for a plane to finish accelerating and similarly for decelerating
        Acceleration is 1406.25 km^2/h
        All physics equations simplified
        :param distance: distance of the flight
        :return: time needed
        """
        if distance < 400:
            return 2*math.sqrt(distance / 1406.25)
        else:
            distance -= 400
            return distance / 750 + 16 / 15

    def djikstra(self, source, target):
        """
        Calculates the shortest route between two cities using Djikstra
        Taken from the pseudocode from Wikipedia

        TODO: Perhaps try to use priority queue or heapq instead?

        :param source: the source city of the algorithm
        :param target: the target city of the algorithm
        :return: the shortest path
        """
        dist = {}
        prev = {}
        set_q = {}
        for vertex in self.vertices.keys():
            dist[vertex] = sys.maxsize
            prev[vertex] = None
            set_q[vertex] = dist[vertex]
        dist[source] = 0
        set_q[source] = 0
        while set_q:
            vertex_u = min(set_q, key=set_q.get)
            if vertex_u == target:
                break
            set_q.pop(vertex_u)
            for edge in self.edges[vertex_u]:
                alt = dist[vertex_u] + edge.distance
                if alt < dist[edge.destination]:
                    dist[edge.destination] = alt
                    set_q[edge.destination] = dist[edge.destination]
                    prev[edge.destination] = vertex_u
        path = []
        vertex_u = target
        while prev[vertex_u]:
            path.insert(0, vertex_u)
            vertex_u = prev[vertex_u]
        path.insert(0, vertex_u)
        return path
