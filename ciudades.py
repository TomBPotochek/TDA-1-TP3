from dataclasses import dataclass
from typing import DefaultDict, Dict, List, Tuple, Set, Iterable

@dataclass
class Ciudades:
    """el grafo de ciudades por lista de adyacencias 
    y total de ciudades"""
    adyacencias: DefaultDict[str, List[str]]
    lista: Set[str]

    def iterar(self):
        """generador para iterar las ciudades 
        siguiendo las adyacencias"""
        for u in self.adyacencias:
            for v in self.adyacencias[u]:
                yield u, v
