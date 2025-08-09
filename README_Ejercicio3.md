# Ejercicio 3: Navegación en una Red de Metro

**Autores:** Jose Alejandro Jimenez Vasquez, Felipe Castro, Nicolas Vasquez

## 1. Diseño del Grafo

El mapa de la red de metro se ha modelado como un grafo no dirigido donde las estaciones son los nodos y las conexiones directas entre ellas son las aristas. Dado que el objetivo es encontrar la ruta con menos paradas, todas las aristas tienen un costo uniforme de 1. La estructura del grafo se ha implementado en Python utilizando un diccionario, donde cada clave es una estación y su valor es una lista de las estaciones a las que está conectada.

## 2. Implementación de Clases y Acciones

- **Clase `Nodo`:** Representa un punto en la búsqueda. Almacena el estado (la estación actual) y una referencia a su nodo padre, lo que permite reconstruir la ruta una vez que se alcanza el objetivo.
- **Clase `Problema`:** Encapsula la definición del problema. Contiene el estado inicial, el estado objetivo y el grafo de la red de metro. Proporciona métodos para obtener las acciones posibles desde un estado (`acciones`), el resultado de una acción (`resultado`) y verificar si un estado es el objetivo (`es_objetivo`).
- **Acciones:** Las acciones se definen como el movimiento de una estación a otra conectada directamente. La función `problema.acciones(estado)` devuelve la lista de estaciones a las que se puede viajar desde la estación actual.

## 3. Algoritmos: BFS e IDS

Se han implementado dos algoritmos de búsqueda no informada para resolver el problema:

- **Búsqueda en Anchura (BFS):** Este algoritmo explora el grafo nivel por nivel. Utiliza una cola para gestionar los nodos pendientes (frontera). BFS garantiza encontrar la ruta más corta en términos de número de aristas (paradas) porque expande todos los caminos de longitud `d` antes de explorar cualquier camino de longitud `d+1`.

- **Búsqueda en Profundidad Iterativa (IDS):** IDS combina los beneficios de BFS (optimalidad) y Búsqueda en Profundidad (bajo consumo de memoria). Realiza búsquedas en profundidad con un límite de profundidad que se incrementa iterativamente (0, 1, 2, ...). Aunque parece ineficiente porque vuelve a visitar nodos, el costo de estas visitas repetidas es bajo en comparación con el crecimiento exponencial de la frontera en BFS.

## 4. Comparación de Resultados (Ruta A -> J)

Ambos algoritmos se ejecutaron para encontrar la ruta más corta desde la Estación A hasta la Estación J. Los resultados fueron los siguientes:

- **Ruta Encontrada:** Ambos algoritmos encontraron la misma ruta óptima: `['A', 'C', 'F', 'J']`.

- **Rendimiento (los valores pueden variar ligeramente en cada ejecución):**
  - **BFS:**
    - **Tiempo:** ~0.0009 segundos
    - **Memoria:** ~3768 bytes
  - **IDS:**
    - **Tiempo:** ~0.00006 segundos
    - **Memoria:** ~808 bytes

## 5. Diferencias entre BFS e IDS

Las diferencias fundamentales entre los dos algoritmos, reflejadas en los resultados, son:

- **Consumo de Memoria:**
  - **BFS** necesita almacenar todos los nodos de la frontera en memoria. En grafos anchos, esto puede llevar a un consumo de memoria exponencial (`O(b^d)`), donde `b` es el factor de ramificación y `d` la profundidad. Esto es evidente en los resultados, donde BFS usó significativamente más memoria.
  - **IDS** solo necesita almacenar la rama actual del camino en su búsqueda en profundidad, lo que resulta in un consumo de memoria lineal (`O(bd)`). Esta es su principal ventaja.

- **Tiempo de Ejecución:**
  - En este problema pequeño, **IDS** fue ligeramente más rápido. Aunque IDS regenera los nodos en cada iteración, el costo de hacerlo en los niveles superiores del árbol de búsqueda es pequeño. La sobrecarga de gestionar la cola de la frontera en BFS puede hacer que sea un poco más lento en grafos pequeños.
  - En grafos muy grandes, BFS podría ser más rápido si la solución se encuentra a una profundidad `d` y el factor de ramificación es grande, ya que IDS expandirá múltiples veces los nodos de los niveles superiores. Sin embargo, el costo en memoria de BFS a menudo lo hace impracticable mucho antes de que el tiempo de ejecución de IDS se convierta en un problema.

En resumen, **BFS** es óptimo y completo, pero su requerimiento de memoria es su mayor debilidad. **IDS** ofrece la misma optimalidad y completitud que BFS pero con un costo de memoria mucho menor, lo que lo convierte en una mejor opción para árboles de búsqueda grandes o desconocidos.