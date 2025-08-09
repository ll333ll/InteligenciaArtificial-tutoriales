# Ejercicio 1: Búsqueda A*

**Autores:** Jose Alejandro Jimenez Vasquez, Felipe Castro, Nicolas Vasquez

## Análisis del Problema

El problema consiste en encontrar la ruta más corta entre dos ciudades en un mapa, en este caso, desde Arad hasta Bucarest en el mapa de Rumania. Este es un problema clásico de búsqueda de caminos en un grafo, donde las ciudades son los nodos y las carreteras entre ellas son las aristas con un peso igual a la distancia.

## Aplicación de A*

El algoritmo A* es una estrategia de búsqueda informada que combina las ventajas de la búsqueda de costo uniforme (priorizando el camino ya recorrido) y la búsqueda voraz (priorizando la cercanía estimada al objetivo). Lo hace evaluando los nodos con la siguiente función:

**f(n) = g(n) + h(n)**

Donde:
- **g(n):** Es el costo real del camino desde el nodo inicial hasta el nodo `n`. En nuestro caso, es la suma de las distancias de las carreteras recorridas.
- **h(n):** Es la función heurística, que estima el costo desde el nodo `n` hasta el objetivo. Para este problema, utilizamos la distancia en línea recta desde la ciudad `n` hasta Bucarest. Esta heurística es admisible porque nunca sobrestima el costo real (la distancia en línea recta es siempre la más corta posible).

El algoritmo mantiene una cola de prioridad de nodos a explorar, ordenados por su valor `f(n)`. En cada paso, expande el nodo con el menor valor `f(n)`, añadiendo sus vecinos a la cola. Gracias a que A* tiene en cuenta tanto el costo del camino recorrido como el costo heurístico estimado, es capaz de encontrar la ruta óptima de manera eficiente.

## Optimalidad de la Ruta Encontrada

La ruta encontrada por A* es óptima porque la heurística utilizada (distancia en línea recta) es **admisible** y **consistente**.

- **Admisible:** Como se mencionó, la distancia en línea recta nunca es mayor que la distancia real por carretera. Esto garantiza que A* no se deje engañar por una estimación demasiado optimista que podría llevarlo por un camino incorrecto.
- **Consistente (o monotónica):** Para cualquier par de nodos adyacentes `n` y `n'`, el costo estimado desde `n` es menor o igual que el costo de ir de `n` a `n'` más el costo estimado desde `n'`. En un mapa con distancias euclidianas, esto se cumple.

Cuando la heurística es admisible y consistente, se puede demostrar que la primera vez que A* expande el nodo objetivo, ha encontrado la ruta óptima. Esto se debe a que cualquier otro camino hacia el objetivo que aún esté en la frontera tendrá un valor `f(n)` mayor o igual, lo que significa que su costo real `g(n)` ya es mayor o no puede ser mejor que la solución ya encontrada.

La ruta encontrada es: **['Arad', 'Sibiu', 'Rimnicu Vilcea', 'Pitesti', 'Bucharest']** con un costo total de 418.