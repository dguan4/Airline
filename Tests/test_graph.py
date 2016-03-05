from unittest import TestCase
from graph import Graph
from edge import Edge
from vertex import Vertex
import collections as col


class TestGraph(TestCase):
    def test_add_from_json(self):
        """
        Tests the add_from_json function in the Graph class
        :return: true if all asserts pass
        """
        graph = Graph()
        graph.add_from_json('../Data/map_data.json')
        self.assertIsInstance(graph, Graph)
        self.assertIsInstance(graph.edges, dict)
        self.assertIs(len(graph.edges), 48)
        self.assertIs(len(graph.vertices), 48)
        pass

    def test_longest_flight(self):
        """
        Tests the longest_flight function in the Graph class
        :return: true if all tests pass
        """
        graph = Graph()
        graph.add_from_json('../Data/map_data.json')
        longest = graph.longest_flight()
        self.assertEqual(longest[2], 12051)
        self.assertTrue(longest[0] in ("SYD", "LAX"))
        self.assertTrue(longest[1] in ("SYD", "LAX"))
        self.assertIsNot(longest, 0)
        pass

    def test_shortest_flight(self):
        """
        Tests the shortest_flight function in the Graph class
        :return: true if all tests pass
        """
        graph = Graph()
        graph.add_from_json('../Data/map_data.json')
        shortest = graph.shortest_flight()
        self.assertEqual(shortest[2], 334)
        self.assertTrue(shortest[0] in ("WAS", "NYC"))
        self.assertTrue(shortest[1] in ("WAS", "NYC"))
        self.assertIsNot(shortest[2], 0)
        pass

    def test_average_distance(self):
        """
        Tests the average distance
        :return: true if all test pass
        """
        graph = Graph()
        graph.add_from_json('../Data/map_data.json')
        average = graph.average_distance()
        self.assertEqual(average, 2300.276595744681)
        self.assertNotEqual(average, 0)
        pass

    def test_biggest_city(self):
        """
        Tests the biggest city
        :return: true if all tests pass
        """
        graph = Graph()
        graph.add_from_json('../Data/map_data.json')
        biggest = graph.biggest_city()
        self.assertEqual(biggest[2], 34000000)
        self.assertTrue(biggest[1] in ("TYO", "Tokyo"))
        self.assertTrue(biggest[0] in ("TYO", "Tokyo"))
        pass

    def test_smallest_city(self):
        """
        Tests the smallest city
        :return: true if all tests pass
        """
        graph = Graph()
        graph.add_from_json('../Data/map_data.json')
        smallest = graph.smallest_city()
        self.assertEquals(smallest[2], 589900)
        self.assertTrue(smallest[0] in ("ESS", "Essen"))
        self.assertTrue(smallest[1] in ("ESS", "Essen"))
        pass

    def test_average_city_size(self):
        """
        Test the average city size
        :return: true if all tests pass
        """
        graph = Graph()
        graph.add_from_json('../Data/map_data.json')
        average = graph.average_city_size()
        self.assertEqual(average, 11796143)
        self.assertNotEqual(average, 0)
        pass

    def test_continents_and_cities(self):
        """
        Test the continents and cities
        :return: true if all tests pass
        """
        graph = Graph()
        graph.add_from_json('../Data/map_data.json')
        list_continents_and_cities = graph.continents_and_cities()
        self.assertNotEqual(len(list_continents_and_cities), 0)
        cities = ("Buenos Aires", "Bogota", "Santiago", "Lima", "Sao Paulo")
        self.assertTrue(list_continents_and_cities["South America"][0] in cities)
        self.assertTrue(list_continents_and_cities["South America"][1] in cities)
        self.assertTrue(list_continents_and_cities["South America"][2] in cities)
        self.assertTrue(list_continents_and_cities["South America"][3] in cities)
        self.assertTrue(list_continents_and_cities["South America"][4] in cities)
        cities = ("Beijing", "Bangkok", "Osaka", "Taipei", "Chennai", "Shanghai", "Mumbai", "Ho Chi Minh City", "Riyadh", "Karachi", "Manila", "Tokyo", "Seoul", "Bagdad", "Delhi", "Jakarta", "Hong Kong", "Calcutta", "Tehrah")
        self.assertTrue(list_continents_and_cities["Asia"][0] in cities)
        self.assertTrue(list_continents_and_cities["Asia"][1] in cities)
        self.assertTrue(list_continents_and_cities["Asia"][2] in cities)
        self.assertTrue(list_continents_and_cities["Asia"][3] in cities)
        self.assertTrue(list_continents_and_cities["Asia"][4] in cities)
        self.assertTrue(list_continents_and_cities["Asia"][5] in cities)
        self.assertTrue(list_continents_and_cities["Asia"][6] in cities)
        self.assertTrue(list_continents_and_cities["Asia"][7] in cities)
        self.assertTrue(list_continents_and_cities["Asia"][8] in cities)
        self.assertTrue(list_continents_and_cities["Asia"][9] in cities)
        self.assertTrue(list_continents_and_cities["Asia"][10] in cities)
        self.assertTrue(list_continents_and_cities["Asia"][11] in cities)
        self.assertTrue(list_continents_and_cities["Asia"][12] in cities)
        self.assertTrue(list_continents_and_cities["Asia"][13] in cities)
        self.assertTrue(list_continents_and_cities["Asia"][14] in cities)
        self.assertTrue(list_continents_and_cities["Asia"][15] in cities)
        self.assertTrue(list_continents_and_cities["Asia"][16] in cities)
        self.assertTrue(list_continents_and_cities["Asia"][17] in cities)
        self.assertTrue(list_continents_and_cities["Asia"][18] in cities)
        pass

    def test_hubs(self):
        """
        Test the hubs in the network
        :return: true if all tests pass
        """
        graph = Graph()
        graph.add_from_json('../Data/map_data.json')
        hubs = graph.hubs()
        dict = {('HKG', 6),('IST', 6),('BGW', 5),('BKK', 5),('BOG', 5)}
        self.assertTrue(hubs[0] in dict)
        self.assertTrue(hubs[1] in dict)
        self.assertTrue(hubs[2] in dict)
        self.assertTrue(hubs[3] in dict)
        self.assertTrue(hubs[4] in dict)
        pass

    def test_remove_cities(self):
        """
        Test the remove cities function
        :return: true if all tests pass
        """
        graph = Graph()
        graph.add_from_json('../Data/test.json')
        self.assertTrue("AYY" in graph.vertices)
        self.assertTrue("LOL" in graph.vertices)
        self.assertTrue("LMA" in graph.vertices)
        self.assertTrue("AYY" in graph.edges)
        self.assertTrue("AYY" in graph.edges["AYY"][0].start)
        graph.remove_city("AYY")
        self.assertFalse("AYY" in graph.vertices)
        self.assertFalse("AYY" in graph.edges)
        for _list in graph.edges.values():
            for edge in _list:
                self.assertFalse("AYY" == edge.start)
                self.assertFalse("AYY" == edge.destination)
        pass

    def test_remove_route(self):
        """
        Test the remove route function
        :return: true if all tests pass
        """
        graph = Graph()
        graph.add_from_json('../Data/test.json')
        self.assertTrue("AYY" in graph.edges)
        ayy_edge = graph.edges["AYY"]
        for edge in ayy_edge:
            self.assertTrue("AYY" == edge.start)
        for edge in graph.edges["LOL"]:
            self.assertTrue("AYY" == edge.destination or "LMA" == edge.destination)
        graph.remove_route("AYY", "LOL")
        for edge in ayy_edge:
            self.assertFalse("LOL" == edge.destination)
        for edge in graph.edges["LOL"]:
            self.assertTrue("AYY" == edge.destination or "LMA" == edge.destination)
        graph.remove_route("LOL", "AYY")
        for edge in graph.edges["LOL"]:
            self.assertFalse("AYY" == edge.destination)
        pass

    def test_add_city(self):
        """
        Test the add city function
        :return: true if all tests pass
        """
        graph = Graph()
        metros = {'code': "SCL", 'name': "Santiago", 'country': "CL", 'continent': "South America", 'timezone': -4,
                  'coordinates': {"S": 33, "W": 71}, 'population': 6000000, 'region': 1}
        vertex = Vertex(metros)
        self.assertFalse(vertex in graph.vertices)
        graph.add_city(metros)
        self.assertTrue("SCL" in graph.vertices)
        other_vertex = graph.vertices["SCL"]
        self.assertTrue(vertex.code == other_vertex.code)
        self.assertTrue(vertex.name == other_vertex.name)
        self.assertTrue(vertex.country == other_vertex.country)
        self.assertTrue(vertex.continent == other_vertex.continent)
        self.assertTrue(vertex.timezone == other_vertex.timezone)
        self.assertTrue(vertex.coordinates == other_vertex.coordinates)
        self.assertTrue(vertex.population == other_vertex.population)
        self.assertTrue(vertex.region == other_vertex.region)
        pass

    def test_add_route(self):
        """
        Test the add route function
        :return: true if all tests pass
        """
        graph = Graph()
        distance = 420
        start = "LOL"
        destination = "KEK"
        edge = Edge(distance, start, destination)
        self.assertFalse("LOL" in graph.edges)
        graph.add_route(distance, start, destination)
        self.assertTrue("LOL" in graph.edges)
        self.assertTrue(start == graph.edges["LOL"][0].start)
        self.assertTrue(destination == graph.edges["LOL"][0].destination)
        self.assertTrue(distance == graph.edges["LOL"][0].distance)
        self.assertTrue(edge.start == graph.edges["LOL"][0].start)
        self.assertTrue(edge.destination == graph.edges["LOL"][0].destination)
        self.assertTrue(edge.distance == graph.edges["LOL"][0].distance)
        pass

    def test_edit_city(self):
        """
        Test the edit city function
        :return: true if all tests pass
        """
        graph = Graph()
        graph.add_from_json('../Data/test.json')
        self.assertTrue("LOL" in graph.vertices)
        vertex = graph.vertices["LOL"]
        self.assertTrue(vertex.code == "LOL")
        self.assertTrue(vertex.name == "Hello")
        graph.edit_city("LOL", "code", "KEK")
        self.assertTrue("KEK" in graph.vertices)
        self.assertFalse("LOL" in graph.vertices)
        vertex = graph.vertices["KEK"]
        self.assertTrue(vertex.name == "Hello")
        graph.edit_city("KEK", "name", "BLAH")
        self.assertTrue(vertex.name == "BLAH")
        pass

    def test_route_info(self):
        """
        Test whether the route information is correct
        :return: true if all tests pass
        """
        graph = Graph()
        graph.add_from_json('../Data/test.json')
        route = graph.route_info(["LOL", "AYY"])
        self.assertTrue(route[0] == 2736)
        self.assertTrue(route[1] == 957.6)
        self.assertTrue(route[2] == 4.18)
        route = graph.route_info(["LOL", "AYY", "LMA"])
        self.assertTrue(route[0] == 9705)
        self.assertTrue(route[1] == 3048.3)
        self.assertTrue(route[2] == 15.84)
        route = graph.route_info(["BLAH", "LOL"])
        self.assertTrue(route == (0, 0, 0))
        pass

    def test_djikstra(self):
        """
        Test whether djikstra calculates the shortest route
        :return: true if all tests pass
        """
        graph = Graph()
        graph.add_from_json('../Data/test.json')
        route = graph.djikstra("AYY", "LMA")
        self.assertTrue(["AYY", "LOL", "LMA"] == route)
        route = graph.djikstra("LMA", "AYY")
        self.assertTrue(route == ["LMA", "LOL", "AYY"])
        route = graph.djikstra("LOL", "LMA")
        self.assertTrue(route == ["LOL", "LMA"])
        route = graph.djikstra("LMA", "LOL")
        self.assertTrue(route == ["LMA", "LOL"])
