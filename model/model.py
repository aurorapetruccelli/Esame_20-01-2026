import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []

        self._artist_list_min = []
        self._artists_coppie = []
        self.dizionario_artisti = {}
        self.node = []
        self.edges = []

        self.artisti_durata = []
        self.load_all_artists()


    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, min_albums):
        self._artists_list_min = DAO.get_artists(min_albums)
        return self._artists_list

    def build_graph(self,min_albums):
        self._graph.clear()
        for a in self._artists_list:
            self.dizionario_artisti[a.id]=a.name

        self._artists_list_min = DAO.get_artists(min_albums)
        for a in self._artists_list_min:
            self._graph.add_node(a[0])
            self.node.append(a[0])

        self._artists_coppie = DAO.get_artists_coppie()
        for a1,a2,peso in self._artists_coppie:
            if a1 in self.node and a2 in self.node:
                self.edges.append((a1,a2,peso))

        self._graph.add_weighted_edges_from(self.edges)
        print(self.edges)
        print(self._graph)
        print(self._graph)

    def connected_artists(self,a1):
        lista_artisti = []
        connessi = nx.node_connected_component(self._graph,a1)
        for c in connessi:
            if c!=a1:
                lista_artisti.append((c,self.dizionario_artisti[c],self._graph[a1][c]["weight"]))

        print(sorted(lista_artisti))
        return sorted(lista_artisti)



    def ricerca(self,nodo,lunghezza,durata_min):
        self.artisti_durata = DAO.get_artisti_min_canzoni(durata_min)
        self.peso_migliore = 0
        self.cammino_migliore = []

        self.ricorsione([nodo],lunghezza,0)

        print(self.peso_migliore)
        print(self.cammino_migliore)
        return self.peso_migliore,self.cammino_migliore

    def ricorsione(self,partial_node,lunghezza,peso):
        ultimo_nodo = partial_node[-1]

        if len(partial_node)== lunghezza and peso> self.peso_migliore:
            self.peso_migliore = peso
            self.cammino_migliore = partial_node.copy()

        for v in self._graph.neighbors(ultimo_nodo):
            if v in self.artisti_durata and v not in partial_node:
                partial_node.append(v)
                self.ricorsione(partial_node,lunghezza,peso+self._graph[ultimo_nodo][v]["weight"])
                partial_node.pop()
