from __future__ import annotations
from typing import DefaultDict, List, Tuple
from ciudades import Ciudades


def __bsf(fuente: str,
          ciudades: Ciudades, ciudades_inv: Ciudades,
          flujos: DefaultDict):
    """
        devuelve un diccionario con todos los vértices accesibles 
        desde la fuente (sin la fuente) y las distancias desde la 
        fuente a cada uno.
    """
    from collections import deque, defaultdict

    cola = deque()
    visitados = set()  # sino, usar un defaultdict(lambda: False) para buscar en O(1)

    cola.append((fuente, 0))

    # {vertice: [distancia a vertice desde fuente, vertice_anterior] ...}
    distancias = defaultdict(lambda: (999, None))

    while (len(cola) != 0):
        u, distancia_actual = cola.popleft()
        visitados.add(u)

        distancia_actual += 1

        #vamos recorriendo el grafo de forma de  
        #un breadth first search pero teniendo en cuenta 
        #si un vertice dado es accesible desde la fuente
        #en el sentido de flujo de ida
        for v in ciudades.adyacencias[u]:
            if flujos[u, v] > 0:
                if v not in visitados:
                    cola.append((v, distancia_actual))
                    if distancias[v][0] > distancia_actual:
                        distancias[v] = distancia_actual, u
        #y lo repetimos en el sentido de vuelta
        for v in ciudades_inv.adyacencias[u]:
            if flujos[u, v] > 0:
                if v not in visitados:
                    cola.append((v, distancia_actual))
                    if distancias[v][0] > distancia_actual:
                        distancias[v] = distancia_actual, u
    return distancias


def breadthFirstSearch(fuente: str, sumidero: str,
                       ciudades: Ciudades, ciudades_inv: Ciudades,
                       flujos: DefaultDict) -> List[Tuple]:
    """
        Toma el grafo con adyacencias en el sentido directo y sentido 
        inverso y usa ambos para obtener el camino menor de `fuente` 
        a `sumidero`, teniendo en cuenta la capacidad (ie. si es 0 no 
        se puede ir por ahí).

        Devuelve una lista de pares de vertices en orden desde 
        fuente hasta sumidero (izquierda a derecha).

        Si no hay más caminos, devuelve `[]`.
    """
    distancias = __bsf(fuente, ciudades, ciudades_inv, flujos)

    camino = []
    vertice = sumidero
    if sumidero in distancias:  # si no esta, no hay caminos de aumento hasta `sumidero`
        for _ in distancias:
            if vertice == fuente:
                break
            vert_ant = distancias[vertice][1]
            camino.insert(0, (vert_ant, vertice))
            vertice = vert_ant

    return camino



def edmonds_karp(ciudades: Ciudades, capacidades: DefaultDict,
                 fuente: str, sumidero: str):
    from copy import deepcopy
    flujos = deepcopy(capacidades)  # evito efectos secundarios

    # creamos el grafo que va a contener las adyacencias inversas
    adyacencias_inv = DefaultDict(list)
    for u, v in ciudades.iterar():
        adyacencias_inv[v].append(u)
    ciud_inv = Ciudades(adyacencias_inv, ciudades.lista)

    camino_de_aumento = breadthFirstSearch(fuente, sumidero,
                                           ciudades, ciud_inv, flujos)

    while camino_de_aumento != []:

        # cuello de botella
        arista_cuello_bot = min(camino_de_aumento, key=lambda x: flujos[x])
        cuello_bot = flujos[arista_cuello_bot]

        # actualizamos flujos por cada arista del camino
        for u, v in camino_de_aumento:
            if v in ciudades.adyacencias[u]:  # (u,v) es en sentido de ida
                flujos[u, v] -= cuello_bot
                flujos[v, u] += cuello_bot
            else:                             # (u,v) es en sentido de vuelta
                flujos[u, v] += cuello_bot
                flujos[v, u] -= cuello_bot

        camino_de_aumento = breadthFirstSearch(fuente, sumidero,
                                               ciudades, ciud_inv, flujos)

    return flujos, ciud_inv


# PRE: el grafo ya esta reducido
def minCut(fuente: str, ciudades: Ciudades, ciudades_inv: Ciudades, flujos: DefaultDict):

    # contiene a los predecesores
    distancias = __bsf(fuente, ciudades, ciudades_inv, flujos)
    
    min_cut_set = set(distancias.keys())
    min_cut_set.add(fuente)
    return min_cut_set, ciudades.lista - min_cut_set
