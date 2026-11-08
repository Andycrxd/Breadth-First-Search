from collections import deque
import cv2
import numpy as np
import pandas as pd

# 1. Cargar el laberinto 150x150 desde el CSV
matriz = pd.read_csv("laberinto_150x150.csv", header=None).values
filas, columnas = matriz.shape

# Filtrar casillas transitables (valor 0)
celdas_libres = [tuple(coord) for coord in np.argwhere(matriz == 0)]
TOTAL_TRANSITABLES = len(celdas_libres)  # Son 10,951 celdas libres


def solicitar_coordenada(nombre_punto):
    """Solicita una coordenada (fila, columna) y valida que sea un camino transitable (0)."""
    while True:
        try:
            print(f"\n--- Ingrese las coordenadas para {nombre_punto} ---")
            r = int(input(f"Fila (0 a {filas-1}): "))
            c = int(input(f"Columna (0 a {columnas-1}): "))

            if not (0 <= r < filas and 0 <= c < columnas):
                print(
                    f" Error: La coordenada ({r}, {c}) está fuera del rango [0..{filas-1}]."
                )
                continue

            if matriz[r, c] != 0:
                print(
                    f" Error: La coordenada ({r}, {c}) es una PARED (valor 1). Elige una casilla libre."
                )
                continue

            return (r, c)
        except ValueError:
            print(" Error: Ingrese números enteros válidos.")


# Configuración de renderizado
FACTOR_ESCALA = 4  # Ventana de 600x600 píxeles
DURACION_OBJETIVO_SEG = 15.0
FPS = 30
DELAY_MS = int(1000 / FPS)

