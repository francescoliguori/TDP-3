from TdP_collections.graphs.graph import Graph

from TdP_collections.priority_queue.adaptable_heap_priority_queue import AdaptableHeapPriorityQueue
from TdP_collections.list.positional_list import PositionalList
from circular_positional_list import CircularPositionalList
#Progettare una funzione find_route() che, preso in input l’orario della compagnia, gli areoporti a e b, ed un orario di partenza t,
# trova la rotta che permette di arrivare da a a b nel minor tempo possibile, partendo ad un orario non precedente a t.
# (Come per l’esercizio precedente, bisogna tener conto del tempo minimo di coincidenza di
# ogni scalo).

def find_route(g, src, dest, t):
    """Preso in input l’orario della compagnia, gli areoporti a e b, ed un orario di partenza t,
     trova la rotta che permette di arrivare da a a b nel minor tempo possibile, partendo ad un orario non precedente a t.
     Tenere conto del tempo di coincidenza id ogni aeroporto."""
    #Aggiungere caso in cui src o dest non appatengono al grafo
    if not isinstance(src, CompagniaAreaFindRouteGraph.NewVertex) or not isinstance(dest, CompagniaAreaFindRouteGraph.NewVertex):
        raise TypeError('a e b devono essere NewVertex')
    if t < 0:
        raise ValueError("t deve essere un orario (double)")
    cloud, precedente = shortest_path_lengths(g, src, t)

    if dest in cloud and cloud[dest] != float("inf"):
        #Ricostruzione del percorso qualora la destinazione sia raggiungibile
        path = shortest_path(dest,precedente)
        for p in path:
            print(p)
    else:
        print("Destinazione non raggiungibile")
    #print(cloud)

def shortest_path_lengths(g, src,t):
    """Compute shortest-path distances from src to reachable vertices of g.

    Graph g can be undirected or directed, but must be weighted such that
    e.element() returns a numeric weight for each edge e.

    Return dictionary mapping each reachable vertex to its distance from src.
    """
    d = {}  # d[v] is upper bound from s to v
    cloud = {}  # map reachable v to its d[v] value
    pq = AdaptableHeapPriorityQueue()  # vertex v will have key d[v]
    pqlocator = {}  # map from vertex to its pq locator

    #dizionario che mappa ad ogni vertice quello che lo precede lungo il cammino
    precedente = {}
    # for each vertex v of the graph, add an entry to the priority queue, with
    # the source having distance 0 and all others having infinite distance
    for v in g.vertices():
        if v is src:
           # d[v] = 0
            d[v] = [0,t]
           #prima del vertice iniziale c'è None
            precedente[v] = None

        else:
            #d[v] = float('inf')  # syntax for positive infinity
            d[v] = [float('inf'),float('inf')]
        pqlocator[v] = pq.add(d[v][0], v)  # save locator for future updates

    while not pq.is_empty():
        key, u = pq.remove_min()
        cloud[u] = key  # its correct d[u] value
        del pqlocator[u]  # u is no longer in pq
        for e in g.incident_edges(u):  # outgoing edges (u,v)
            v = e.opposite(u)
            if v not in cloud:
                # perform relaxation step on edge (u,v)
                #Il tempo per andare da A a B è il tempo di volo + il tempo che è necessario attendere in A
                wgt = e.element() + u.get_tc()
                print("Orario arrivo in " + str(u) + ": " + str(d[u][1]))
                print("Orario partenza da "+str(u)+": "+str(e.get_orario_partenza()))
                print("Orario arrivo + coincidenza:"+str(d[u][1]+ u.get_tc()))
                #per partire da un aeroporto l'orario di partenza deve essere maggiore dell'orario in cui siamo arrivati
                #+ il tempo di coincidenza
                if d[u][0] + wgt < d[v][0] and e.get_orario_partenza() > d[u][1] + u.get_tc():  # better path to v?

                    d[v][0] = d[u][0] + wgt  # update the distance

                    precedente[v] = u
                    #si aggiorna l'orario di arrivo
                    d[v][1] = e.get_orario_arrivo()
                    pq.update(pqlocator[v], d[v][0], v)  # update the pq entry

    return cloud, precedente # only includes reachable vertices


