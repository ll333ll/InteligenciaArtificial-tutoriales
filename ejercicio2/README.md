# Ejercicio 2: Problema del Laberinto

**Autores:** Jose Alejandro Jimenez Vasquez, Felipe Castro, Nicolas Vasquez

## 1. Solución del Ejercicio

Se ha implementado un algoritmo de búsqueda A* para resolver el problema del laberinto. El código `ejercicio2.py` contiene la solución, donde se define una clase `Problem` para abstraer las características del laberinto y se utiliza A* con la distancia de Manhattan como heurística para encontrar la salida.

En la implementación (ejercicio2.py), la función principal encontrar_salida usa A* combinando:
g(n): calculado en nuevo_costo, que suma el costo acumulado con el resultado de funcion_costo.
h(n): calculado por distancia_manhattan entre el nodo actual y el objetivo.
f(n) = g(n) + h(n): usado para ordenar la cola de prioridad frontera mediante heapq.
La clase Nodo almacena posicion, padre, accion y costo_camino, permitiendo reconstruir la ruta óptima con reconstruir_camino.

## 2. Cambio en la Función de Costo

La función de costo (`action_cost`) determina el "esfuerzo" de moverse a una nueva casilla. En la implementación base, cada movimiento tiene un costo uniforme de 1.

Si cambiamos esta función, el comportamiento del algoritmo se altera significativamente:

- **Rutas Preferenciales:** Si asignamos costos menores a ciertos tipos de casillas (por ejemplo, casillas que representan un "camino pavimentado"), el algoritmo preferirá estas rutas, incluso si son más largas en términos de número de pasos.
- **Evitar Zonas:** Al asignar costos mayores a otras casillas (como en el laberinto modificado, donde pasar por "agua" (`A`) tiene un costo de 5), el algoritmo intentará evitar estas zonas a menos que sea estrictamente necesario. El camino resultante podría ser más largo, pero será el de menor costo total.

En resumen, modificar la función de costo permite modelar entornos más complejos y realistas, donde no todos los movimientos son iguales, y el algoritmo optimizará la ruta basándose en el costo acumulado en lugar de solo la distancia.

## 3. Múltiples Salidas en el Laberinto

Si existen múltiples salidas, el algoritmo A* estándar se detendrá tan pronto como encuentre la primera salida en su camino. Sin embargo, esta podría no ser la salida óptima o la más cercana.

Para manejar múltiples salidas, se pueden plantear las siguientes modificaciones:

1.  **Modificar la Condición de Parada:** En lugar de tener un único estado objetivo, se tendría una lista de posibles estados objetivo. La condición `is_goal(state)` verificaría si el estado actual se encuentra en esta lista.

2.  **Encontrar la Salida Óptima (No solo la primera):**
    - **No detenerse en la primera solución:** Cuando se encuentra una salida, en lugar de terminar, se guarda la solución y su costo. El algoritmo continúa ejecutándose hasta que la frontera (la cola de prioridad) esté vacía.
    - **Comparar soluciones:** Al final, se comparan todas las soluciones encontradas y se elige la de menor costo total. Esto garantiza encontrar la mejor ruta hacia la salida más "barata".

3.  **Heurística Múltiple:** La función heurística necesitaría ser adaptada. Se podría calcular la distancia de Manhattan a la salida más cercana desde la posición actual y usar ese valor. `h(n) = min(manhattan_distance(n, exit1), manhattan_distance(n, exit2), ...)`

## 4. Laberinto Modificado y Limitaciones del Algoritmo

Se ha modificado el laberinto para hacerlo más grande y se ha añadido un nuevo tipo de obstáculo: agua (`A`), que tiene un costo de movimiento más alto.

Al ejecutar el algoritmo en este laberinto modificado, se observa que encuentra un camino que evita el agua siempre que sea posible, demostrando la flexibilidad de la función de costo. Sin embargo, esto también resalta algunas limitaciones:

- **Consumo de Memoria:** A* necesita mantener un registro de los nodos visitados (`reached`) y una frontera de nodos por visitar. En laberintos muy grandes o complejos, la cantidad de nodos puede crecer exponencialmente, consumiendo una gran cantidad de memoria. Si el laberinto fuera de, por ejemplo, 1000x1000, el diccionario `reached` podría volverse demasiado grande para la memoria disponible.

- **Rendimiento en Espacios Abiertos:** En áreas grandes y abiertas con pocos obstáculos, A* puede pasar mucho tiempo explorando caminos que tienen un costo `f(n)` muy similar. Esto se debe a que la heurística no ofrece suficiente información para decidir qué camino es claramente mejor, llevando a la exploración de una gran cantidad de nodos.

- **Calidad de la Heurística:** La eficiencia de A* depende críticamente de la calidad de la heurística. Una heurística pobre (que no se aproxima bien al costo real) puede hacer que A* se comporte de manera similar a algoritmos no informados como Dijkstra, perdiendo su ventaja en velocidad. Si en el laberinto existieran "portales" o caminos no euclidianos, la distancia de Manhattan dejaría de ser una buena estimación, y el rendimiento del algoritmo se degradaría.
