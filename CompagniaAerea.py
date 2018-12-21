from TdP_collections.graphs.graph import Graph


class CompagniaAerea(Graph):
    def __init__(self, directed=False):
        super().__init__(directed)

    def inserisci_vertice(self, name_aiport, connecting_time):
        if not isinstance(connecting_time, int):
            raise TypeError("connecting_time is not int.")
        if connecting_time < 0:
            raise ValueError("connecting_time must be a positive number.")
        return super().insert_vertex([name_aiport, connecting_time])

    def inserisci_arco(self, origin_aiport, destination_aiport, departure_time, arrival_time, places_available):
        volo = {}
        volo["l"] = arrival_time
        volo["a"] = departure_time
        volo["p"] = places_available
        super().insert_edge(origin_aiport, destination_aiport, volo)

    '''A recursive function to print all paths from 'u' to 'd'. 
            visited[] keeps track of vertices in current path. 
            path[] stores actual vertices and path_index is current 
            index in path[]'''


def _print_all_paths_util(g, u, d, path, time_departure, time_travel, arrival_time=0, sorgente=True):  # o(2m)
    # Mark the current node as visited and store in path
    path.append(u)

    # If current vertex is same as destination, then print
    if u == d:
        print("\n\n")
        for e in path:
            print(e)
    else:
        # If current vertex is not destination
        # Recur for all the vertices adjacent to this vertex
        for i in g.incident_edges(u):
            if sorgente:
                if arrival_time <= i.element()["a"] and time_departure <= i.element()["a"] and time_travel >= i.element()["l"] - i.element()["a"]:
                    _print_all_paths_util(g, i.opposite(u), d, path, time_departure, time_travel - (i.element()["l"] - i.element()["a"]),
                                          arrival_time=i.element()["l"], sorgente=False)

            else:
                if arrival_time + u.element()[1] <= i.element()["a"] and time_travel >= i.element()["l"] - i.element()["a"] + u.element()[1]:
                    _print_all_paths_util(g, i.opposite(u), d, path, time_departure, time_travel - (i.element()["l"] - i.element()["a"] + u.element()[1]),
                                          arrival_time=i.element()["l"], sorgente=False)

    # Remove current vertex from path[]
    path.pop()


# Prints all paths from 's' to 'd'
def list_routes(g, s, d, time_departure, time_travel):  #circa o(n+2m)
    # Create an array to store paths
    path = []

    # Call the recursive helper function to print all paths
    _print_all_paths_util(g, s, d, path, time_departure, time_travel)


g = CompagniaAerea(True)
# primo albero
jfk = g.inserisci_vertice("JFK", 2)
bos = g.inserisci_vertice("BOS", 5)
ord = g.inserisci_vertice("ORD", 8)
dfw = g.inserisci_vertice("DFW", 3)
mia = g.inserisci_vertice("MIA", 10)

g.inserisci_arco(jfk, bos, 10, 30, 5)
g.inserisci_arco(bos, ord, 50, 60, 5)
g.inserisci_arco(jfk, ord, 60, 70, 5)
g.inserisci_arco(bos, mia, 55, 75, 5)
g.inserisci_arco(bos, jfk, 35, 50, 5)
g.inserisci_arco(ord, dfw, 68, 80, 5)
g.inserisci_arco(dfw, bos, 80, 90, 5)
g.inserisci_arco(ord, mia, 67, 87, 5)
g.inserisci_arco(mia, jfk, 82, 99, 5)

#secondo albero
sfo = g.inserisci_vertice("SFO", 6)
lax = g.inserisci_vertice("LAX", 6)
rom = g.inserisci_vertice("ROM", 6)
mil = g.inserisci_vertice("MIL", 6)
nap = g.inserisci_vertice("NAP", 6)

for e in g.edges():
    print(e)

list_routes(g, jfk, ord, 5, 100)
