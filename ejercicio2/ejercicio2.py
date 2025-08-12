#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROBLEMA DEL MAZE - SOLUCIÓN CON A*
Estudiante: [Tu nombre]
Fecha: 2025
"""

# ============================================
# CELDA 1: IMPORTACIONES
# ============================================
import heapq
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Optional
import time

# ============================================
# CELDA 2: DEFINICIÓN DEL PROBLEMA (ESTRUCTURA)
# ============================================

class MazeProblem:
    """
    Estructura del problema del laberinto.
    Define el espacio de estados y las operaciones básicas.
    """

    def __init__(self, maze: List[List[str]], heuristic: str = 'manhattan'):
        """
        Inicializa el problema del laberinto.

        Args:
            maze: Matriz representando el laberinto
            heuristic: 'manhattan' o 'euclidean'
        """
        self.maze = maze
        self.heuristic = heuristic

        # Encontrar posicion inicial y salida(s)
        self.start = None
        self.goals = []  # Lista para manejar multiples salidas

        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == 'S':
                    self.start = (i, j)
                elif maze[i][j] == 'E':
                    self.goals.append((i, j))

    # ============================================
    # FUNCIONES PRINCIPALES DEL PROBLEMA
    # ============================================

    def actions(self, state: Tuple[int, int]) -> List[str]:
        """
        FUNCIÓN 1: ACTIONS
        Retorna las acciones válidas desde un estado.
        Movimientos: UP, DOWN, LEFT, RIGHT (sin diagonales)
        """
        row, col = state
        valid_actions = []

        # Verificar cada dirección
        if row > 0 and self.maze[row-1][col] != '#':
            valid_actions.append('UP')
        if row < len(self.maze)-1 and self.maze[row+1][col] != '#':
            valid_actions.append('DOWN')
        if col > 0 and self.maze[row][col-1] != '#':
            valid_actions.append('LEFT')
        if col < len(self.maze[0])-1 and self.maze[row][col+1] != '#':
            valid_actions.append('RIGHT')

        return valid_actions

    def result(self, state: Tuple[int, int], action: str) -> Tuple[int, int]:
        """
        FUNCIÓN 2: RESULT
        Retorna el nuevo estado después de aplicar una acción.
        Cambia la posición (x,y) del robot.
        """
        row, col = state

        if action == 'UP':
            return (row - 1, col)
        elif action == 'DOWN':
            return (row + 1, col)
        elif action == 'LEFT':
            return (row, col - 1)
        elif action == 'RIGHT':
            return (row, col + 1)

        return state

    def action_cost(self, state: Tuple[int, int], action: str,
                   next_state: Tuple[int, int]) -> float:
        """
        FUNCIÓN 3: ACTION-COST
        Retorna el costo de una acción.
        Costo base: 1 para todos los movimientos
        Modificable para diferentes tipos de terreno.
        """
        # Costo uniforme base
        cost = 1

        # MODIFICACIÓN: Si hay obstáculos 'O', tienen mayor costo
        row, col = next_state
        if self.maze[row][col] == 'O':
            cost = 3  # Los obstáculos cuestan más atravesar

        return cost

    def is_goal(self, state: Tuple[int, int]) -> bool:
        """Verifica si el estado actual corresponde a una salida del laberinto"""
        return state in self.goals

    # ============================================
    # FUNCIONES HEURÍSTICAS
    # ============================================

    def manhattan_distance(self, state: Tuple[int, int]) -> float:
        """
        Calcula la distancia Manhattan entre el estado actual y las salidas.
        Esta heuristica es optima para movimientos ortogonales (arriba, abajo, izquierda, derecha).
        Formula: |x1-x2| + |y1-y2|
        """
        # Calcular distancia a la salida mas cercana
        min_distance = float('inf')
        for goal in self.goals:
            distance = abs(state[0] - goal[0]) + abs(state[1] - goal[1])
            min_distance = min(min_distance, distance)
        return min_distance

    def euclidean_distance(self, state: Tuple[int, int]) -> float:
        """
        Calcula la distancia euclidiana entre el estado actual y las salidas.
        Esta heuristica representa la distancia en linea recta.
        Formula: sqrt((x1-x2)^2 + (y1-y2)^2)
        """
        min_distance = float('inf')
        for goal in self.goals:
            distance = ((state[0] - goal[0])**2 + (state[1] - goal[1])**2)**0.5
            min_distance = min(min_distance, distance)
        return min_distance

    def h(self, state: Tuple[int, int]) -> float:
        """Retorna el valor heuristico segun la configuracion seleccionada"""
        if self.heuristic == 'manhattan':
            return self.manhattan_distance(state)
        elif self.heuristic == 'euclidean':
            return self.euclidean_distance(state)
        else:
            return 0

# ============================================
# CELDA 3: ALGORITMO A*
# ============================================

def a_star_search(problem: MazeProblem) -> Dict:
    """
    Implementacion completa del algoritmo A*.
    
    El algoritmo utiliza una cola de prioridad para explorar estados,
    priorizando aquellos con menor funcion f(n) = g(n) + h(n).
    
    Returns:
        Dict con informacion de la solucion encontrada o None si no existe solucion
    """
    start_time = time.time()

    # Cola de prioridad: (f_score, estado)
    frontier = [(0, problem.start)]
    heapq.heapify(frontier)

    # Diccionarios para el algoritmo
    came_from = {}
    g_score = {problem.start: 0}
    f_score = {problem.start: problem.h(problem.start)}
    visited = set()

    nodes_explored = 0

    while frontier:
        current_f, current = heapq.heappop(frontier)

        if current in visited:
            continue

        visited.add(current)
        nodes_explored += 1

        # Verificar si el estado actual es una salida del laberinto
        if problem.is_goal(current):
            # Reconstruir el camino
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(problem.start)
            path.reverse()

            return {
                'path': path,
                'cost': g_score[path[-1]],
                'nodes_explored': nodes_explored,
                'time': time.time() - start_time,
                'visited': visited
            }

        # Explorar vecinos
        for action in problem.actions(current):
            neighbor = problem.result(current, action)

            tentative_g = g_score[current] + problem.action_cost(current, action, neighbor)

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + problem.h(neighbor)
                f_score[neighbor] = f
                heapq.heappush(frontier, (f, neighbor))

    return None  # No se encontró solución

# ============================================
# CELDA 4: VISUALIZACIÓN
# ============================================

def visualize_solution(maze: List[List[str]], solution: Dict, title: str = ""):
    """Visualiza el laberinto original y la solucion encontrada por A*"""

    # Crear copia del laberinto para visualización
    visual_maze = [row[:] for row in maze]

    if solution:
        # Marcar celdas visitadas
        for pos in solution['visited']:
            if visual_maze[pos[0]][pos[1]] == ' ':
                visual_maze[pos[0]][pos[1]] = '.'
        # Marcar el camino
        for pos in solution['path'][1:-1]:  # Excluir inicio y fin
            if visual_maze[pos[0]][pos[1]] in [' ', '.']:
                visual_maze[pos[0]][pos[1]] = '*'

    # Funcion auxiliar para convertir representacion de caracteres a matriz numerica
    def maze_to_array(maze_grid):
        rows, cols = len(maze_grid), len(maze_grid[0])
        array = np.zeros((rows, cols))
        for i in range(rows):
            for j in range(cols):
                if maze_grid[i][j] == '#':
                    array[i][j] = 0  # Pared
                elif maze_grid[i][j] == 'S':
                    array[i][j] = 1  # Inicio
                elif maze_grid[i][j] == 'E':
                    array[i][j] = 2  # Fin
                elif maze_grid[i][j] == 'O':
                    array[i][j] = 3  # Obstáculo
                elif maze_grid[i][j] == '*':
                    array[i][j] = 4  # Camino solución
                elif maze_grid[i][j] == '.':
                    array[i][j] = 5  # Visitado
                else:
                    array[i][j] = 6  # Vacío
        return array

    # Crear figura con dos subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Colores personalizados
    from matplotlib.colors import ListedColormap
    colors = ['#2C2C2C',  # 0: Pared - Gris oscuro
              '#00FF00',  # 1: Inicio - Verde brillante
              '#FF0000',  # 2: Fin - Rojo
              '#FFA500',  # 3: Obstáculo - Naranja
              '#FFD700',  # 4: Camino - Dorado
              '#87CEEB',  # 5: Visitado - Azul cielo
              '#FFFFFF']  # 6: Vacío - Blanco
    cmap = ListedColormap(colors)

    # ANTES - Laberinto original
    maze_before = maze_to_array(maze)
    im1 = ax1.imshow(maze_before, cmap=cmap, interpolation='nearest')
    ax1.set_title('ANTES - Laberinto Original', fontsize=12, fontweight='bold')
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.grid(True, alpha=0.3, linewidth=0.5)

    # DESPUÉS - Laberinto con solución
    maze_after = maze_to_array(visual_maze)
    im2 = ax2.imshow(maze_after, cmap=cmap, interpolation='nearest')
    ax2.set_title(f'DESPUÉS - Solución {title}', fontsize=12, fontweight='bold')
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.grid(True, alpha=0.3, linewidth=0.5)

    # Crear leyenda con cuadros de colores
    from matplotlib.patches import Rectangle
    legend_elements = [
        Rectangle((0,0),1,1, fc='#2C2C2C', label='■ Pared'),
        Rectangle((0,0),1,1, fc='#00FF00', label='■ S - Inicio'),
        Rectangle((0,0),1,1, fc='#FF0000', label='■ E - Salida'),
        Rectangle((0,0),1,1, fc='#FFD700', label='■ Camino'),
        Rectangle((0,0),1,1, fc='#87CEEB', label='■ Visitado'),
        Rectangle((0,0),1,1, fc='#FFFFFF', ec='black', label='□ Vacío')
    ]

    # Si hay obstáculos, agregar a la leyenda
    if any('O' in row for row in maze):
        legend_elements.insert(3, Rectangle((0,0),1,1, fc='#FFA500', label='■ O - Obstáculo'))

    # Colocar leyenda en el centro entre las dos imágenes
    fig.legend(handles=legend_elements, loc='center', bbox_to_anchor=(0.5, -0.05),
               ncol=len(legend_elements), frameon=True, fontsize=10)

    plt.suptitle(f'Algoritmo A* - Visualización del Laberinto', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

    if solution:
        print(f"\nSOLUCION ENCONTRADA:")
        print(f"   - Longitud del camino: {len(solution['path'])} pasos")
        print(f"   - Costo total: {solution['cost']}")
        print(f"   - Nodos explorados: {solution['nodes_explored']}")
        print(f"   - Tiempo de ejecución: {solution['time']:.4f} segundos")
        print(f"   - Eficiencia: {len(solution['path'])/solution['nodes_explored']*100:.1f}%")
    else:
        print("No se encontró solución")

# ============================================
# CELDA 5: EXPERIMENTOS Y ANÁLISIS
# ============================================

# LABERINTO ORIGINAL
maze_original = [
    ["#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", "S", "#", " ", "#", " ", "E", "#"],
    ["#", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#"]
]

print("="*50)
print("1. LABERINTO ORIGINAL - SOLUCIÓN BASE")
print("="*50)

# Resolver con Manhattan
problem1 = MazeProblem(maze_original, 'manhattan')
solution1 = a_star_search(problem1)
visualize_solution(maze_original, solution1, "- Heurística Manhattan")

# Resolver con Euclidiana
problem2 = MazeProblem(maze_original, 'euclidean')
solution2 = a_star_search(problem2)
visualize_solution(maze_original, solution2, "- Heurística Euclidiana")

# ============================================
# CELDA 6: ANÁLISIS DE CAMBIO DE FUNCIÓN DE COSTO
# ============================================

print("\n" + "="*50)
print("2. ANÁLISIS: CAMBIO DE FUNCIÓN DE COSTO")
print("="*50)

# Laberinto con obstáculos (O)
maze_obstacles = [
    ["#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", "S", " ", "O", " ", " ", "E", "#"],
    ["#", " ", "#", "#", "#", "O", " ", "#"],
    ["#", " ", " ", "O", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#"]
]

print("\nComparación de costos:")
print("   - Espacio vacío (' '): costo = 1")
print("   - Obstáculo ('O'): costo = 3")

problem_obs = MazeProblem(maze_obstacles, 'manhattan')
solution_obs = a_star_search(problem_obs)
visualize_solution(maze_obstacles, solution_obs, "- Con Obstáculos")

print("""
OBSERVACION: Con funcion de costo modificada, el algoritmo
prefiere rodear los obstaculos cuando es posible, ya que
atravesarlos tiene mayor costo (3 vs 1).
""")

# ============================================
# CELDA 7: MÚLTIPLES SALIDAS
# ============================================

print("\n" + "="*50)
print("3. ANÁLISIS: MÚLTIPLES SALIDAS")
print("="*50)

maze_multi_exit = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", "S", " ", " ", "#", " ", "E", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", " ", " ", "#"],
    ["#", " ", " ", " ", "#", "#", "#", "E", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#"]
]

problem_multi = MazeProblem(maze_multi_exit, 'manhattan')
solution_multi = a_star_search(problem_multi)
visualize_solution(maze_multi_exit, solution_multi, "- Múltiples Salidas")

print("""
OBSERVACION: El algoritmo encuentra automaticamente la salida
mas cercana gracias a la heuristica que calcula la distancia
minima a cualquier salida disponible.
""")

# ============================================
# CELDA 8: LABERINTO MÁS GRANDE
# ============================================

print("\n" + "="*50)
print("4. LABERINTO MÁS GRANDE Y COMPLEJO")
print("="*50)

maze_large = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", "S", " ", " ", "#", " ", " ", " ", " ", " ", "E", "#"],
    ["#", "#", "#", " ", "#", " ", "#", "#", "#", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#", " ", "#", "#"],
    ["#", " ", "#", "#", "#", "#", "#", " ", "#", " ", " ", "#"],
    ["#", " ", " ", " ", "O", "O", " ", " ", " ", " ", "#", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
]

problem_large = MazeProblem(maze_large, 'manhattan')
solution_large = a_star_search(problem_large)
visualize_solution(maze_large, solution_large, "- Laberinto Grande")

# ============================================
# CELDA 9: COMPARACIÓN DE COMPORTAMIENTO
# ============================================

print("\n" + "="*50)
print("5. COMPARACIÓN DE HEURÍSTICAS")
print("="*50)

def compare_heuristics(maze, maze_name):
    """Compara el rendimiento computacional de las heuristicas Manhattan y Euclidiana"""
    print(f"\n{maze_name}:")

    for heuristic in ['manhattan', 'euclidean']:
        problem = MazeProblem(maze, heuristic)
        solution = a_star_search(problem)

        if solution:
            print(f"   {heuristic.capitalize()}:")
            print(f"      - Nodos explorados: {solution['nodes_explored']}")
            print(f"      - Longitud del camino: {len(solution['path'])}")
            print(f"      - Costo: {solution['cost']}")

# Comparar en diferentes laberintos
compare_heuristics(maze_original, "Laberinto Original")
compare_heuristics(maze_large, "Laberinto Grande")

print("""
CONCLUSION: Manhattan es generalmente mas eficiente para
laberintos con movimientos ortogonales, explorando menos nodos.
Euclidiana puede explorar mas nodos pero sigue siendo admisible.
""")

# ============================================
# CELDA 10: LIMITACIONES DEL ALGORITMO (CELDA SEPARADA)
# ============================================

print("\n" + "="*50)
print("6. LIMITACIONES DEL ALGORITMO")
print("="*50)

print("""
LIMITACIONES IDENTIFICADAS:

