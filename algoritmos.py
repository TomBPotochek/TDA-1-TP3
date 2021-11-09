from typing import DefaultDict, List, Tuple
from ciudades import Ciudades


def breadthFirstSearch(fuente: str, sumidero: str,
                        ciudades: Ciudades, ciudades_inv: Ciudades, 
                         capacidades: DefaultDict) -> List[Tuple, ...]:
    """
        Toma el grafo con adyacencias en el sentido directo y sentido 
        inverso y usa ambos para obtener el camino menor de `fuente` 
        a `sumidero`, teniendo en cuenta la capacidad (ie. si es 0 no 
        se puede ir por ahí).

        Devuelve una lista de pares de vertices en orden desde 
        fuente hasta sumidero (izquierda a derecha).

        Si no hay más caminos, devuelve `None`.
    """
    
    from collections import deque, defaultdict

    cola = deque()
    visitados = set() # sino, usar un defaultdict(lambda: False) para buscar en O(1)
    distancia_total = 9999 # asumo que eso es mayor a cualquier distancia en el grafo

    cola.append(fuente)
    visitados.add(fuente)

    camino = []
    camino_final = []

    while (len(cola) != 0):
        u = cola.popleft()

        for v in ciudades.adyacencias[u]:
            if capacidades[u,v] > 0:
                if v not in visitados:
                    cola.append(v)
                    camino.append((u,v))
                    




                                    # nombre: flujos en vez de capacidades?
def edmonds_karp(ciudades: Ciudades, capacidades: DefaultDict,
                 fuente: str, sumidero: str):
    
    # creamos el grafo que va a contener las adyacencias inversas
    adyacencias_inv = DefaultDict(list)
    for u,v in ciudades.iterar():
        adyacencias_inv[v].append(u)
    ciud_inv = Ciudades(adyacencias_inv, ciudades.lista)

    camino_de_aumento = breadthFirstSearch(fuente, sumidero,
                                 ciudades, ciud_inv, capacidades)

    while camino_de_aumento is not None:
        
        #cuello de botella
        cuello_bot = min(camino_de_aumento, key=lambda x: capacidades[x])
        for u,v in camino_de_aumento:
            if v in ciudades.adyacencias[u]: # (u,v) esta en el grafo original
                capacidades[u,v] -= cuello_bot
            else:
                capacidades[u,v] += cuello_bot
    
    # TODO: duplicar capacidades para evitar efectos secundarios?
    return capacidades, ciud_inv

def minCut(fuente: str, ciudades: Ciudades, ciudades_inv: Ciudades, flujos: DefaultDict):
    min_cut = set()

    vertice_actual = fuente
    min_cut.add(vertice_actual)
    while True: #algo, no se aun
        for v in ciudades.adyacencias[vertice_actual]:
            if flujos[vertice_actual, v] > 0:
                if v not in min_cut:
                    min_cut.add(v)
            



    
