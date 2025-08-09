# Autores: Jose Alejandro Jimenez Vasquez, Felipe Castro, Nicolas Vasquez
# Fecha: 2024-08-09
# Versión: 1.0

import heapq

class Nodo:
    def __init__(self, estado, padre=None, accion=None, costo_camino=0):
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.costo_camino = costo_camino
        self.costo_heuristico = 0

    def __lt__(self, otro):
        return (self.costo_camino + self.costo_heuristico) < (otro.costo_camino + otro.costo_heuristico)

class Problema:
    def __init__(self, inicial, objetivo, acciones, resultado, costo_accion, es_objetivo, heuristica):
        self.inicial = inicial
        self.objetivo = objetivo
        self.acciones = acciones
        self.resultado = resultado
        self.costo_accion = costo_accion
        self.es_objetivo = es_objetivo
        self.heuristica = heuristica

def expandir(problema, nodo):
    hijos = []
    for accion in problema.acciones(nodo.estado):
        estado_resultado = problema.resultado(nodo.estado, accion)
        costo = nodo.costo_camino + problema.costo_accion(nodo.estado, accion, estado_resultado)
        nodo_hijo = Nodo(estado=estado_resultado, padre=nodo, accion=accion, costo_camino=costo)
        nodo_hijo.costo_heuristico = problema.heuristica(estado_resultado)
        hijos.append(nodo_hijo)
    return hijos

def busqueda_a_estrella(problema):
    nodo = Nodo(estado=problema.inicial)
    nodo.costo_heuristico = problema.heuristica(nodo.estado)
    frontera = [(nodo.costo_camino + nodo.costo_heuristico, nodo)]
    heapq.heapify(frontera)
    alcanzados = {problema.inicial: nodo}

    while frontera:
        _, nodo = heapq.heappop(frontera)
        if problema.es_objetivo(nodo.estado):
            return nodo

        for hijo in expandir(problema, nodo):
            s = hijo.estado
            if s not in alcanzados or hijo.costo_camino < alcanzados[s].costo_camino:
                alcanzados[s] = hijo
                heapq.heappush(frontera, (hijo.costo_camino + hijo.costo_heuristico, hijo))

    return None

mapa_rumania = {
    'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
    'Bucharest': {'Urziceni': 85, 'Pitesti': 101, 'Giurgiu': 90, 'Fagaras': 211},
    'Craiova': {'Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
    'Drobeta': {'Mehadia': 75, 'Craiova': 120},
    'Eforie': {'Hirsova': 86},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Giurgiu': {'Bucharest': 90},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Neamt': {'Iasi': 87},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
    'Rimnicu Vilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Urziceni': {'Bucharest': 85, 'Hirsova': 98, 'Vaslui': 142},
    'Vaslui': {'Iasi': 92, 'Urziceni': 142},
    'Zerind': {'Arad': 75, 'Oradea': 71}
}

heuristica = {
    'Arad': 366,
    'Bucharest': 0,
    'Craiova': 160,
    'Drobeta': 242,
    'Eforie': 161,
    'Fagaras': 176,
    'Giurgiu': 77,
    'Hirsova': 151,
    'Iasi': 226,
    'Lugoj': 244,
    'Mehadia': 241,
    'Neamt': 234,
    'Oradea': 380,
    'Pitesti': 100,
    'Rimnicu Vilcea': 193,
    'Sibiu': 253,
    'Timisoara': 329,
    'Urziceni': 80,
    'Vaslui': 199,
    'Zerind': 374
}

def resultado(estado, accion):
    return accion

def costo_accion(estado, accion, resultado):
    return mapa_rumania[estado][accion]

def es_objetivo(estado):
    return estado == 'Bucharest'

def obtener_acciones(estado):
    return list(mapa_rumania.get(estado, {}).keys())

def obtener_heuristica(estado):
    return heuristica.get(estado, float('inf'))

problema = Problema(
    inicial='Arad',
    objetivo='Bucharest',
    acciones=obtener_acciones,
    resultado=resultado,
    costo_accion=costo_accion,
    es_objetivo=es_objetivo,
    heuristica=obtener_heuristica
)

solucion = busqueda_a_estrella(problema)

if solucion:
    camino = []
    while solucion:
        camino.append(solucion.estado)
        solucion = solucion.padre
    camino.reverse()
    print("Camino de la solucion:", camino)
else:
    print("No se encontro solucion")