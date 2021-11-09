from __future__ import annotations
from ciudades import Ciudades
path = str
from typing import DefaultDict, Dict, List, Tuple


def parse_file(listado_ciudades: path) -> Tuple[Ciudades, DefaultDict, Tuple[str, str]]:
    from csv import reader
    from collections import defaultdict

    matriz_capacidades = defaultdict(lambda: 0)
    grafo_ciudades = defaultdict(list)
    total_ciudades = set()

    with open(listado_ciudades, "r") as depositos_csv:
        filas = reader(depositos_csv, delimiter=',')

    # primeras 2 lineas, la fuente y sumidero
    # operador magico ,= (es simplemente desempaquetado de tuplas, no un operador)
        ciud_s ,= next(filas)
        ciud_t ,= next(filas)

        for a, b, capacidad in filas:
            capacidad = int(capacidad)
            grafo_ciudades[a].append(b)
            matriz_capacidades[a, b] = capacidad
            total_ciudades |= {a, b}
    return Ciudades(grafo_ciudades, total_ciudades),  matriz_capacidades, (ciud_s, ciud_t)



if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description=('Determina los trayectos simples donde '
                                         'poner publicidad de forma de alcanzar '
                                         'todas las personas que tienen destino '
                                         'inicial A y final B, con la menor cantidad '
                                         'de vuelos comerciales.'))

    parser.add_argument('archivo', metavar='archivo.txt', type=str,
                        help=('path al archivo que contiene la información '
                              'sobre los vuelos disponibles entre pares de ciudades '
                              'y la cantidad maxima de pasajeros en la misma.\n'
                              'Las primeras 2 linas deben contener el país de origen y destino.'))

    args = parser.parse_args()