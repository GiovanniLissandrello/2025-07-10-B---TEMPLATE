from model.model import Model

myModel = Model()
myModel.buildGraph("2016-01-01 00:00:00", "2018-12-28 00:00:00", 5)
nNodes, nEdges = myModel.getGraphDetails()
dizionario = myModel.getDizionario()
print(f"Num nodes: {nNodes}, num edges: {nEdges}")

# nodo1 = myModel.getNodes()
# print(nodo1[0].datetime.month, nodo1[0].datetime.day)

nodo = dizionario[186]
nodo2 = dizionario[193]


# cammino, score = myModel.getPath(nodo, nodo2, 5)
# if len(cammino) != 0 and score != 0:
#     for c in cammino:
#         print(c.product_name)
#     print(score)
# else:
#     print("cammino non trovato")
#
# print(score)

# cammino = myModel.getPercorsoLungo(myModel.idMap[150])
# for c in cammino:
#     print(c)
# best_5 = myModel.bestProduct()
# for b in best_5:
#     print(f"{b[0]} - {b[1]}")
#
# nodi = myModel.getNodiCompleti()
# percorso, score= myModel.getPath(nodi[0], nodi[5], 6)
# print(score)
# for p in percorso:
#     print(p.product_name)