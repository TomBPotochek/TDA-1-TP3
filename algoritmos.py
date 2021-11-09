from typing import DefaultDict, List, Tuple
from ciudades import Ciudades


def __bsf(fuente: str,
            ciudades: Ciudades, ciudades_inv: Ciudades, 
                capacidades: DefaultDict):
    from collections import deque, defaultdict

    cola = deque()
    visitados = set() # sino, usar un defaultdict(lambda: False) para buscar en O(1)

    cola.append((fuente,0))

    distancias = defaultdict(lambda: (999, None)) # {vertice: [distancia a vertice desde fuente, vertice_anterior] ...}

    while (len(cola) != 0):
        u, distancia_actual = cola.popleft()
        visitados.add(u)

        distancia_actual += 1
        for v in ciudades.adyacencias[u]:
            if capacidades[u,v] > 0:
                if v not in visitados:
                    cola.append((v, distancia_actual))
                    if distancias[v][0] > distancia_actual:
                        distancias[v] = distancia_actual, u
        
        for v in ciudades_inv.adyacencias[u]:
            if capacidades[u,v] > 0:
                if v not in visitados:
                    cola.append((v, distancia_actual))
                    if distancias[v][0] > distancia_actual:
                        distancias[v] = distancia_actual, u
    return distancias

def breadthFirstSearch(fuente: str, sumidero: str,
                        ciudades: Ciudades, ciudades_inv: Ciudades, 
                         capacidades: DefaultDict) -> List[Tuple]:
    """
        Toma el grafo con adyacencias en el sentido directo y sentido 
        inverso y usa ambos para obtener el camino menor de `fuente` 
        a `sumidero`, teniendo en cuenta la capacidad (ie. si es 0 no 
        se puede ir por ahí).

        Devuelve una lista de pares de vertices en orden desde 
        fuente hasta sumidero (izquierda a derecha).

        Si no hay más caminos, devuelve `[]`.
    """
    distancias = __bsf(fuente, ciudades, ciudades_inv, capacidades)
        
    camino = []
    vertice = sumidero
    if sumidero in distancias: # si no esta, no hay caminos de aumento hasta `sumidero`
        for _ in distancias:
            if vertice == fuente:
                break
            vert_ant = distancias[vertice][1]
            camino.insert(0, (vert_ant, vertice))
            vertice = vert_ant

    return camino

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

    while camino_de_aumento != []:
        
        #cuello de botella
        arista_cuello_bot = min(camino_de_aumento, key=lambda x: capacidades[x])
        cuello_bot = capacidades[arista_cuello_bot]
        for u,v in camino_de_aumento:
            if v in ciudades.adyacencias[u]: # (u,v) esta en el grafo original
                capacidades[u,v] -= cuello_bot
                capacidades[v,u] += cuello_bot
            else:
                capacidades[u,v] += cuello_bot
                capacidades[v,u] -= cuello_bot

        camino_de_aumento = breadthFirstSearch(fuente, sumidero,
                                    ciudades, ciud_inv, capacidades)
    
    # TODO: duplicar capacidades para evitar efectos secundarios?
    return capacidades, ciud_inv

def minCut(fuente: str, ciudades: Ciudades, ciudades_inv: Ciudades, flujos: DefaultDict):
    # asumo que el grafo ya esta reducido

    # contiene a los predecesores
    distancias = __bsf(fuente, ciudades, ciudades_inv, flujos)
    min_cut_set = set(distancias.keys())
    min_cut_set.add(fuente)
    return min_cut_set, ciudades.lista - min_cut_set


            



    