1. COMPLEJIDAD ESPACIAL:
   - A* mantiene todos los nodos en memoria
   - Problema en laberintos muy grandes (>1000x1000)
   - Solucion: Usar IDA* (Iterative Deepening A*)

2. MOVIMIENTOS RESTRINGIDOS:
   - Solo 4 direcciones (arriba, abajo, izquierda, derecha)
   - No permite movimientos diagonales
   - Puede resultar en caminos mas largos

3. COSTO COMPUTACIONAL:
   - La heuristica se calcula para cada nodo
   - Con multiples salidas, aumenta el calculo
   - En laberintos grandes puede ser lento

4. LABERINTOS DINAMICOS:
   - No maneja cambios durante la busqueda
   - Si el laberinto cambia, debe recalcular todo
   - No es adaptativo a cambios en tiempo real

5. OPTIMALIDAD:
   - Depende de la admisibilidad de la heuristica
   - Con heuristica inadmisible, puede no encontrar el optimo
   - Euclidiana no es perfecta para movimientos ortogonales

PRUEBA DE ESCALABILIDAD:
""")

# Crear un laberinto muy grande para demostrar limitaciones
import random

def create_random_maze(size):
    """Genera un laberinto aleatorio de tamano especificado para pruebas de escalabilidad"""
    maze = [['#' for _ in range(size)] for _ in range(size)]

    # Generar espacios vacios de forma aleatoria
    for i in range(1, size-1):
        for j in range(1, size-1):
            if random.random() > 0.3:  # 70% de probabilidad de espacio vacio
                maze[i][j] = ' '

    # Establecer posiciones de inicio y salida
    maze[1][1] = 'S'
    maze[size-2][size-2] = 'E'

    return maze

# Probar con diferentes tamaños
print("\nTiempo de ejecucion vs Tamano del laberinto:")
for size in [10, 20, 30]:
    maze_test = create_random_maze(size)
    problem_test = MazeProblem(maze_test, 'manhattan')
    solution_test = a_star_search(problem_test)

    if solution_test:
        print(f"   - {size}x{size}: {solution_test['time']:.4f} seg, "
              f"{solution_test['nodes_explored']} nodos")

print("""
CONCLUSION: El tiempo y memoria aumentan significativamente
con el tamano del laberinto, confirmando las limitaciones
de escalabilidad del algoritmo A*.
""")

# ============================================
# RESUMEN FINAL
# ============================================

print("\n" + "="*50)
print("RESUMEN DEL TRABAJO")
print("="*50)

print("""
COMPLETADO:
1. Estructura del problema definida (actions, result, action_cost)
2. Implementacion de A* con heuristicas Manhattan y Euclidiana
3. Manejo de multiples salidas
4. Analisis de cambio de funcion de costo
5. Laberintos mas grandes con obstaculos
6. Identificacion de limitaciones

CONCLUSIONES PRINCIPALES:
- Manhattan es mas eficiente para movimientos ortogonales
- La funcion de costo afecta la ruta elegida
- El algoritmo maneja multiples salidas automaticamente
- Tiene limitaciones de escalabilidad en laberintos grandes
""")