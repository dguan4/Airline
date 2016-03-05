"""
Vertex class for this graph
@author David Guan
"""


class Vertex:

    def __init__(self, metros):
        """
        Vertex constructor for vertices
        Simple check that raises an Exception if the metros isn't proper
        Might have to change this class around later if we're to edit information
        :param metros: a dictionary with the information of the city
        :return: nothing
        """
        if len(metros) == 8 and "code" in metros:
            self.code = metros["code"]
            self.name = metros["name"]
            self.country = metros["country"]
            self.continent = metros["continent"]
            self.timezone = metros["timezone"]
            self.coordinates = metros["coordinates"]
            self.population = metros["population"]
            self.region = metros["region"]
        else:
            raise Exception