def shortest_path_tree(g, s, dest, d):
    """Reconstruct shortest-path tree rooted at vertex s, given distance map d.

    Return tree as a map from each reachable vertex v (other than s) to the
    edge e=(u,v) that is used to reach v from its parent u in the tree.
    """
    tree = {}
    for v in d:
        if v is not s:
            for e in g.incident_edges(v, False):  # consider INCOMING edges
                u = e.opposite(v)
                #wgt = e.element()
                #Si considera anche il tempo di coicidenza
                wgt = e.element() + u.get_tc()
                if d[v] == d[u] + wgt:
                    tree[v] = e  # edge e is used to reach v
                #Si ferma la costruzione dell'albero una volta raggiunta la destinazione
                if v == dest:
                    return tree
    return tree

def shortest_path(dest, precedente):
    """Si calcola il percorso minimo tra verso la destinazione"""
    #controlli opportuni su src, dest e g

    path = []
    walk = dest
    path.insert(0,walk)
    while precedente[walk] is not None:
        path.insert(0,precedente[walk])
        walk = precedente[walk]
    return path


class CompagniaAreaFindRouteGraph(Graph):

    class NewVertex(Graph.Vertex):
        def __init__(self, x, tc):
            """Do not call constructor directly. Use Graph's insert_vertex(x)."""
            self._element = x
            #tempo da attendere in un aereporto prima di poter prendere un altro volo
            self._tc = tc

        def get_tc(self):
            #metodo per ritornare il tempo da aspettare in un aereoporto prima della prossima coincidenza
            return self._tc


    class NewEdge(Graph.Edge):

        def __init__(self, u, v, orario_partenza, orario_arrivo, posti_disponibili):
            #Verificare orario di arrivo sia maggiore di orario di partenza, cioè il tempo di volo deve essere positivo

            self._origin = u
            self._destination = v
            self._element = orario_arrivo-orario_partenza
            self._orario_partenza = orario_partenza
            self._orario_arrivo = orario_arrivo
            self._posti_disponibili = posti_disponibili

        def get_orario_partenza(self):
            return self._orario_partenza

        def get_orario_arrivo(self):
            return self._orario_arrivo

    def insert_vertex(self, x, tc):
        """Insert and return a new Vertex with element x."""
        v = self.NewVertex(x,tc)
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}  # need distinct map for incoming edges
        return v

    def insert_edge(self, u, v, orario_partenza, orario_arrivo, posti_disponibili):
        """Insert and return a new Edge from u to v with auxiliary element x.

        Raise a ValueError if u and v are not vertices of the graph.
        Raise a ValueError if u and v are already adjacent.
        """
        if self.get_edge(u, v) is not None:  # includes error checking
            raise ValueError('u and v are already adjacent')
        e = self.NewEdge(u, v, orario_partenza, orario_arrivo, posti_disponibili)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e





def testFindRoute():
    g = CompagniaAreaFindRouteGraph(True)

    a = g.insert_vertex("A", 1)
    b = g.insert_vertex("B", 2)
    c = g.insert_vertex("C", 3)
    d = g.insert_vertex("D", 4)
    e = g.insert_vertex("E", 5)
    f = g.insert_vertex("F", 5)
    #edge:  u, v, orario_partenza, orario_arrivo, posti_disponibili
    g.insert_edge(a, b, 8.0, 10.0, 1)
    g.insert_edge(b, c, 13.0, 14.0, 1)
    g.insert_edge(c, d, 17.5, 19.0, 1)
    g.insert_edge(d, e, 19.0, 22.0, 1)
    g.insert_edge(b, e, 13.0, 15.0, 1)
    #find_route(g, a, b, 9.0)
    #f non è raggiungibile

    find_route(g, a, f, 5.0)
    print("_________________________")
    find_route(g, a, d, 5.0)


if __name__ == "__main__":
    testFindRoute()