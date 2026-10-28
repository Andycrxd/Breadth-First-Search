import random
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# 1. ALGORITMO BFS (PROPUESTA CON RASTREO DE PADRES)
def resolver_laberinto_bfs(matriz, inicio, destino):
    filas, columnas = matriz.shape

    # Estructuras principales de BFS
    frontera = deque([inicio])  # Cola FIFO
    visitados = {inicio}  # Conjunto de explorados (reached)
    padres = {}  # Rastreo de ruta: padres[(r,c)] = (r_anterior, c_anterior)

    # Movimientos ortogonales: Arriba, Abajo, Izquierda, Derecha
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    encontrado = False

    while frontera:
        actual = frontera.popleft()  # Extraer el primer elemento (FIFO)

        if actual == destino:
            encontrado = True
            break

        r, c = actual

        for dr, dc in movimientos:
            nr, nc = r + dr, c + dc

            # Validar: 1) Dentro de límites, 2) Es camino libre (0), 3) No visitado
            if 0 <= nr < filas and 0 <= nc < columnas and matriz[nr, nc] == 0:
                if (nr, nc) not in visitados:
                    visitados.add((nr, nc))
                    padres[(nr, nc)] = (r, c)  # Guardar la procedencia
                    frontera.append((nr, nc))

    if not encontrado:
        return None, len(visitados)

    # Reconstrucción de la ruta desde el destino hasta el inicio
    camino = []
    paso = destino
    while paso in padres:
        camino.append(paso)
        paso = padres[paso]
    camino.append(inicio)
    camino.reverse()  # Ordenar de Origen a Destino

    return camino, len(visitados)


# 2. CARGA DE DATOS Y DEFINICIÓN DE PUNTOS
# Cargar el laberinto desde el CSV
laberinto = pd.read_csv("laberinto_150x150.csv", header=None).values

# Encontrar celdas libres (valor 0) para elegir puntos aleatorios válidos
celdas_libres = [tuple(coord) for coord in np.argwhere(laberinto == 0)]

# Seleccionar 2 puntos aleatorios dentro del laberinto
inicio, destino = random.sample(celdas_libres, 2)

print(f"Dimensiones de la matriz: {laberinto.shape}")
print(f"Punto de Inicio: {inicio}")
print(f"Punto Destino: {destino}")

# 3. EJECUCIÓN DE BFS Y GENERACIÓN DE RESULTADOS
camino, casillas_exploradas = resolver_laberinto_bfs(
    laberinto, inicio, destino
)

if camino:
    print(f"¡Ruta encontrada exitosamente!")
    print(f"Longitud del camino: {len(camino) - 1} pasos")
    print(f"Total de casillas exploradas por BFS: {casillas_exploradas}")
else:
    print("No se encontró una ruta posible entre los dos puntos.")

# 4. VISUALIZACIÓN GRAFICA DE LA SOLUCIÓN
plt.figure(figsize=(10, 10))

# Dibuja paredes en negro (1) y caminos en blanco (0)
plt.imshow(laberinto, cmap="binary")

# Trazar la ruta encontrada por BFS si existe
if camino:
    filas_camino = [p[0] for p in camino]
    cols_camino = [p[1] for p in camino]

    # Dibujar la línea de la solución sobre el laberinto
    plt.plot(
        cols_camino,
        filas_camino,
        color="gold",
        linewidth=2,
        label=f"Camino BFS ({len(camino)-1} pasos)",
    )

# Dibujar los puntos de Inicio (Verde) y Destino (Rojo)
plt.plot(inicio[1], inicio[0], "go", markersize=9, label=f"Inicio: {inicio}")
plt.plot(
    destino[1], destino[0], "ro", markersize=9, label=f"Destino: {destino}"
)

plt.title(
    f"Laberinto 150x150 - Solución BFS\nCasillas exploradas por el algoritmo: {casillas_exploradas}",
    fontsize=12,
)
plt.xlabel("Columna (X)")
plt.ylabel("Fila (Y)")
plt.legend(loc="upper right")
plt.tight_layout()

# Guardar la imagen final resuelta
plt.savefig("laberinto_solucion_bfs.png", dpi=200)
plt.show()