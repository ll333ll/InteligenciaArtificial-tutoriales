# Autores: Jose Alejandro Jimenez Vasquez, Felipe Castro, Nicolas Vasquez
# Fecha: 2024-08-09
# Versión: 1.0

import heapq

class Nodo:
    def __init__(self, posicion, padre=None, accion=None, costo_camino=0):
        self.posicion = posicion
        self.padre = padre
        self.accion = accion
        self.costo_camino = costo_camino

    def __lt__(self, otro):
        return self.costo_camino < otro.costo_camino

class Problema:
    def __init__(self, inicial, objetivo, acciones, resultado, costo_accion, es_objetivo):
        self.inicial = inicial
        self.objetivo = objetivo
        self.acciones = acciones
        self.resultado = resultado
        self.costo_accion = costo_accion
        self.es_objetivo = es_objetivo

def encontrar_salida(laberinto, inicial, objetivo, funcion_costo):
    acciones = {
        'Arriba': (-1, 0),
        'Abajo': (1, 0),
        'Izquierda': (0, -1),
        'Derecha': (0, 1)
    }

    def resultado(estado, accion):
        return (estado[0] + acciones[accion][0], estado[1] + acciones[accion][1])

    def costo_accion(estado, accion, resultado):
        return funcion_costo(resultado)

    def es_objetivo(estado):
        return estado == objetivo

    def obtener_acciones(estado):
        acciones_posibles = []
        for accion in acciones:
            nueva_pos = resultado(estado, accion)
            if 0 <= nueva_pos[0] < len(laberinto) and 0 <= nueva_pos[1] < len(laberinto[0]) and laberinto[nueva_pos[0]][nueva_pos[1]] != '#':
                acciones_posibles.append(accion)
        return acciones_posibles

    problema = Problema(
        inicial=inicial,
        objetivo=objetivo,
        acciones=obtener_acciones,
        resultado=resultado,
        costo_accion=costo_accion,
        es_objetivo=es_objetivo
    )

    def distancia_manhattan(pos, objetivo):
        return abs(pos[0] - objetivo[0]) + abs(pos[1] - objetivo[1])

    nodo_inicial = Nodo(problema.inicial, costo_camino=0)
    frontera = [(distancia_manhattan(problema.inicial, problema.objetivo), nodo_inicial)]
    heapq.heapify(frontera)
    alcanzados = {problema.inicial: nodo_inicial}

    while frontera:
        _, nodo = heapq.heappop(frontera)

        if problema.es_objetivo(nodo.posicion):
            return reconstruir_camino(nodo)

        for accion in problema.acciones(nodo.posicion):
            pos_vecino = problema.resultado(nodo.posicion, accion)
            nuevo_costo = nodo.costo_camino + problema.costo_accion(nodo.posicion, accion, pos_vecino)
            
            if pos_vecino not in alcanzados or nuevo_costo < alcanzados[pos_vecino].costo_camino:
                nodo_vecino = Nodo(pos_vecino, padre=nodo, accion=accion, costo_camino=nuevo_costo)
                alcanzados[pos_vecino] = nodo_vecino
                heapq.heappush(frontera, (nuevo_costo + distancia_manhattan(pos_vecino, problema.objetivo), nodo_vecino))

    return None

def reconstruir_camino(nodo):
    camino = []
    acciones = []
    while nodo.padre:
        camino.append(nodo.posicion)
        acciones.append(nodo.accion)
        nodo = nodo.padre
    camino.append(nodo.posicion)
    camino.reverse()
    acciones.reverse()
    return camino, acciones

# Laberinto Original
laberinto1 = [
    ['#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', 'S', ' ', ' ', '#', ' ', 'E', '#'],
    ['#', ' ', '#', ' ', '#', ' ', ' ', '#'],
    ['#', ' ', '#', ' ', ' ', ' ', '#', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#']
]

inicio1 = (1, 1)
fin1 = (1, 6)

def costo_estandar(pos):
    return 1

camino1, acciones1 = encontrar_salida(laberinto1, inicio1, fin1, costo_estandar)
print("Camino del Laberinto Original:", camino1)
print("Acciones del Laberinto Original:", acciones1)

# Laberinto Modificado
laberinto2 = [
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', 'S', ' ', '#', ' ', 'A', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', '#', ' ', '#', '#', '#', '#', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#'],
    ['#', '#', '#', '#', '#', 'A', '#', '#', ' ', '#', 'E', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
]

inicio2 = (1, 1)
fin2 = (4, 10)

def costo_agua(pos):
    if laberinto2[pos[0]][pos[1]] == 'A':
        return 5 # Costo más alto por pasar por agua
    return 1

camino2, acciones2 = encontrar_salida(laberinto2, inicio2, fin2, costo_agua)
print("Camino del Laberinto Modificado:", camino2)
print("Acciones del Laberinto Modificado:", acciones2)