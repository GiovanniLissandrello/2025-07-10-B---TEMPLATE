import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}

    def buildGraph(self, anno1, anno2, idcategoria):

        nodi = DAO.getAllNodes(idcategoria)
        self._graph.add_nodes_from(nodi)

        for nodo in nodi:
            self._idMap[nodo.product_id] = nodo

        archi = DAO.getAllArchi(anno1, anno2, idcategoria, self._idMap)
        for arco in archi:
            self._graph.add_edge(arco.u, arco.v, weight = arco.peso)

    def getPiuVenduti(self):

         classifica = []
         for nodo in list(self._graph.nodes()):

            archi_uscenti = list(self._graph.out_edges(nodo, data = True))
            archi_entranti = list(self._graph.in_edges(nodo, data = True))

            tot_u = 0
            tot_e = 0
            for u,v,peso in archi_uscenti:
                tot_u += self._graph[u][v]["weight"]

            for u,v,peso in archi_entranti:
                tot_e += self._graph[u][v]["weight"]

            differenza = tot_e-tot_u

            classifica.append((nodo, differenza))

         classifica.sort(key = lambda x: x[1], reverse = True)
         top_5 = classifica[:5]

         return top_5

    def getPath(self, source, end, lun):

        self._bestPath = []
        self._score = 0

        parziale = [source]

        if lun > len(list(self._graph.nodes())):
            return [],0

        lista_vicini = list(self._graph.out_edges(source, data = True))
        lista_vicini.sort(key=lambda x: x[2]["weight"], reverse=True)
        for _,v,peso in lista_vicini:
            if v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale, end, lun)
                parziale.pop()

        return self._bestPath, self._score

    def _ricorsione(self, parziale, end, lun):

        if parziale[-1] == end:
            if len(parziale) == lun and self._getScore(parziale) > self._score:
                    self._bestPath = copy.deepcopy(parziale)
                    self._score = self._getScore(parziale)
                    return

            self._bestPath = []
            self._score = 0
            return

        lista_vicini = list(self._graph.out_edges(parziale[-1], data=True))
        lista_vicini.sort(key = lambda x: x[2]["weight"], reverse = True)
        for _, v, peso in lista_vicini:
            if v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale, end, lun)
                parziale.pop()

    def _getScore(self, parziale):

        tot = 0
        for i in range(0, len(parziale)-1):
            tot += self._graph[parziale[i]][parziale[i+1]]["weight"]

        return tot


    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategorie(self):
        return DAO.getAllCategorie()

    def getDizionario(self):
        return self._idMap

    def getNodes(self):
        return self._graph.nodes()