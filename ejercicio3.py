# Autores: Jose Alejandro Jimenez Vasquez, Felipe Castro, Nicolas Vasquez
# Fecha: 2024-08-09
# Versión: 1.0

import time
import tracemalloc

class Nodo:
    def __init__(self, estado, padre=None, accion=None):
        self.estado = estado
        self.padre = padre
        self.accion = accion

class Problema:
    def __init__(self, inicial, objetivo, grafo):
        self.inicial = inicial
        self.objetivo = objetivo
        self.grafo = grafo

    def acciones(self, estado):
        return self.grafo.get(estado, [])

    def resultado(self, estado, accion):
        return accion

    def es_objetivo(self, estado):
        return estado == self.objetivo

def busqueda_bfs(problema):
    nodo = Nodo(problema.inicial)
    if problema.es_objetivo(nodo.estado):
        return nodo
    frontera = [nodo]
    alcanzados = {problema.inicial}

    while frontera:
        nodo = frontera.pop(0)
        for accion in problema.acciones(nodo.estado):
            hijo = Nodo(accion, padre=nodo)
            if hijo.estado not in alcanzados:
                if problema.es_objetivo(hijo.estado):
                    return hijo
                alcanzados.add(hijo.estado)
                frontera.append(hijo)
    return None

def busqueda_dls(problema, limite):
    return busqueda_recursiva_dls(Nodo(problema.inicial), problema, limite)

def busqueda_recursiva_dls(nodo, problema, limite):
    if problema.es_objetivo(nodo.estado):
        return nodo
    elif limite == 0:
        return 'cutoff'
    else:
        cutoff_ocurrio = False
        for accion in problema.acciones(nodo.estado):
            hijo = Nodo(accion, padre=nodo)
            resultado = busqueda_recursiva_dls(hijo, problema, limite - 1)
            if resultado == 'cutoff':
                cutoff_ocurrio = True
            elif resultado is not None:
                return resultado
        return 'cutoff' if cutoff_ocurrio else None

def busqueda_ids(problema):
    for profundidad in range(1000):
        resultado = busqueda_dls(problema, profundidad)
        if resultado != 'cutoff':
            return resultado

def reconstruir_camino(nodo):
    camino = []
    while nodo:
        camino.append(nodo.estado)
        nodo = nodo.padre
    camino.reverse()
    return camino

mapa_metro = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B', 'G'],
    'E': ['B', 'H', 'I'],
    'F': ['C', 'J'],
    'G': ['D'],
    'H': ['E'],
    'I': ['E', 'J'],
    'J': ['F', 'I']
}

problema = Problema('A', 'J', mapa_metro)

# BFS
tracemalloc.start()
tiempo_inicio = time.time()
solucion_bfs = busqueda_bfs(problema)
tiempo_fin = time.time()
memoria_bfs = tracemalloc.get_traced_memory()
tracemalloc.stop()
camino_bfs = reconstruir_camino(solucion_bfs)

print("Camino BFS:", camino_bfs)
print("Tiempo BFS:", tiempo_fin - tiempo_inicio)
print("Memoria BFS:", memoria_bfs)

# IDS
tracemalloc.start()
tiempo_inicio = time.time()
solucion_ids = busqueda_ids(problema)
tiempo_fin = time.time()
memoria_ids = tracemalloc.get_traced_memory()
tracemalloc.stop()
camino_ids = reconstruir_camino(solucion_ids)

print("Camino IDS:", camino_ids)
print("Tiempo IDS:", tiempo_fin - tiempo_inicio)
print("Memoria IDS:", memoria_ids)