while True:
    print("\n" + "=" * 55)
    print("      CONFIGURACIÓN DE PRUEBA - BFS LABERINTO 150x150")
    print("=" * 55)

    inicio = solicitar_coordenada("PUNTO INICIAL (VERDE)")
    destino = solicitar_coordenada("PUNTO DESTINO (ROSA/MAGENTA)")

    if inicio == destino:
        print(
            "\n El punto inicial y el destino son el mismo. Intente de nuevo."
        )
        continue

    print(
        f"\nIniciando BFS desde {inicio} hasta {destino} (~15s de animación)..."
    )

    # 2. Ejecución del Algoritmo BFS
    frontera = deque([inicio])
    visitados = {inicio}
    padres = {}
    orden_exploracion = []
    meta_alcanzada = False

    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while frontera:
        actual = frontera.popleft()
        orden_exploracion.append(actual)

        if actual == destino:
            meta_alcanzada = True
            break

        r, c = actual
        for dr, dc in movimientos:
            nr, nc = r + dr, c + dc
            if 0 <= nr < filas and 0 <= nc < columnas and matriz[nr, nc] == 0:
                if (nr, nc) not in visitados:
                    visitados.add((nr, nc))
                    padres[(nr, nc)] = (r, c)
                    frontera.append((nr, nc))

    # Reconstrucción de la ruta
    camino = []
    if meta_alcanzada:
        curr = destino
        while curr in padres:
            camino.append(curr)
            curr = padres[curr]
        camino.append(inicio)
        camino.reverse()

    # 3. Canvas base
    img = np.zeros((filas, columnas, 3), dtype=np.uint8)
    img[matriz == 1] = [0, 0, 0]  # Paredes: Negro
    img[matriz == 0] = [255, 255, 255]  # Caminos: Blanco

    img[inicio[0], inicio[1]] = [0, 255, 0]  # Inicio: Verde
    img[destino[0], destino[1]] = [255, 0, 255]  # Destino: Rosa

    total_pasos = len(orden_exploracion)
    total_cuadros = int(DURACION_OBJETIVO_SEG * FPS)
    pasos_por_cuadro = max(1, total_pasos // total_cuadros)

    # 4. Animación paso a paso
    usuario_salio = False
    for i in range(0, total_pasos, pasos_por_cuadro):
        bloque = orden_exploracion[i : i + pasos_por_cuadro]

        for r, c in bloque:
            if (r, c) != inicio and (r, c) != destino:
                img[r, c] = [235, 180, 100]  # Visitados: Azul claro

        r_act, c_act = bloque[-1]
        if (r_act, c_act) != inicio and (r_act, c_act) != destino:
            img[r_act, c_act] = [50, 50, 255]  # Frontera: Rojo

        frame = cv2.resize(
            img,
            (columnas * FACTOR_ESCALA, filas * FACTOR_ESCALA),
            interpolation=cv2.INTER_NEAREST,
        )
        cv2.imshow("BFS Laberinto 150x150 - En Ejecucion", frame)

        tecla = cv2.waitKey(DELAY_MS) & 0xFF
        if tecla == ord("q") or tecla == 27:
            usuario_salio = True
            break

    if usuario_salio:
        break

    # 5. Colorear Ruta Óptima y Actualizar Pantalla
    if meta_alcanzada:
        for r, c in camino:
            if (r, c) != inicio and (r, c) != destino:
                img[r, c] = [0, 215, 255]  # Ruta final: Dorado

        img[inicio[0], inicio[1]] = [0, 255, 0]
        img[destino[0], destino[1]] = [255, 0, 255]

    # Generar el cuadro final resuelto
    frame_final = cv2.resize(
        img,
        (columnas * FACTOR_ESCALA, filas * FACTOR_ESCALA),
        interpolation=cv2.INTER_NEAREST,
    )

    # Cálculos de porcentaje corregidos
    pct_caminos = (len(visitados) / TOTAL_TRANSITABLES) * 100
    pct_matriz_total = (len(visitados) / (filas * columnas)) * 100

    # Texto superpuesto en la imagen
    txt_nodos = (
        f"Explorados: {len(visitados)} / {TOTAL_TRANSITABLES} ({pct_caminos:.1f}% de caminos)"
    )
    txt_pasos = (
        f"Pasos del camino: {len(camino)-1}"
        if meta_alcanzada
        else "Sin camino disponible"
    )

    cv2.putText(
        frame_final,
        txt_nodos,
        (15, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (0, 0, 0),
        3,
    )
    cv2.putText(
        frame_final,
        txt_nodos,
        (15, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        1,
    )
    cv2.putText(
        frame_final,
        txt_pasos,
        (15, 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (0, 0, 0),
        3,
    )
    cv2.putText(
        frame_final,
        txt_pasos,
        (15, 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (0, 255, 255),
        1,
    )

    # Mostrar marco final
    cv2.imshow("BFS Laberinto 150x150 - En Ejecucion", frame_final)

    # IMPRIMIR MÉTRICAS EN CONSOLA
    print("\n" + "=" * 55)
    print("              RESULTADOS DE LA BÚSQUEDA")
    print("=" * 55)
    print(f"Punto Inicial:                 {inicio}")
    print(f"Punto Destino:                 {destino}")
    print(
        f"Nodos explorados:              {len(visitados)} de {TOTAL_TRANSITABLES} celdas libres"
    )
    print(f"Porcentaje de caminos libres:  {pct_caminos:.2f}%")
    print(
        f"Porcentaje de matriz total:    {pct_matriz_total:.2f}% (incluyendo paredes)"
    )

    if meta_alcanzada:
        print(f"Estado:                        ÉXITO")
        print(f"Longitud del camino óptimo:    {len(camino) - 1} pasos")
    else:
        print(f"Estado:                        FRACASO (Sin ruta)")

    print(
        "\n Presione CUALQUIER TECLA dentro de la ventana de OpenCV para continuar..."
    )

    # FORZAR A OPENCV A PROCESAR EL EVENTO DE DIBUJO Y ESPERAR UN CLIC/TECLA EN LA VENTANA
    cv2.waitKey(0)

    respuesta = input("\n¿Desea ingresar otro par de coordenadas? (s/n): ")
    if respuesta.lower() != "s":
        break

cv2.destroyAllWindows()
