"""
Console class for this graph
@author David Guan
"""

from cmd import Cmd

from graph import Graph
import webbrowser


class Console(Cmd):
    def __init__(self):
        """
        Constructor for the Console class
        """
        Cmd.__init__(self)
        self.prompt = "=>> "
        self.intro = "Welcome to CSAir!\nInput a command or type help for more"
        self.graph = Graph()
        self.graph.add_from_json('../Data/map_data.json')
        self.graph.add_from_json('../Data/cmi_hub.json')

    def do_all_cities(self, args):
        """
        Grabs a list of all the cities this airline can fly to and its code
        :param args: nothing, leave blank. Type all_cities
        :return: all the cities this airline can fly to with its name and code
        """
        for key, val in self.graph.vertices.items():
            print("City: {}, code: {}".format(val.name, val.code))

    def do_city(self, args):
        """
        Grabs city information by its argument i.e. city SCL
        :param args: code, name, country, continent, timezone, coordinates (lat & long), population, region
        :return: specific argument requested, such as the code or the name or tells the user it's not there
        """
        string = args.split()
        if len(string) <= 0:
            print("Enter a valid argument")
        else:
            if args in self.graph.vertices:
                for key, val in vars(self.graph.vertices[args]).items():
                    print("{}: {}".format(key, val))
            else:
                print("Enter a valid city")

    def do_all_single_flights(self, args):
        """
        Grabs a list of all the other cities accessible via a single nonstop flight
        Enter by code name and it'll find all cities it can go to as well as distance
        :param args: city code, i.e. SCL for Santiago
        :return: a list of all flights from the city
        """
        if args in self.graph.edges:
            for edge in self.graph.edges[args]:
                print("City: {}, distance: {}".format(edge.destination, edge.distance))
        else:
            print("City does not exist!")

    def do_longest_flight(self, args):
        """
        Displays the longest flight in this network of flights
        :param args: nothing, can type longest_flight
        :return: longest flight by codes and distance
        """
        longest = self.graph.longest_flight()
        print("Longest flight is from {} to {} and distance is {}".format(longest[0], longest[1], longest[2]))

    def do_shortest_flight(self, args):
        """
        Displays the shortest flight in this network of flights
        :param args: nothing, can type shortest_flight
        :return: shortest flight by codes and distance
        """
        shortest = self.graph.shortest_flight()
        print("Shortest flight is from {} to {} and distance is {}".format(shortest[0], shortest[1], shortest[2]))

    def do_average_flight(self, args):
        """
        Displays the average distance of all the flights in this network of flights
        :param args: nothing, can type average_flight
        :return: average distance of all the flights
        """
        print("Average distance is {}".format(self.graph.average_distance()))

    def do_biggest_city(self, args):
        """
        Displays the biggest city of all the cities in the network
        :param args: nothing, can type biggest_city
        :return: biggest city by code, name, and population size
        """
        biggest = self.graph.biggest_city()
        print("Biggest city is: {} {} and population is: {}".format(biggest[0], biggest[1], biggest[2]))

    def do_smallest_city(self, args):
        """
        Displays the smallest city of all the cities in the network
        :param args: nothing, type smallest_city
        :return: smallest city by code, name, and population size
        """
        smallest = self.graph.smallest_city()
        print("Smallest city is: {} {} and population is: {}".format(smallest[0], smallest[1], smallest[2]))

    def do_average_city_size(self, args):
        """
        Displays the average size of all the cities in the network
        :param args: nothing, type average_city_size
        :return: average size of the cities rounded down
        """
        print("Average size of the cities is: {}".format(self.graph.average_city_size()))

    def do_continents_and_cities(self, args):
        """
        Displays all the continents and the cities each one
        :param args: nothing, type continents_and_cities
        :return: all the continents and cities that belong in each one
        """
        list_all = self.graph.continents_and_cities()
        for continent, cities in list_all.items():
            print(continent, end=": ")
            print(", ".join(cities))

    def do_hubs(self, args):
        """
        Displays the top 5 hubs based on the number of outgoing connections
        :param args: nothing, type hubs
        :return: the top 5 hubs by code
        """
        hubs = self.graph.hubs()
        for cities in hubs:
            print("{} with {} outgoing routes".format(cities[0], cities[1]))

    def do_visualize(self, args):
        """
        Displays a map of the entire route
        This function displays the link as well as opens it in a browser for you
        :param args: nothing, type visualize
        :return: a map of the entire network of flights
        """
        url = "http://www.gcmap.com/mapui?P="
        for code, _list in self.graph.edges.items():
            for edge in _list:
                url = "{}{}-{},".format(url, edge.start, edge.destination)
        print(url)
        webbrowser.open(url)

    def do_del_city(self, args):
        """
        Deletes a city from the network
        Note that this deletes the city both ways in the network as well
        :param args: city code to remove
        :return: city removed or not
        """
        if self.graph.remove_city(args):
            print("City removed")
        else:
            print("City not found")

    def do_del_route(self, args):
        """
        Deletes a route from the network
        This deletes both way
        Argument must consist of two codes, i.e. del_route TYO LAX
        :param args: two codes for the cities
        :return: route removed or not
        """
        route = args.split()
        if len(route) <= 1:
            print("Enter a valid number of arguments")
        else:
            if self.graph.remove_route(route[0], route[1]):
                print("Edge removed")
            else:
                print("Edge couldn't be found")

    def do_add_city(self, args):
        """
        Adds a city to the network
        Asks for user input and calls the graph class afterwards
        :param args: none, can simply call add_city
        :return: city added or not
        """
        city = {"code": input("Enter city code"), "name": input("Enter city name"),
                "country": input("Enter city country"), "continent": input("Enter city continent"),
                "timezone": input("Enter city timezone")}
        coordinates = input("Enter coordinates, i.e. N 5 W 74")
        coordinates = coordinates.strip()
        while len(coordinates) < 4:
            coordinates = input("Please enter a valid coordinate parameter, i.e. N 5 W 74")
            coordinates = coordinates.split()
        city["coordinates"] = {coordinates[0]: coordinates[1], coordinates[2]: coordinates[3]}
        population = input("Enter city population")
        while int(population) < 0:
            population = input("Please enter a valid population size")
        city["population"] = population
        city["region"] = input("Enter city region")
        self.graph.add_city(city)
        print("City added!")

    def do_add_route(self, args):
        """
        Takes in three parameters for args so that we can add them to the network
        Must add in the order of distance start destination
        :param args: three different parameters, i.e. 5000 TYO LAX
        :return: route added
        """
        route = args.split()
        if len(route) < 3:
            print("Enter valid parameters")
        else:
            self.graph.add_route(route[0], route[1], route[2])
            print("Route added!")

    def do_edit_city(self, args):
        """
        Takes in three parameters to edit the city
        Must add in order of the code, key, value
        :param args: three different parameters, i.e. LAX name somecity
        :return: city edited
        """
        city = args.split()
        if len(city) < 3:
            print("Enter valid parameters")
        else:
            if city[0] in self.graph.vertices:
                self.graph.edit_city(city[0], city[1], city[2])
                print("City edited!")
            else:
                print("City does not exist!")

    def do_save_json(self, args):
        """
        Saves the data to the json
        Simply call by save_json
        :param args: none
        :return: JSON saved
        """
        self.graph.save_to_json()

    def do_load_json(self, args):
        """
        Loads the data from the json
        :param args: none, simply uses the same file
        :return: JSON loaded
        """
        self.graph.vertices.clear()
        self.graph.edges.clear()
        self.graph.add_from_json('../Data/save.json')

    def do_route_info(self, args):
        """
        Checks if a route is valid based on argument of spaces
        :param args: code names separated by spaces
        :return: true or false on whether a route is valid
        """
        route = args.split()
        result = self.graph.route_info(route)
        print(result)
        if result is not None:
            print("Total distance is {} km, cost is {} dollars, and time is {} hours".format(result[0], result[1],
                                                                                             result[2]))
        else:
            print("Invalid route")

    def do_shortest_route(self, args):
        """
        Gets the shortest route from two cities
        :param args: two city codes, i.e. CMI NYC
        :return: shortest route between the two
        """
        route = args.split()
        if len(route) < 1:
            print("Enter two cities")
        else:
            path = self.graph.djikstra(route[0], route[1])
            print("Route is ", end="")
            route = ""
            for code in path:
                if code is not path[-1]:
                    print(code, end="->")
                else:
                    print(code)
                route = route + " " + code
            self.do_route_info(route)

    def do_help(self, args):
        """
        Gets help for a certain command
        :param args: Any input you need help with
        :return: Documented comments about the command
        """
        Cmd.do_help(self, args)

    def do_quit(self, args):
        """
        Exits on system end or EOF
        :param args:
        :return:
        """
        exit()

    def emptyline(self):
        """
        Defines what happens when nothing is typed in
        :return: Output telling user to type something in
        """
        print("Please input something. Type help for available commands")

    def default(self, line):
        """
        Defines what happens when anything other than these commands are typed
        :param line: random input the user types
        :return: Output telling user to type in a valid command
        """
        print("Command not recognized. Type help for available commands")


console = Console()
console.cmdloop()
