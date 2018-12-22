from TdP_collections.graphs.graph import *



def NewBFS(g, s, discovered,colore,X,Y):
    """Perform BFS of the undiscovered portion of Graph g starting at Vertex s.

    discovered is a dictionary mapping each vertex to the edge that was used to
    discover it during the BFS (s should be mapped to None prior to the call).
    Newly discovered vertices will be added to the dictionary as a result.
    """
    level = [s]  # first level includes only s

    colore[s] = 0
    X.append(s)
    while len(level) > 0:
        next_level = []  # prepare to gather newly found vertices
        for u in level:
            for e in g.incident_edges(u):  # for every outgoing edge from u
                v = e.opposite(u)
                if v not in discovered:  # v is an unvisited vertex

                    if colore[u] == 1:
                        colore[v] = 0
                        X.append(v)
                    else:
                        colore[v] = 1
                        Y.append(v)

                    discovered[v] = e  # e is the tree edge that discovered v
                    next_level.append(v)  # v will be further considered in next pass
        level = next_level  # relabel 'next' level to become current



def NewBFS_complete(g):
    """Perform BFS for entire graph and return forest as a dictionary.

    Result maps each vertex v to the edge that was used to discover it.
    (vertices that are roots of a BFS tree are mapped to None).
    """
    forest = {}
    colore = {}#Il dizionario dei colori
    X = [] #I due sottoinisiemi di elementi, qui visti come liste
    Y = []
    for u in g.vertices():
        if u not in forest:
            forest[u] = None  # u will be a root of a tree
            NewBFS(g, u, forest, colore,X,Y)
    for e in g.edges():
        u, v = e.endpoints()
        if colore[u] == colore[v]:
            return forest,None
    return forest,(X,Y)


def bipartite(g):
    """Preso in input un grafo G non diretto, verifica se G è bipartito e restituisce una partizione (X, Y).
     Nel caso in cui il grafo non sia bipartito la funzione deve restituire None. """
    #Idea alla base dell'algoritmo. Un grafo è bipartito se l'insieme dei suoi vertici si può partizionare in
    # due sottoinsiemi tali che ogni vertice di una di queste due parti è collegato solo a vertici dell'altra.
    #I grafi bipartiti hanno un numero cromatico dei vertici uguale a 2. Questo vuol dire che il minimo numero di colori
    # necessari per colorare i vertici di G in modo che, presi comunque due vertici adiacenti in G, essi abbiano diverso colore è due.
    #Ad ogni iterazione dell'algoritmo BFS si visitano tutti i vertici adiacenti ad un altro. Quindi, quando si scopre un vertice x, gli si
    #associa il colore opposto a quello del vertice y da cui siamo partiti per scoprire x.
    #Una volta terminata la BFS ogni vertice avrà un colore, 0 o 1. A questo punto, se compare un arco che unisce due vertici dello stesso
    #colore allora questo corrisponde ad un arco che unisce due vertici sullo stesso livello e quindi il grafo non è bipartito.
    if not isinstance(g, Graph):
        raise TypeError('Graph expected')
    forest, partizione = NewBFS_complete(g)
    return partizione




def testBipartite():
    g = Graph()
    a = g.insert_vertex("A")
    b = g.insert_vertex("B")
    c = g.insert_vertex("C")
    d = g.insert_vertex("D")
    e = g.insert_vertex("E")
    g.insert_edge(a, b)
    g.insert_edge(b, c)
    g.insert_edge(c, d)
    g.insert_edge(d, e)
    g.insert_edge(b, e)
    #Se il comando seguente è commentato il grafo è bipartito, altrimenti non lo è
    #g.insert_edge(a, c)
    ##################
    #Gli inserimenti dei seguenti vertici e archi rendono il grafo non connesso
    m = g.insert_vertex("M")
    n = g.insert_vertex("N")
    o = g.insert_vertex("O")
    p = g.insert_vertex("P")
    q = g.insert_vertex("Q")
    g.insert_edge(m, n)
    g.insert_edge(n, o)
    g.insert_edge(o, p)
    g.insert_edge(p, q)
    g.insert_edge(n, q)

    partizione = bipartite(g)
    if partizione is not None:
        for e in partizione:
            i = 0
            while i < len(e):
                print(e[i])
                i += 1
            print("-------------")
    else:
        print(partizione)


if __name__ == "__main__":
    testBipartite()

