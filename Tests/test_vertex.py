from unittest import TestCase
from vertex import Vertex


class TestVertex(TestCase):
    def test_vertex_constructor(self):
        """
        Simple test to check if vertices are initialized correctly
        :return: true if the tests pass
        """
        metros = {"code": "SCL", "name": "Santiago"}
        self.assertRaises(Exception, Vertex, metros)
        metros = {"code": "SCL", "name": "Santiago", "country": "CL", "continent": "South America", "timezone": -4,
                  "coordinates": {"S": 33, "W": 71}, "population": 6000000, "region": 1}
        vertex = Vertex(metros)
        self.assertIsInstance(vertex, Vertex)
        self.assertIs(vertex.code, "SCL")
        self.assertIs(vertex.name, "Santiago")
        self.assertIs(vertex.country, "CL")
        self.assertIs(vertex.continent, "South America")
        self.assertIs(vertex.coordinates["S"], 33)
        self.assertIs(vertex.coordinates["W"], 71)
        self.assertIs(vertex.population, 6000000)
        self.assertIs(vertex.region, 1)
    pass
