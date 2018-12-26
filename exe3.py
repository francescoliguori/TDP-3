from TdP_collections.graphs.graph import Graph

# from TdP_collections.priority_queue.adaptable_heap_priority_queue import AdaptableHeapPriorityQueue
# from TdP_collections.list.positional_list import PositionalList
# from circular_positional_list import CircularPositionalList


class CompagniaAreaFindRouteGraph(Graph):

    class NewVertex(Graph.Vertex):
        def __init__(self, x, tc):
            """Do not call constructor directly. Use Graph's insert_vertex(x)."""
            self._element = x
            # tempo da attendere in un aereporto prima di poter prendere un altro volo
            self._tc = tc

        def get_tc(self):
            # metodo per ritornare il tempo da aspettare in un aereoporto prima della prossima coincidenza
            return self._tc

    class NewEdge(Graph.Edge):

        def __init__(self, u, v, orario_partenza, orario_arrivo, posti_disponibili):
            # Verificare orario di arrivo sia maggiore di orario di partenza, cioè il tempo di volo deve essere positivo

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

        def get_posti_disponibili(self):
            return self._posti_disponibili

        def get_origin(self):
            return self._origin

    def insert_vertex(self, x, tc):
        """Insert and return a new Vertex with element x."""
        v = self.NewVertex(x, tc)
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


def find_sol(v, c, B, C):
    n = len(v)
    sol = list()
    while n-1 >= 0:
        if C[n-1][B]:
            sol.append(n-1)
            B = B-v[n-1]
        n -= 1
    return sol


def knapsack(volume, cost, B):
    n = len(volume)
    M = [[0 for k in range(B+1)] for i in range(n)]
    C = [[False for k in range(B+1)] for i in range(n)]
    for k in range(B+1):
        # trovo la posizione in tabella dove il solo elemento v[0] ci entra
        # da lì in poi copio nella tabella il suo costo
        if volume[0] <= k:
            M[0][k] = cost[0]
            C[0][k] = True
    for i in range(1, n):
        for k in range(B+1):
            if volume[i] <= k and M[i - 1][k - volume[i]] + cost[i] > M[i - 1][k]:
                M[i][k] = M[i-1][k - volume[i]] + cost[i]
                C[i][k] = True
            else:
                M[i][k] = M[i-1][k]

    # print("il valore della table:\n")
    # for i in range(len(M)):
    #     print(M[i])
    # print("\n\n\n\n\n\n")
    # print("C vale:\n")
    # for i in range(len(C)):
    #     print(C[i])
    return M[n-1][B], find_sol(volume, cost, B, C)


def select_flights(g, budget):
    gasolio, posti = [], []
    for e in g.edges():
        gasolio.append(int(e.element()*60))
        posti.append(e.get_posti_disponibili())
    print(gasolio)
    print(posti)
    n_posti, soluz = knapsack(gasolio, posti, budget)
    print(n_posti)
    print(soluz)
    archi = []
    for e in g.edges():
        archi.append(e.get_origin())
    airport = {}
    for sol in soluz:
        key = archi[sol]
        if key in airport.keys():
            airport[key] += gasolio[sol]
        else:
            airport[key] = gasolio[sol]
    for k in airport.keys():
        print("In airport:", k, "servono €:", airport[k])


def test_select_flights():
    g = CompagniaAreaFindRouteGraph()

    a = g.insert_vertex("A", 1)
    b = g.insert_vertex("B", 2)
    c = g.insert_vertex("C", 3)
    d = g.insert_vertex("D", 4)
    e = g.insert_vertex("E", 5)
    f = g.insert_vertex("F", 5)

    # edge:  u, v, orario_partenza, orario_arrivo, posti_disponibili
    g.insert_edge(a, b, 8.0, 10.0, 50)
    g.insert_edge(b, c, 13.0, 14.0, 45)
    g.insert_edge(c, d, 17.5, 19.0, 40)
    g.insert_edge(d, e, 19.0, 22.0, 60)
    g.insert_edge(b, e, 13.0, 15.0, 30)

    # budget in euro. Volo: 1h = 60 kg = 60 euro
    budget = 390

    select_flights(g, budget)


if __name__ == "__main__":
    test_select_flights()
